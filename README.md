# 🛒 Stock Alerts (Shopify)

An automated serverless bot that monitors Shopify stores for restocks. It runs automatically in the background using GitHub Actions and sends instant push notifications to your phone via Telegram.

## ✨ Features

* **Zero-Infrastructure:** Runs 100% free on GitHub Actions. No servers to maintain or pay for.

* **Highly Reliable:** Bypasses fragile HTML web scraping by querying Shopify's native backend `.js` product endpoints directly.

* **Instant Alerts:** Delivers immediate restock notifications to your phone or desktop via Telegram.

* **Fully Customizable:** Easily add new products, change target variants, or adjust the checking frequency.

## 🚀 Setup Instructions

### 1. Create Your Telegram Bot

To receive messages, you need to set up a free Telegram bot and get your unique Chat ID.

1. Open Telegram and search for **@BotFather**.

2. Send `/newbot`, follow the prompts to name it, and copy the **HTTP API Token** provided.

3. Search for **@userinfobot** in Telegram and click "Start" to reveal your numeric **Chat ID**.

4. **CRITICAL:** Search for your newly created bot's username in Telegram and click **Start**. The bot cannot message you unless you initiate the conversation first.

### 2. Configure GitHub Secrets

Keep your keys safe! Never hardcode your Telegram credentials into the script.

1. Go to your repository's **Settings** tab.

2. Navigate to **Secrets and variables > Actions**.

3. Click **New repository secret** and add the following two secrets:

   * Name: `TELEGRAM_TOKEN` | Value: *(Paste your API Token from step 1)*

   * Name: `TELEGRAM_CHAT_ID` | Value: *(Paste your numeric Chat ID from step 1)*

### 3. Add the Code

Ensure your repository has the following file structure:

* `alert.py` - The main Python checking script.

* `.github/workflows/checker.yml` - The GitHub Actions automation file.

## ⚙️ Configuration

### Adding or Changing Products

To monitor a different product, open `alert.py` and modify the `PRODUCTS` dictionary list.
For any Shopify store, just append `.js` to the standard product URL to view its API data and locate the specific `variant_id` you want to track.

```
PRODUCTS = [
    {
        "name": "Perfume Name",
        "api_url": "https://store.com/products/item.js",
        "buy_url": "https://store.com/products/item?variant=123456789",
        "variant_id": 123456789
    }
]

```

### Changing the Checking Schedule

By default, the script checks every 15 minutes. To change this, edit the `cron` schedule in `.github/workflows/checker.yml`:

```
on:
  schedule:
    - cron: '*/15 * * * *' # Checks every 15 minutes
    # - cron: '0 * * * *'  # Checks once every hour
    # - cron: '*/30 * * * *' # Checks every 30 minutes

```

## 📝 Important Notes

* **Persistent Alerts:** Because this script does not use a database to store history, if an item rests in stock for 3 hours, you will receive a notification *every 15 minutes* until it sells out again.

* **GitHub Actions Inactivity:** If you do not push any new code to this repository for 60 days, GitHub will temporarily pause scheduled workflows. You will receive an email warning you, and you can resume it with a single click in the Actions tab.

* **Testing:** You can manually trigger a check at any time by going to the **Actions** tab, selecting the workflow, and clicking **Run workflow**. If you temporarily alter the code to test Telegram delivery (`if variant.get("available") == False:`), **always remember to change it back to `True`**!
