"""stock updater to notion"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
STOCK_DATABASE_ID = os.getenv("STOCK_DATABASE_ID")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{STOCK_DATABASE_ID}/query"

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
        url = f"https://api.notion.com/v1/databases/{STOCK_DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def update_page(page_id: str, data: dict):
    """update page"""
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res


def main():
    current_prices = {}
    # List all stocks
    pages = get_pages()
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        name = props["Name"]["title"][0]["text"]["content"]
        stock_symbol = props["Stock Symbol"]["rich_text"][0]["text"]["content"]
        last_updated = props["Last Updated"]["date"]["start"]
        price = props["Price"]["number"]
        last_updated = datetime.fromisoformat(last_updated)

        current_prices.update(
            {
                page_id: {
                    "name": name,
                    "stock_symbol": stock_symbol,
                    "price": price,
                    "last_updated": last_updated,
                    "props": props,
                }
            }
        )

    # update these fields into notion
    for page_id, data in current_prices.items():
        # call stock api
        resp = requests.get(
            url="https://finnhub.io/api/v1/quote",
            params={"symbol": data.get("stock_symbol"), "token": FINNHUB_API_KEY},
        )
        if resp.status_code != 200:
            print("Could not fetch api data")
            continue
        resp_data = resp.json()
        new_price = resp_data.get("c")
        current_time = datetime.now().isoformat()

        new_props = data.get("props")
        new_props["Last Updated"]["date"]["start"] = current_time
        new_props["Price"]["number"] = new_price
        res = update_page(page_id=page_id, data=new_props)
        if res.status_code == 200:
            print(f"{data.get("name")} stock updated successfully")


if __name__ == "__main__":
    """Main function of the script."""
    from time import sleep

    # sample run for 5 times
    for _ in range(5):
        main()
        sleep(3)
