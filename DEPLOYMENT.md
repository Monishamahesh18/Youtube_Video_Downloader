# Deployment Guide - YouTube Downloader

This guide will help you deploy your YouTube downloader website so you can access it from your mobile device.

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest & Free Tier Available)

1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select this repository

3. **Deploy**:
   - Railway will automatically detect Python and install dependencies
   - Your app will be live in 2-3 minutes!

4. **Access from Mobile**:
   - Railway provides a public URL (like `your-app.railway.app`)
   - Open this URL on your mobile browser
   - Done! 🎉

### Option 2: Render (Free Tier Available)

1. **Sign up**: Go to [render.com](https://render.com) and sign up

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

3. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)

5. **Access from Mobile**:
   - Render provides a URL (like `your-app.onrender.com`)
   - Open on your mobile browser

### Option 3: PythonAnywhere (Free Tier Available)

1. **Sign up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload Files**:
   - Go to "Files" tab
   - Upload all your project files

3. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask and Python 3.13

4. **Configure**:
   - Set source code directory to your project folder
   - Set WSGI file to point to `app.py`

5. **Install Dependencies**:
   - Go to "Consoles" → "Bash"
   - Run: `pip3.13 install --user -r requirements.txt`

6. **Reload**:
   - Go back to "Web" tab
   - Click "Reload" button

### Option 4: Heroku (Requires Credit Card, but Free Tier)

1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create App**:
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open**:
   ```bash
   heroku open
   ```

## 📱 Testing Locally First (Before Deployment)

To test on your local network (accessible from mobile on same WiFi):

1. **Find your local IP**:
   - Windows: Open CMD, type `ipconfig`, look for IPv4 Address
   - Example: `192.168.1.100`

2. **Run the app**:
   ```bash
   python app.py
   ```

3. **Access from mobile**:
   - Make sure your phone is on the same WiFi network
   - Open browser on phone
   - Go to: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

## ⚙️ Important Notes

- **Free tiers** usually have limitations (sleep after inactivity, slower speeds)
- **Railway** and **Render** are easiest for beginners
- The app is already configured to work on any hosting platform
- Make sure to keep your deployment URL private if it's for personal use only

## 🔒 Security Note

For personal use, consider:
- Adding basic authentication
- Using a custom domain
- Setting up rate limiting

## 📝 After Deployment

Once deployed, you'll get a public URL. Simply:
1. Open the URL on your mobile browser
2. Paste YouTube links
3. Download videos!

---

**Need help?** Check the platform's documentation or support forums.
