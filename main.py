"""main file"""

from datetime import datetime, timezone

import requests
import os
from dotenv import load_dotenv


load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    import json

    with open("db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def create_page(data: dict):
    """create new page"""
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res


def update_page(page_id: str, data: dict):
    """update page"""
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)

    print(res.status_code)
    return res


def generate_create_page_data():
    name = "My Custom Coin"
    price = 6.66
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    return {
        "Name": {"title": [{"text": {"content": name}}]},
        "Price": {"number": price},
        "Updated at": {"date": {"start": published_date, "end": None}},
    }


if __name__ == "__main__":
    """Main function of the script."""

    # List pages on given database
    # get_pages()

    # Create page based on data provided in dict
    # create_page(data=generate_create_page_data())

    # Update particular page id
    # page_id_to_update = ""
    # update_page(page_id=page_id_to_update, data=generate_create_page_data())
