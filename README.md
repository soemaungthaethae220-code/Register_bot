# Telegram Device ID Registration Bot

A simple Telegram bot built with Python (`python-telegram-bot`) to register and forward User IDs and Device IDs to an admin.

## Features
- Handles `/start [DeviceID]` commands.
- Automatically forwards registration details to the designated Admin Chat ID.
- Runs via Long Polling for reliable connection.

## Usage
1. Open the bot in Telegram.
2. Send the command with your device ID:
   `/start YOUR_DEVICE_ID`
