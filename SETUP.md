# Setup Guide - TechParts Mockups with ngrok

## Current Status

Your server is now running at `http://localhost:8000`

## Next Steps to Expose Publicly

### 1. Install ngrok (if not already installed)

```bash
choco install ngrok
```

### 2. Start ngrok tunnel

In a new terminal window:

```bash
ngrok http 8000
```

Or use the convenience script:

```bash
start_ngrok.bat
```

### 3. Access your public URL

ngrok will display a public URL like:
- Forwarding: `https://abc123-xyz-456.ngrok-free.app` -> `http://localhost:8000`

You can now share this URL to access your mockups.

### 4. Test your public URL

Visit: `https://your-ngrok-url.ngrok-free.app/techparts-landing.html`

## Important Notes

1. **Keep both terminals open**: The server and ngrok both need to be running
2. **Free tier limits**: ngrok free tier URLs change each time you restart ngrok
3. **Authtoken**: For persistent URLs, sign up at ngrok.com and configure an authtoken:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

## Available Pages

Once the ngrok URL is active, you can access:

- `/techparts-landing.html` - Main landing page
- `/techparts-owner-dashboard.html` - Dashboard
- `/techparts-crm.html` - CRM module
- `/techparts-erp.html` - ERP module
- `/techparts-hris.html` - HRIS module
- `/techparts-oms.html` - OMS module
- `/techparts-qms.html` - QMS module
- `/techparts-mes.html` - MES module
- `/techparts-wms.html` - WMS module
- `/techparts-automation.html` - Automation module
- `/mvp-workflow-tracker.html` - 5-Day Journey
- `/vsol-onepager.html` - One-pager

## Troubleshooting

- If port 8000 is busy, edit `server.py` and change `PORT = 8000` to another port
- Make sure Python 3 is in your PATH
- Check that all HTML files are in the `mockups/` directory
- Use `curl http://localhost:8000` to test the local server before starting ngrok

