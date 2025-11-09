# Setup Guide: Connecting Google Sheets to Your Website

This guide will help you set up the Google Apps Script API to fetch data from your Google Sheets spreadsheet and display it on your website.

## Problem

Direct fetching from Google Sheets using JavaScript causes CORS (Cross-Origin Resource Sharing) errors. The solution is to create a simple API using Google Apps Script that serves your data with proper CORS headers.

## Solution: Google Apps Script Web App

### Step 1: Create the Apps Script

1. **Open your Google Sheet**
   - Go to: https://docs.google.com/spreadsheets/d/1rRkDt7FXyLgYCLBGE12t5gFxnhXoKy2xgiLPrdr7bcA/edit

2. **Open Apps Script Editor**
   - Click on **Extensions** → **Apps Script**
   - This will open a new tab with the Apps Script editor

3. **Add the Code**
   - Delete any existing code in the editor
   - Copy and paste this code:

```javascript
function doGet(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Get headers from first row
  const headers = data[0];
  
  // Convert to array of objects
  const jsonData = data.slice(1).map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header] = row[index];
    });
    return obj;
  });
  
  // Return JSON with CORS headers
  const output = ContentService.createTextOutput(JSON.stringify(jsonData));
  output.setMimeType(ContentService.MimeType.JSON);
  
  return output;
}
```

4. **Save the Project**
   - Click the disk icon or press `Cmd+S` (Mac) / `Ctrl+S` (Windows)
   - Give it a name like "Frozen Assets API"

### Step 2: Deploy the Web App

1. **Start Deployment**
   - Click the **Deploy** button (top right)
   - Select **New deployment**

2. **Configure Deployment**
   - Click the gear icon ⚙️ next to "Select type"
   - Choose **Web app**
   - Set the following:
     - **Description**: Frozen Assets API (or any description)
     - **Execute as**: Me (your@email.com)
     - **Who has access**: **Anyone**
   
   ⚠️ **Important**: Make sure "Who has access" is set to **"Anyone"** so the website can access the data

3. **Authorize the Script**
   - Click **Deploy**
   - You'll need to authorize the script:
     - Click **Authorize access**
     - Choose your Google account
     - Click **Advanced** → **Go to [Project Name] (unsafe)**
     - Click **Allow**

4. **Copy the Web App URL**
   - After deployment, you'll see a **Web app URL**
   - It looks like: `https://script.google.com/macros/s/AKfycby.../exec`
   - **Copy this entire URL** - you'll need it in the next step

### Step 3: Configure Your Website

1. **Edit config.js**
   - Open the file: `docs/config.js`
   - Replace `'YOUR_APPS_SCRIPT_URL_HERE'` with your actual URL:

```javascript
const CONFIG = {
    // Your Google Apps Script Web App URL
    API_URL: 'https://script.google.com/macros/s/AKfycby.../exec',
    
    // Set to true to use fallback data while testing
    USE_FALLBACK: false
};
```

2. **Save and Test**
   - Save the file
   - Open `docs/index.html` in your browser
   - The documents from your spreadsheet should now load automatically!

## Testing

1. **Local Testing**
   - Open `docs/index.html` in your browser
   - Open the browser console (F12)
   - Check for any errors
   - Verify that documents are loading from your spreadsheet

2. **Verify Data**
   - Scroll to the "Database" section
   - Check that category counts are updating
   - Try searching and filtering documents

## Updating Data

- Any changes you make to your Google Sheet will automatically appear on the website
- Users will see the latest data when they refresh the page
- No need to redeploy the Apps Script unless you change the code

## Troubleshooting

### "Loading documents..." doesn't go away
- Check that you've set the correct API_URL in `config.js`
- Open browser console (F12) to see any error messages
- Verify the Apps Script is deployed with "Anyone" access

### "Unable to load documents" error
- Make sure the Apps Script deployment is set to "Anyone" for access
- Check that the Web App URL is correct
- Try redeploying the Apps Script

### Documents are empty or missing data
- Verify your spreadsheet has data in the correct format
- Make sure the first row contains the headers:
  - link, type, date, year, authority, title, short description
- Check that there are no empty rows at the top of your sheet

### Need to update the Apps Script?
1. Make changes in the Apps Script editor
2. Click **Deploy** → **Manage deployments**
3. Click the pencil icon ✏️ to edit
4. Change the version to "New version"
5. Click **Deploy**

## Alternative: Using Fallback Data

If you want to test without setting up the API immediately:

1. Edit `config.js`:
```javascript
const CONFIG = {
    API_URL: 'YOUR_APPS_SCRIPT_URL_HERE',
    USE_FALLBACK: true  // Set to true
};
```

2. The website will use sample data defined in `index.html`
3. Remember to set `USE_FALLBACK: false` once your API is ready

## Security Notes

- The Apps Script is read-only - it can't modify your spreadsheet
- Setting access to "Anyone" means the data is publicly accessible
- This is appropriate for public information
- Don't include sensitive data in your public spreadsheet

## Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify all steps in this guide
3. Make sure your spreadsheet is set to public or "Anyone with the link"
4. Try the fallback data mode to verify the website works

