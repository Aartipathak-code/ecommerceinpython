# E-Commerce Application Deployment

## Quick Start - Deploy to Render (Easiest)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your repository
5. Render will detect the `render.yaml` file automatically
6. Click **"Create Web Service"**
7. Wait 2-3 minutes for deployment

Your app will be live at: `https://your-app-name.onrender.com`

---

## Alternative: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-deploys!

Your app will be live at: `https://your-app.railway.app`

---

## Files Included for Deployment

- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Files to exclude from git
- ✅ `Procfile` - For Heroku deployment
- ✅ `render.yaml` - For Render deployment
- ✅ `vercel.json` - For Vercel deployment

---

## Important Notes

### Database
Your SQLite database won't persist on most free hosting platforms. For production, consider:
- PostgreSQL (most platforms offer free tier)
- MySQL
- MongoDB

### CORS Settings
Update `main.py` to allow your production domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Update this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

For detailed deployment instructions for all platforms, see the full deployment guide.
