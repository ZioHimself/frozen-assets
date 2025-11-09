# Quick Start Guide

## TL;DR - Get Your Website Working in 5 Minutes

### Step 1: Create the API (2 minutes)

1. Open your spreadsheet: https://docs.google.com/spreadsheets/d/1rRkDt7FXyLgYCLBGE12t5gFxnhXoKy2xgiLPrdr7bcA/edit
2. Click **Extensions** → **Apps Script**
3. Paste this code:

```javascript
function doGet(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const jsonData = data.slice(1).map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index];
    });
    return obj;
  });
  const output = ContentService.createTextOutput(JSON.stringify(jsonData));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}
```

4. Click **Deploy** → **New deployment**
5. Choose **Web app** (click gear icon)
6. Set "Who has access" to **Anyone**
7. Click **Deploy** and authorize
8. **Copy the URL** that appears

### Step 2: Configure Your Website (1 minute)

1. Open `docs/config.js`
2. Replace `YOUR_APPS_SCRIPT_URL_HERE` with your URL:

```javascript
const CONFIG = {
    API_URL: 'https://script.google.com/macros/s/YOUR_URL_HERE/exec',
    USE_FALLBACK: false
};
```

3. Save the file

### Step 3: Test (1 minute)

1. Open `docs/index.html` in your browser
2. Scroll to the Database section
3. Your documents should load! 🎉

## That's It!

Your website now pulls data directly from your Google Sheet. Update the sheet, refresh the page, and see your changes!

---

**Having issues?** Check the [Full Setup Guide](SETUP.md) for detailed troubleshooting.

