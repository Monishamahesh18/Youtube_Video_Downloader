from flask import Flask, render_template, request, jsonify, send_file, Response, make_response
import os
import yt_dlp
import uuid
import glob
import re
import threading
import time
import signal
import sys
from functools import wraps

app = Flask(__name__)

# Production configuration
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # No caching for downloads

# Configure upload folder
UPLOAD_FOLDER = 'downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cleanup old files periodically
def cleanup_old_files():
    """Remove files older than 1 hour"""
    try:
        current_time = time.time()
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getctime(filepath)
                if file_age > 3600:  # 1 hour
                    try:
                        os.remove(filepath)
                    except:
                        pass
    except:
        pass

# Run cleanup every 30 minutes
def periodic_cleanup():
    while True:
        time.sleep(1800)  # 30 minutes
        cleanup_old_files()

cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
cleanup_thread.start()

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def timeout_handler(signum, frame):
    raise TimeoutError("Download timeout")

@app.route('/')
def index():
    """Main page - optimized for fast loading"""
    response = make_response(render_template('index.html'))
    # Cache headers for faster subsequent loads
    response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/health')
def health():
    """Health check endpoint for Railway - keeps app awake"""
    return jsonify({'status': 'ok', 'service': 'youtube-downloader'}), 200

@app.route('/ping')
def ping():
    """Simple ping endpoint for keep-alive"""
    return 'pong', 200

@app.route('/download', methods=['POST'])
def download():
    downloaded_file = None
    video_id = None
    
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
        
        # Validate YouTube URL
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Generate unique filename
        video_id = str(uuid.uuid4())
        output_path = os.path.join(UPLOAD_FOLDER, f'{video_id}.%(ext)s')
        
        # Get video info first with timeout
        info_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,  # 30 second timeout
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                safe_title = sanitize_filename(title)
        except Exception as e:
            return jsonify({'error': f'Failed to get video info: {str(e)}'}), 500
        
        # Check if ffmpeg is available
        import shutil
        has_ffmpeg = shutil.which('ffmpeg') is not None
        
        # Optimize format selection for SPEED and QUALITY
        # Priority: Fast single-file formats > merged formats
        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],  # Use faster clients
                }
            },
            # Optimize for speed
            'concurrent_fragment_downloads': 4,  # Download fragments in parallel
            'http_chunk_size': 10485760,  # 10MB chunks for faster download
        }
        
        if has_ffmpeg:
            # With ffmpeg: prioritize high quality but optimize format selection
            # Use formats that merge quickly
            ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=720][ext=mp4]/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        else:
            # Without ffmpeg: prioritize fast single-file formats
            # Limit to 1080p max for speed, but prioritize mp4 for compatibility
            ydl_opts['format'] = 'best[height<=1080][ext=mp4]/best[height<=720][ext=mp4]/best[ext=mp4]/best[height<=1080]/best[height<=720]/best'
        
        # Download with timeout protection
        download_success = False
        download_error = None
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_success = True
        except yt_dlp.utils.DownloadError as e:
            download_error = str(e)
            # Try fallback format if first attempt fails
            if 'ffmpeg' not in download_error.lower():
                try:
                    ydl_opts['format'] = 'best[ext=mp4]/best'
                    ydl_opts.pop('postprocessors', None)
                    ydl_opts.pop('merge_output_format', None)
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    download_success = True
                except:
                    pass
        
        if not download_success:
            error_msg = download_error or 'Download failed'
            if 'ffmpeg' in error_msg.lower():
                return jsonify({'error': 'Video processing failed. Please try again.'}), 500
            return jsonify({'error': f'Download failed: {error_msg}'}), 500
        
        # Find the downloaded file - optimized search
        downloaded_file = None
        
        # Check for file with video_id (most likely location)
        for ext in ['mp4', 'webm', 'mkv', 'm4v', 'mov']:
            potential_file = os.path.join(UPLOAD_FOLDER, f'{video_id}.{ext}')
            if os.path.exists(potential_file):
                downloaded_file = potential_file
                break
        
        # If not found, check recent files
        if not downloaded_file:
            try:
                all_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
                video_extensions = ('.mp4', '.webm', '.mkv', '.m4v', '.mov')
                video_files = [f for f in all_files if f.lower().endswith(video_extensions) and os.path.isfile(f)]
                
                if video_files:
                    # Get the most recently modified file
                    downloaded_file = max(video_files, key=os.path.getmtime)
            except:
                pass
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            return jsonify({'error': 'Download completed but file not found. Please try again.'}), 500
        
        # Determine MIME type and extension
        ext = os.path.splitext(downloaded_file)[1].lower()
        mime_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.m4v': 'video/mp4',
            '.mov': 'video/quicktime'
        }
        mime_type = mime_types.get(ext, 'video/mp4')
        
        # Clean up old files before sending
        cleanup_old_files()
        
        # Return file for download with proper headers for mobile
        response = send_file(
            downloaded_file,
            as_attachment=True,
            download_name=f'{safe_title}{ext}',
            mimetype=mime_type
        )
        
        # Add headers for better mobile compatibility
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Cleanup file after sending (in background)
        def cleanup_after_send():
            time.sleep(60)  # Wait 1 minute
            try:
                if downloaded_file and os.path.exists(downloaded_file):
                    os.remove(downloaded_file)
            except:
                pass
        
        threading.Thread(target=cleanup_after_send, daemon=True).start()
        
        return response
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        return jsonify({'error': f'Download error: {error_msg[:200]}'}), 500
    except Exception as e:
        error_msg = str(e)
        return jsonify({'error': f'An error occurred: {error_msg[:200]}'}), 500
    finally:
        # Cleanup on error
        if video_id:
            try:
                for ext in ['mp4', 'webm', 'mkv', 'm4v', 'mov', 'part']:
                    potential_file = os.path.join(UPLOAD_FOLDER, f'{video_id}.{ext}')
                    if os.path.exists(potential_file) and potential_file != downloaded_file:
                        try:
                            os.remove(potential_file)
                        except:
                            pass
            except:
                pass

@app.route('/info', methods=['POST'])
def get_info():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
        
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 15,  # Faster timeout for info
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],  # Use fast client for info
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get('duration', 0)
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'duration': duration,
                'thumbnail': info.get('thumbnail', ''),
            })
            
    except Exception as e:
        return jsonify({'error': str(e)[:200]}), 500

# Keep-alive mechanism - ping health endpoint periodically
def start_keep_alive():
    """Background thread to keep Railway awake"""
    def ping():
        while True:
            try:
                time.sleep(240)  # 4 minutes
                # Simple HTTP request to health endpoint
                import urllib.request
                try:
                    port = int(os.environ.get('PORT', 5000))
                    urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2)
                except:
                    pass
            except:
                pass
    thread = threading.Thread(target=ping, daemon=True)
    thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Start keep-alive in production
    if not debug:
        start_keep_alive()
    
    # Use production WSGI server if available
    # Railway will use gunicorn from Procfile, so this is for local/dev
    app.run(debug=debug, host='0.0.0.0', port=port, threaded=True)
