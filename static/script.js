let downloadInProgress = false;

// Handle paste event with debounce
let infoTimeout;
document.getElementById('youtubeUrl').addEventListener('paste', function(e) {
    clearTimeout(infoTimeout);
    infoTimeout = setTimeout(() => {
        const url = this.value.trim();
        if (url && (url.includes('youtube.com') || url.includes('youtu.be'))) {
            getVideoInfo(url);
        }
    }, 300);
});

// Handle Enter key
document.getElementById('youtubeUrl').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !downloadInProgress) {
        handleDownload();
    }
});

// Handle input change with debounce
let inputTimeout;
document.getElementById('youtubeUrl').addEventListener('input', function() {
    clearTimeout(inputTimeout);
    inputTimeout = setTimeout(() => {
        const url = this.value.trim();
        if (url && (url.includes('youtube.com') || url.includes('youtu.be'))) {
            getVideoInfo(url);
        } else {
            hideVideoInfo();
            hideMessages();
        }
    }, 500);
});

async function getVideoInfo(url) {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
        
        const response = await fetch('/info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (response.ok) {
            const data = await response.json();
            showVideoInfo(data);
        } else {
            hideVideoInfo();
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Error fetching video info:', error);
        }
        hideVideoInfo();
    }
}

function showVideoInfo(info) {
    const videoInfo = document.getElementById('videoInfo');
    const thumbnail = document.getElementById('thumbnail');
    const videoTitle = document.getElementById('videoTitle');
    const videoDuration = document.getElementById('videoDuration');

    thumbnail.src = info.thumbnail || '';
    videoTitle.textContent = info.title || 'Unknown Title';
    
    const duration = info.duration || 0;
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    videoDuration.textContent = `Duration: ${minutes}:${seconds.toString().padStart(2, '0')}`;

    videoInfo.style.display = 'block';
}

function hideVideoInfo() {
    document.getElementById('videoInfo').style.display = 'none';
}

function hideMessages() {
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    document.getElementById('successMessage').style.display = 'none';
}

function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
}

async function handleDownload() {
    const url = document.getElementById('youtubeUrl').value.trim();
    const downloadBtn = document.getElementById('downloadBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        showError('Please enter a valid YouTube URL');
        return;
    }

    if (downloadInProgress) {
        return;
    }

    downloadInProgress = true;
    downloadBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'block';
    hideMessages();

    try {
        // Add timeout for mobile browsers (5 minutes)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes
        
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (response.ok) {
            // Get filename from Content-Disposition header or use default
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'video.mp4';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }

            // Create blob and download
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(downloadUrl);

            showSuccess('Video downloaded successfully!');
        } else {
            const error = await response.json();
            let errorMessage = error.error || 'Download failed. Please try again.';
            
            showError(errorMessage);
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            showError('Download timeout. The video might be too large. Please try again or use a shorter video.');
        } else {
            showError('An error occurred. Please check your connection and try again.');
        }
        console.error('Download error:', error);
    } finally {
        downloadInProgress = false;
        downloadBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}
