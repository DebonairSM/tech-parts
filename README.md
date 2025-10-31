# TechParts Mockups

HTML mockups for TechParts Manufacturing MVP demo.

## Quick Start

### Start the server

```bash
# Windows
start_server.bat

# Or directly with Python
python server.py
```

Server starts on `http://localhost:8000`

### Expose with ngrok

In a separate terminal:

```bash
ngrok http 8000
```

This will give you a public URL like `https://abc123.ngrok.io`

Visit the landing page: `https://your-ngrok-url.ngrok.io/techparts-landing.html`

## Modules

All mockups are in the `mockups/` directory:

- **techparts-landing.html** - Main landing page
- **techparts-owner-dashboard.html** - Owner dashboard
- **techparts-crm.html** - Customer Relationship Management
- **techparts-erp.html** - Enterprise Resource Planning
- **techparts-hris.html** - Human Resources Information System
- **techparts-oms.html** - Order Management System
- **techparts-qms.html** - Quality Management System
- **techparts-mes.html** - Manufacturing Execution System
- **techparts-wms.html** - Warehouse Management System
- **techparts-automation.html** - AI & Automation
- **mvp-workflow-tracker.html** - 5-Day Journey tracker
- **vsol-onepager.html** - VSOL one-pager

## Navigation

All pages have built-in navigation in the header to switch between modules.

## Requirements

- Python 3.x
- ngrok (for public URL)

### Install ngrok

Option 1 - Using Chocolatey (recommended):
```bash
choco install ngrok
```

Option 2 - Download from [ngrok.com](https://ngrok.com/download) and add to PATH

