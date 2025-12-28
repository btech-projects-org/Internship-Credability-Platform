# Vercel Deployment Guide

## Overview
This project is configured for deployment on Vercel with a Python Flask backend and static frontend.

## Project Structure for Vercel
```
.
├── api/                    # Serverless functions
│   └── index.py           # Main API handler
├── backend/               # Backend source code
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   ├── models/           # ML models
│   └── requirements.txt  # Python dependencies
├── frontend/             # Static frontend files
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── pages/
├── vercel.json           # Vercel configuration
└── .vercelignore         # Files to exclude from deployment
```

## Prerequisites
1. Vercel account (free tier available)
2. Vercel CLI (optional): `npm install -g vercel`
3. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)
1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Visit [vercel.com](https://vercel.com) and sign in
3. Click "Add New Project"
4. Import your Git repository
5. Configure environment variables (see below)
6. Click "Deploy"

### Option 2: Deploy via CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

## Environment Variables
Configure these in Vercel Dashboard → Project Settings → Environment Variables:

### Required Variables
- `FLASK_ENV=production`
- Add any API keys or secrets from `backend/config/secrets.env`

Example variables you may need:
```
OPENAI_API_KEY=your_key_here
HUGGINGFACE_TOKEN=your_token_here
```

## Configuration Details

### vercel.json
- **Static Files**: Frontend files served from `/frontend`
- **API Routes**: All `/api/*` routes handled by Python serverless function
- **Memory**: 1024 MB allocated for Python function
- **Timeout**: 30 seconds max execution time

### API Endpoint Structure
After deployment, your API will be available at:
```
https://your-project.vercel.app/api/credibility
https://your-project.vercel.app/api/sentiment
https://your-project.vercel.app/api/health
```

## Important Notes

### Size Limitations
Vercel has deployment size limits:
- **Serverless Function**: Max 50 MB (compressed)
- **Total Deployment**: Depends on plan (Free: 100 MB)

### Large Dependencies
Some ML libraries (TensorFlow, PyTorch) are very large. Consider:
1. **Optimize dependencies**: Remove unused packages from `requirements.txt`
2. **Use lighter alternatives**: 
   - Use `tensorflow-cpu` instead of `tensorflow`
   - Consider `transformers` lite versions
3. **External model hosting**: Store large models on external storage

### Cold Starts
Serverless functions may experience cold starts (1-5 seconds). This is normal for infrequently accessed endpoints.

## Testing Deployment Locally

Test the production build locally:
```bash
# Install Vercel CLI
npm install -g vercel

# Run local development server
vercel dev
```

## Troubleshooting

### Build Fails
1. Check build logs in Vercel dashboard
2. Verify `requirements.txt` dependencies
3. Ensure Python version compatibility (Vercel uses Python 3.9)

### API Returns 404
1. Verify routes in `vercel.json`
2. Check API endpoint URLs
3. Ensure blueprints are properly registered

### Function Timeout
1. Increase `maxDuration` in `vercel.json` (max 60s for Pro plans)
2. Optimize slow operations
3. Consider caching results

### Import Errors
1. Verify all backend modules are in the correct paths
2. Check `sys.path` configuration in `api/index.py`
3. Ensure all `__init__.py` files exist

## Performance Optimization

### 1. Reduce Package Size
```bash
# Create minimal requirements.txt for production
pip freeze > requirements-full.txt
# Edit requirements.txt to include only necessary packages
```

### 2. Enable Caching
Update `vercel.json` to cache static assets:
```json
{
  "headers": [
    {
      "source": "/(.*\\.(css|js|png|jpg|jpeg|gif|svg|ico))",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 3. Use Edge Functions (Advanced)
For frequently accessed, lightweight operations, consider Vercel Edge Functions.

## Monitoring

1. **Analytics**: Enable in Vercel Dashboard → Analytics
2. **Logs**: View in Vercel Dashboard → Deployments → Function Logs
3. **Performance**: Monitor cold starts and execution time

## Custom Domain

1. Go to Vercel Dashboard → Project → Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed

## Rollback

If deployment fails:
1. Go to Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
