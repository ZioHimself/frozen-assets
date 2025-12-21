[![Website Uptime Monitor](https://github.com/ZioHimself/frozen-assets/actions/workflows/uptime-monitor.yml/badge.svg)](https://github.com/ZioHimself/frozen-assets/actions/workflows/uptime-monitor.yml)

# Ukraine Reconstruction Fund

A comprehensive resource tracking the international effort to utilize frozen Russian assets for Ukraine's reconstruction.

## Overview

This platform serves two primary functions:

1. **Interactive Presentation** – Visual infographics and data on frozen Russian assets and reconstruction funding
2. **Document Database** – Aggregated repository of legal, financial, political, and expert documents related to asset seizure and utilization

## Features

- Real-time search and filtering across document categories
- Timeline of key legislative and policy milestones
- Regional asset distribution breakdowns
- Categorized resource library (legal, financial, political, opinion, research, media)

## Technology

Static HTML/CSS/JavaScript website. No build process required.

### Data Source

The document database is dynamically loaded from a Google Sheets spreadsheet via Google Apps Script API. This allows for easy content management without rebuilding the website.

**Setup Required**: To connect your own Google Sheets data, follow the [Setup Guide](docs/SETUP.md).

## Usage

The platform is currently available at: **https://ziohimself.github.io/frozen-assets/**

For local development:
1. Clone this repository
2. Follow the [Setup Guide](docs/SETUP.md) to configure your Google Sheets API
3. Open `docs/index.html` in a web browser

*Note: Shortly, this will be hosted on a dedicated domain.*

## Contributing

Document submissions and corrections welcome. Please ensure all references include proper citations and dates.

## License

Content aggregated from public sources. See individual documents for their respective licenses.

---

*This is an independent information resource and is not affiliated with any government entity.*
