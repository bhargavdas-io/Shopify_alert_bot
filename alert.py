import os

import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_SECRETS")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_ID")

# The .js endpoints bypass HTML and fetch direct inventory data
PRODUCTS = [
    {
        "name": "Alexander",
        "api_url": "https://menworks.in/products/alexander.js",
        "buy_url": "https://menworks.in/collections/perfume/products/alexander?variant=51640784716096",
        "variant_id": 51640784716096
    },
    {
        "name": "After Dark",
        "api_url": "https://menworks.in/products/after-dark.js",
        "buy_url": "https://menworks.in/products/after-dark?variant=51141407768896",
        "variant_id": 51141407768896
    },
    {
        "name": "Elixir",
        "api_url": "https://menworks.in/products/elixir.js",
        "buy_url": "https://menworks.in/collections/perfume/products/elixir?variant=50652943384896",
        "variant_id": 50652943384896
    }
]

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def check_stock():
    in_stock_items = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    for item in PRODUCTS:
        try:
            response = requests.get(item["api_url"], headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                variants = data.get("variants", [])

                # Find your specific variant ID in the data
                for variant in variants:
                    if variant.get("id") == item["variant_id"]:
                        if variant.get("available") == False:
                            in_stock_items.append(f"✅ <b>{item['name']}</b> is IN STOCK!\n<a href='{item['buy_url']}'>Buy Here</a>")
                        break
        except Exception as e:
            print(f"Failed to check {item['name']}: {e}")

    # Only message you if something is actually in stock
    if in_stock_items:
        final_message = "🚨 <b>Menworks Restock Alert</b> 🚨\n\n" + "\n\n".join(in_stock_items)
        send_telegram_alert(final_message)
        print("Alert sent via Telegram.")
    else:
        print("Nothing is in stock right now.")

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram credentials are not set.")
    else:
        check_stock()
