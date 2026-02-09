from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp
import uuid
import glob
import re

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
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
        
        # Get video info first
        info_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            safe_title = sanitize_filename(title)
        
        # Configure yt-dlp options - Prioritize highest quality formats
        # Check if ffmpeg is available for merging high quality video+audio
        import shutil
        has_ffmpeg = shutil.which('ffmpeg') is not None
        
        ydl_opts = {
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }
        
        if has_ffmpeg:
            # If ffmpeg is available, merge highest quality video+audio streams
            # This gives us the best possible quality
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        else:
            # Without ffmpeg, prioritize highest quality single-file formats
            # Format selector: get best quality formats that already have video+audio combined
            # Prioritize by resolution: 4K > 1440p > 1080p > 720p > best available
            ydl_opts['format'] = 'best[height>=2160][ext=mp4]/best[height>=1440][ext=mp4]/best[height>=1080][ext=mp4]/best[height>=720][ext=mp4]/best[ext=mp4]/best[height>=2160]/best[height>=1440]/best[height>=1080]/best[height>=720]/best'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video
            ydl.download([url])
        
        # Find the downloaded file
        downloaded_file = None
        
        # Check for file with video_id
        for ext in ['mp4', 'webm', 'mkv', 'm4v', 'mov']:
            potential_file = os.path.join(UPLOAD_FOLDER, f'{video_id}.{ext}')
            if os.path.exists(potential_file):
                downloaded_file = potential_file
                break
        
        # If not found, check for any recent video file in downloads folder
        if not downloaded_file:
            all_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
            video_extensions = ('.mp4', '.webm', '.mkv', '.m4v', '.mov')
            video_files = [f for f in all_files if f.lower().endswith(video_extensions)]
            
            if video_files:
                # Get the most recently created file
                downloaded_file = max(video_files, key=os.path.getctime)
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            return jsonify({'error': 'Download failed. Please try again or check if the video is available.'}), 500
        
        # Determine MIME type
        ext = os.path.splitext(downloaded_file)[1].lower()
        mime_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.m4v': 'video/mp4',
            '.mov': 'video/quicktime'
        }
        mime_type = mime_types.get(ext, 'video/mp4')
        
        # Return file for download
        return send_file(
            downloaded_file,
            as_attachment=True,
            download_name=f'{safe_title}{ext}',
            mimetype=mime_type
        )
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if 'ffmpeg' in error_msg.lower():
            return jsonify({'error': 'This video requires format merging. Please install FFmpeg or try a different video.'}), 500
        return jsonify({'error': f'Download error: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
