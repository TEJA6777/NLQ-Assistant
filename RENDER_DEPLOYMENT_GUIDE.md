# 🚀 Render.com Deployment Guide for NLQ Assistant

## Step 1: Delete the Old Service (IMPORTANT!)
**Why?** The old service has incorrect configuration. We need to start fresh.

1. Go to https://dashboard.render.com/
2. Find "nlq-assistant" service
3. Click it → Go to "Settings"
4. Scroll to bottom → Click "Delete Web Service"
5. Type the service name to confirm and delete

---

## Step 2: Create a New Web Service

1. Click **"New +"** → **"Web Service"**

2. **Connect your Repository:**
   - Click "Connect" next to your GitHub account
   - Search for: `NLQ-Assistant`
   - Click to connect it

3. **Fill in the Configuration:**

   | Field | Value |
   |-------|-------|
   | **Name** | nlq-assistant |
   | **Environment** | Python 3 |
   | **Region** | Choose closest to you |
   | **Branch** | master |
   | **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input` |
   | **Start Command** | `gunicorn nlq_project.wsgi:application` |
   | **Instance Type** | Free |

4. **Add Environment Variables** (click "Add Environment Variable" for each):

   | Key | Value |
   |-----|-------|
   | `DEBUG` | `False` |
   | `SECRET_KEY` | `your-secure-random-key-here` (or keep Django's default) |
   | `GEMINI_API_KEY` | Your actual Google Gemini API key |
   | `ALLOWED_HOSTS` | `your-service-name.onrender.com` |

5. **Click "Create Web Service"**

6. **Wait** for build to complete (5-10 minutes)
   - Watch the logs for any errors
   - If successful, you'll see: `==> Your service is live!`

---

## Step 3: Get Your Live URL

Once deployed, you'll see something like:
```
https://nlq-assistant-xxxxx.onrender.com
```

Click it to visit your live site!

---

## Troubleshooting

### If build fails:
1. Go to "Logs" tab
2. Read the error message
3. Common issues:
   - Missing `GEMINI_API_KEY` → Add it in Environment Variables
   - Database error → Delete service and try again
   - Static files error → The build command handles this

### If site shows error after deployment:
1. Check Render logs
2. Make sure `DEBUG=False` (not `DEBUG=false`)
3. Verify `ALLOWED_HOSTS` matches your Render URL

### If you need to redeploy:
- Just push new code to GitHub
- Render will automatically rebuild

---

## Your Project Files Are Ready!

✅ `requirements.txt` - All dependencies  
✅ `Procfile` - Startup configuration  
✅ `build.sh` - Build script  
✅ `nlq_project/settings.py` - Production settings  
✅ GitHub repo - Connected and ready  

**You're all set!** Follow the steps above and your app will be live.
