#!/usr/bin/env python3
"""
Run this once after deploying to register your webhook with Telegram.
Usage: python setup_webhook.py
"""

import os
import httpx

BOT_TOKEN      = os.environ["BOT_TOKEN"]
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
WEBHOOK_URL    = os.environ["WEBHOOK_URL"]  # e.g. https://mangoi.in/webhook

def main():
    api = f"https://api.telegram.org/bot{BOT_TOKEN}"

    # Delete any existing webhook first
    r = httpx.post(f"{api}/deleteWebhook")
    print("Delete old webhook:", r.json())

    # Set new webhook
    r = httpx.post(f"{api}/setWebhook", json={
        "url": f"{WEBHOOK_URL}",
        "secret_token": WEBHOOK_SECRET,
        "allowed_updates": ["message", "channel_post"],
        "drop_pending_updates": True   # ignore queued old messages on startup
    })
    result = r.json()
    print("Set webhook:", result)

    if result.get("ok"):
        print("\n✅ Webhook registered successfully!")
        print(f"   URL : {WEBHOOK_URL}")
    else:
        print("\n❌ Failed:", result.get("description"))

    # Show current webhook info
    r = httpx.get(f"{api}/getWebhookInfo")
    print("\nWebhook info:", r.json())

if __name__ == "__main__":
    main()
