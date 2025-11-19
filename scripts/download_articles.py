#!/usr/bin/env python3
"""
Download articles from the Frozen Assets database for knowledge base indexing.
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
import requests
from datetime import datetime

# Configuration
API_URL = "https://script.google.com/macros/s/AKfycbxfnWccVRWowozxaM0WRy5nb8Ao9Whx9404I9LUhVTyW_mgOTkS8MpwactacDnAjvR0/exec"
OUTPUT_DIR = "knowledge_base"
METADATA_FILE = "knowledge_base/metadata.json"

# Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def sanitize_filename(url, title):
    """Create a safe filename from URL and title."""
    # Try to use title first
    if title and title.strip():
        # Remove special characters, keep alphanumeric and spaces
        safe_name = re.sub(r'[^\w\s-]', '', title)
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        safe_name = safe_name[:100]  # Limit length
    else:
        # Fallback to URL-based naming
        parsed = urlparse(url)
        path = parsed.path
        safe_name = re.sub(r'[^\w\s-]', '_', path)
        safe_name = safe_name.strip('_')[:100]
    
    return safe_name

def get_file_extension(url, content_type, content):
    """Determine appropriate file extension."""
    # Check content type
    if content_type:
        if 'pdf' in content_type.lower():
            return '.pdf'
        elif 'html' in content_type.lower():
            return '.html'
        elif 'xml' in content_type.lower():
            return '.xml'
        elif 'json' in content_type.lower():
            return '.json'
        elif 'text' in content_type.lower():
            return '.txt'
    
    # Check URL extension
    parsed = urlparse(url)
    path = parsed.path.lower()
    if path.endswith('.pdf'):
        return '.pdf'
    elif path.endswith('.html') or path.endswith('.htm'):
        return '.html'
    elif path.endswith('.xml'):
        return '.xml'
    elif path.endswith('.json'):
        return '.json'
    elif path.endswith('.txt'):
        return '.txt'
    
    # Check content for PDF signature
    if content[:4] == b'%PDF':
        return '.pdf'
    
    # Default to html for web pages
    return '.html'

def download_article(doc, index):
    """Download a single article."""
    url = doc.get('link', '').strip()
    title = doc.get('title', '').strip()
    
    if not url:
        print(f"⚠️  Skipping document {index + 1}: No URL found")
        return None
    
    print(f"\n📥 [{index + 1}] Downloading: {title or url}")
    
    try:
        # Download with timeout
        response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Get content type
        content_type = response.headers.get('Content-Type', '')
        
        # Determine file extension
        extension = get_file_extension(url, content_type, response.content)
        
        # Create filename
        base_name = sanitize_filename(url, title)
        if not base_name:
            base_name = f"document_{index + 1}"
        
        filename = f"{base_name}{extension}"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Handle duplicate filenames
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{extension}"
            filepath = os.path.join(OUTPUT_DIR, filename)
            counter += 1
        
        # Save file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content)
        print(f"   ✅ Saved: {filename} ({file_size:,} bytes)")
        
        # Return metadata
        return {
            'filename': filename,
            'url': url,
            'title': title,
            'type': doc.get('type', ''),
            'date': doc.get('date', ''),
            'year': doc.get('year', ''),
            'authority': doc.get('authority', ''),
            'short_description': doc.get('short description', ''),
            'file_size': file_size,
            'content_type': content_type,
            'downloaded_at': datetime.now().isoformat(),
            'status': 'success'
        }
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed: {str(e)}")
        return {
            'filename': None,
            'url': url,
            'title': title,
            'type': doc.get('type', ''),
            'error': str(e),
            'status': 'failed',
            'downloaded_at': datetime.now().isoformat()
        }

def main():
    """Main function to download all articles."""
    print("=" * 70)
    print("📚 Frozen Assets Knowledge Base Downloader")
    print("=" * 70)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n📁 Output directory: {OUTPUT_DIR}/")
    
    # Fetch data from API
    print(f"\n🌐 Fetching data from API...")
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        documents = response.json()
        print(f"   ✅ Retrieved {len(documents)} documents")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed to fetch data: {e}")
        sys.exit(1)
    
    # Filter valid documents
    valid_docs = [
        doc for doc in documents
        if doc.get('title', '').strip() and 
           doc.get('link', '').strip() and 
           doc.get('type', '').strip()
    ]
    
    print(f"   ℹ️  {len(valid_docs)} valid documents to download")
    
    if len(valid_docs) == 0:
        print("\n⚠️  No valid documents found!")
        sys.exit(0)
    
    # Download all articles
    print(f"\n{'=' * 70}")
    print("Starting downloads...")
    print(f"{'=' * 70}")
    
    metadata_list = []
    success_count = 0
    failed_count = 0
    
    for i, doc in enumerate(valid_docs):
        result = download_article(doc, i)
        if result:
            metadata_list.append(result)
            if result.get('status') == 'success':
                success_count += 1
            else:
                failed_count += 1
    
    # Save metadata
    metadata = {
        'downloaded_at': datetime.now().isoformat(),
        'api_url': API_URL,
        'total_documents': len(valid_docs),
        'successful_downloads': success_count,
        'failed_downloads': failed_count,
        'documents': metadata_list
    }
    
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'=' * 70}")
    print("📊 Download Summary")
    print(f"{'=' * 70}")
    print(f"✅ Successfully downloaded: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📄 Metadata saved to: {METADATA_FILE}")
    print(f"\n✨ Done! Knowledge base ready in: {OUTPUT_DIR}/")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()

