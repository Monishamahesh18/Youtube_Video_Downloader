# Deploying to Vercel

## ⚠️ Important Limitations

Vercel has some limitations for this type of app:
- **10-second timeout** on free tier (upgradable to 300 seconds on Pro)
- **50MB response limit** - large video files might fail
- **Serverless functions** - not ideal for long-running downloads

## Better Alternatives (Recommended)

### 🚀 Railway (Easiest - Recommended)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your repository
5. Done! Get a public URL instantly

**Advantages:**
- ✅ No timeout limits
- ✅ Handles large files
- ✅ Free tier available
- ✅ Auto-deploys on git push

### 🌐 Render (Also Great)
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect repository
5. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Deploy!

**Advantages:**
- ✅ Free tier available
- ✅ Good for Flask apps
- ✅ Auto-deploys

## Vercel Setup (If You Still Want It)

### Prerequisites
- Vercel account (free)
- Vercel CLI installed: `npm i -g vercel`

### Steps

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **For production**:
   ```bash
   vercel --prod
   ```

### Important Notes for Vercel

- You'll need a **Pro plan** ($20/month) for 300-second timeout
- Large videos (>50MB) won't work on free tier
- Consider using Railway or Render instead

## Recommendation

**Use Railway** - it's the easiest and best suited for this Flask app with video downloads.
