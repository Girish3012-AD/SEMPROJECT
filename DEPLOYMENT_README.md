# Deployment Guide for Digital Complaint Box

This guide will help you deploy your Flask application to make it accessible worldwide via a domain name.

## 🚀 Quick Deployment Options

### Option 1: PythonAnywhere (Easiest - Recommended for Beginners)

**PythonAnywhere** is the simplest way to deploy your Flask app. It has a free tier and handles everything for you.

#### Steps:

1. **Create Account**: Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free account.

2. **Upload Your Code**:
   - Go to the "Files" tab in your PythonAnywhere dashboard
   - Upload all your project files (HTML, JS, CSS, Python files)
   - Make sure to upload `app_production.py` and `requirements.txt`

3. **Install Dependencies**:
   - Open a Bash console in PythonAnywhere
   - Run: `pip install -r requirements.txt`

4. **Create Web App**:
   - Go to the "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" and Python 3.9
   - Set the source code path to your project directory
   - In the WSGI configuration file, change the import to:
     ```python
     from app_production import app as application
     ```

5. **Configure Domain**:
   - PythonAnywhere gives you a free subdomain like `yourusername.pythonanywhere.com`
   - You can also use a custom domain by configuring DNS settings

6. **Reload Web App**:
   - Click the "Reload" button in the Web tab

**Your app will be live at:** `https://yourusername.pythonanywhere.com`

---

### Option 2: Railway (Modern & Easy)

**Railway** is a modern deployment platform with a generous free tier.

#### Steps:

1. **Create Account**: Go to [railway.app](https://railway.app) and sign up.

2. **Connect GitHub**: Link your GitHub repository.

3. **Deploy**:
   - Railway will automatically detect it's a Python app
   - It will install dependencies from `requirements.txt`
   - Set the start command to: `python app_production.py`

4. **Custom Domain**: You can add your own domain in the settings.

**Railway provides a free domain and handles scaling automatically.**

---

### Option 3: Render (Similar to Railway)

**Render** is another great option with a free tier.

#### Steps:

1. **Create Account**: Go to [render.com](https://render.com) and sign up.

2. **Connect Repository**: Link your GitHub repo.

3. **Create Web Service**:
   - Choose "Web Service"
   - Select your repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app_production.py`

4. **Deploy**: Render will build and deploy automatically.

**Free tier includes a custom domain option.**

---

### Option 4: DigitalOcean App Platform

**For more control and professional deployment.**

#### Steps:

1. **Create Account**: Go to [digitalocean.com](https://digitalocean.com)

2. **Create App**:
   - Choose "Apps" from the dashboard
   - Connect your GitHub repo
   - Configure resource settings
   - Set environment variables if needed

3. **Deploy**: DigitalOcean handles the rest.

**Pricing starts at $5/month for basic apps.**

---

## 🔧 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] All files are committed to GitHub
- [ ] `app_production.py` is ready (uses `0.0.0.0` host and environment PORT)
- [ ] `requirements.txt` includes all dependencies
- [ ] Database file (`complaint_box.db`) is included (or will be created on first run)
- [ ] Static files (HTML, CSS, JS) are in the project root

## 🌐 Custom Domain Setup

Once deployed, you can point your custom domain to the service:

1. **Buy a domain** from Namecheap, GoDaddy, etc.
2. **Configure DNS** in your domain provider's settings
3. **Add domain** in your deployment platform's settings

## 🔒 Security Considerations

For production:

- Change the default admin password in `app_production.py`
- Set a strong `SECRET_KEY` environment variable
- Consider using a production database (PostgreSQL) instead of SQLite
- Enable HTTPS (most platforms do this automatically)

## 🆘 Troubleshooting

**App not loading:**
- Check the deployment logs
- Ensure all dependencies are installed
- Verify the start command is correct

**Database issues:**
- Make sure the SQLite file has proper permissions
- For persistent data, consider cloud database services

**Domain not working:**
- Wait for DNS propagation (can take 24-48 hours)
- Check DNS settings with tools like `dig` or `nslookup`

---

**Need help?** Most deployment platforms have excellent documentation and support communities.