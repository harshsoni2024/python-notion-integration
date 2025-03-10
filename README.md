# python-notion-integration

Notion API Integration with Python

🚀 Overview

This repository provides a seamless Python integration with Notion, enabling interaction between a Notion workspace, a Notion database, and an external API. With this integration, you can fetch, modify, and sync data between Notion and external services effortlessly.

🔗 Workflow

`Notion Workspace <-> Notion Database <-> Python Integration <-> External API`

Here's an example working of this repo:
https://www.loom.com/share/f1b1d62d3c05444abfe219007f1189f0?sid=c74e48bc-a538-4273-bd66-91b803409ec8

✨ Features

✅ Read and write data to Notion databases

✅ Automate data syncing between Notion and external APIs

✅ Fetch data from an external API and push it to Notion

✅ Use Python to manipulate and process Notion database entries

✅ Easily extendable and customizable

📦 Installation
```pip install -r requirements.txt```

🔧 Usage

Setup Notion API

1. Create a Notion integration from Notion Developers

2. Share your Notion workspace with the integration

3. Get your NOTION_API_KEY

4. Configure Environment Variables
   - export NOTION_API_KEY="your_notion_secret"
   - export NOTION_DATABASE_ID="your_database_id"
   - export EXTERNAL_API_KEY="your_external_api_key"

Run the script
- `python main.py`
