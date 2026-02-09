#!/usr/bin/env python
"""Quick script to check if ffmpeg is installed and accessible."""

import subprocess
import sys

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("FFmpeg is installed!")
            print("\nVersion info:")
            print(result.stdout.split('\n')[0])
            return True
        else:
            print("FFmpeg is not working properly")
            return False
    except FileNotFoundError:
        print("FFmpeg is NOT installed")
        print("\nTo install FFmpeg:")
        print("1. See INSTALL_FFMPEG.md for detailed instructions")
        print("2. Or use: winget install ffmpeg (Windows 10/11)")
        print("3. Or use: choco install ffmpeg (if you have Chocolatey)")
        return False
    except Exception as e:
        print(f"Error checking FFmpeg: {e}")
        return False

if __name__ == '__main__':
    print("Checking for FFmpeg installation...\n")
    if check_ffmpeg():
        sys.exit(0)
    else:
        sys.exit(1)
