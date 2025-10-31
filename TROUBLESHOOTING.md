# Troubleshooting Guide - TechParts Mockups

## Common Issues and Solutions

### ERR_NGROK_3200: The endpoint is offline

**Error Message:**
```
ERR_NGROK_3200
The endpoint [domain].ngrok-free.dev is offline.
```

**Cause:**
- ngrok tunnel has expired or been terminated
- Old/stale ngrok URL is being accessed
- ngrok process crashed or was stopped
- ngrok is pointing to the wrong port (e.g., port 80 instead of 8000)

**Diagnosis Steps:**

1. Check if the Python server is running:
   ```bash
   netstat -an | findstr ":8000.*LISTENING"
   ```
   Should show `TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING`

2. Check if ngrok process is running:
   ```bash
   tasklist | findstr /I "ngrok.exe"
   ```

3. Verify ngrok tunnel configuration:
   ```powershell
   powershell -Command "Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels' | ConvertTo-Json -Depth 5"
   ```
   Check that `config.addr` is `http://localhost:8000`, not `http://localhost:80`

**Solution:**

1. Kill all existing ngrok processes:
   ```bash
   taskkill /F /IM ngrok.exe
   ```

2. Ensure the server is running on port 8000:
   ```bash
   python server.py
   ```
   Or use: `start_server.bat`

3. Start ngrok with the correct port:
   ```bash
   ngrok http 8000
   ```
   Or use: `start_ngrok.bat`

4. Wait 3-5 seconds for ngrok to initialize, then verify:
   ```powershell
   powershell -Command "$tunnels = Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels'; $httpsTunnel = $tunnels.tunnels | Where-Object { $_.proto -eq 'https' } | Select-Object -First 1; Write-Host 'Public URL:' $httpsTunnel.public_url; Write-Host 'Target:' $httpsTunnel.config.addr"
   ```

**Verification:**

After restarting, test your new URL:
- Open the ngrok web interface: `http://127.0.0.1:4040`
- Or get the URL programmatically (see command above)
- Test the landing page: `https://[your-new-url].ngrok-free.app/techparts-landing.html`

**Important Notes:**

- Free ngrok URLs change each time you restart ngrok
- Always use the current ngrok URL shown in the ngrok console or web interface
- Keep both the server and ngrok processes running simultaneously
- For persistent URLs, sign up at ngrok.com and configure an authtoken

## Getting the Current ngrok URL

### Method 1: ngrok Web Interface

Navigate to: `http://127.0.0.1:4040`

The web interface shows:
- Current public URL
- Tunnel statistics
- Request inspector
- Connection status

### Method 2: Command Line (PowerShell)

```powershell
$tunnels = Invoke-RestMethod -Uri 'http://127.0.0.1:4040/api/tunnels'
$httpsTunnel = $tunnels.tunnels | Where-Object { $_.proto -eq 'https' } | Select-Object -First 1
Write-Host "Public URL: $($httpsTunnel.public_url)"
Write-Host "Target: $($httpsTunnel.config.addr)"
```

### Method 3: Check ngrok Console Output

When you start ngrok with `ngrok http 8000`, it displays:
```
Forwarding    https://[random-id].ngrok-free.app -> http://localhost:8000
```

Use that `https://[random-id].ngrok-free.app` URL.

## Port Conflicts

If port 8000 is already in use:

1. Find what's using the port:
   ```bash
   netstat -ano | findstr :8000
   ```

2. Either:
   - Change the server port in `server.py` (edit `PORT = 8000` to another port)
   - Kill the process using port 8000 (if appropriate)

3. Update ngrok to use the new port:
   ```bash
   ngrok http [new-port]
   ```

## Server Not Responding

If the local server isn't working:

1. Verify Python is installed:
   ```bash
   python --version
   ```

2. Check the server logs for errors when starting:
   ```bash
   python server.py
   ```

3. Verify the mockups directory exists:
   ```bash
   dir mockups
   ```

4. Test local access before using ngrok:
   ```bash
   curl http://localhost:8000
   ```
   Or open in browser: `http://localhost:8000/techparts-landing.html`

## Successful Setup Checklist

- [ ] Python server running on port 8000 (verify with `netstat`)
- [ ] ngrok process running (verify with `tasklist`)
- [ ] ngrok tunnel pointing to `http://localhost:8000` (verify via API)
- [ ] Can access landing page locally: `http://localhost:8000/techparts-landing.html`
- [ ] Can access landing page via ngrok: `https://[url].ngrok-free.app/techparts-landing.html`
- [ ] ngrok web interface accessible: `http://127.0.0.1:4040`

## Example: Successful Setup

```
Server Status:
  ✓ Python server listening on port 8000
  ✓ ngrok process running (PID: 49540)

Tunnel Status:
  ✓ Public URL: https://5e605cc36c9e.ngrok-free.app
  ✓ Target: http://localhost:8000

Access Points:
  - Local: http://localhost:8000/techparts-landing.html
  - Public: https://5e605cc36c9e.ngrok-free.app/techparts-landing.html
  - Dashboard: http://127.0.0.1:4040
```

