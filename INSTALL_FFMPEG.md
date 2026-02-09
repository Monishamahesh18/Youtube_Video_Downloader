# Installing FFmpeg (Optional but Recommended)

FFmpeg is needed to merge video and audio streams for the highest quality downloads. However, the app will try to download single-file formats first to avoid this requirement.

## Why FFmpeg?

Some YouTube videos have separate video and audio streams. FFmpeg merges them into a single file. Without it, the app will try to download videos that already have audio+video combined.

## Installation Instructions

### Windows (Easiest Method)

1. **Download FFmpeg**:
   - Go to https://www.gyan.dev/ffmpeg/builds/
   - Click "ffmpeg-release-essentials.zip"
   - Download the file

2. **Extract**:
   - Extract the zip file to a folder (e.g., `C:\ffmpeg`)

3. **Add to PATH**:
   - Press `Windows + R`
   - Type `sysdm.cpl` and press Enter
   - Go to "Advanced" tab → "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin` (or wherever you extracted it)
   - Click OK on all windows

4. **Verify**:
   - Open a NEW Command Prompt (close and reopen)
   - Type: `ffmpeg -version`
   - You should see version information

### Alternative: Using Chocolatey (Windows)

If you have Chocolatey installed:
```bash
choco install ffmpeg
```

### Alternative: Using winget (Windows 10/11)

```bash
winget install ffmpeg
```

## After Installation

1. **Restart your Flask app** (if it's running)
2. **Try downloading again** - it should work now!

## Note

The app will work without FFmpeg for most videos, but some high-quality videos might require it. Installing FFmpeg ensures the best compatibility.
