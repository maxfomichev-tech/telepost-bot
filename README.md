# TelePost Bot

Automated weekly Telegram channel poster with scheduled publishing, retry logic, and optional inline buttons.

## Overview

This n8n workflow automatically publishes posts to a Telegram channel on a weekly schedule. Posts are managed through a built-in n8n Data Table — just add rows and the bot handles the rest.

### Features

- **Scheduled publishing**: Mon–Wed, every 15 minutes between 19:00–21:45 (Europe/Moscow)
- **Weekly recurrence**: 6-day cooldown prevents re-sending until next week
- **Retry logic**: Up to 3 attempts per post; after 3 failures marks as `error`
- **Inline buttons**: Optional URL buttons attached to messages
- **Timezone-aware**: All comparisons use Europe/Moscow timezone

## Prerequisites

- n8n instance (self-hosted or cloud)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Channel where bot is an admin

## Installation

### 1. Import Workflow

1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Select `weekly-telegram-poster.json`
4. Save the workflow

### 2. Configure Telegram Credentials

1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Telegram**
3. Enter your Bot Token
4. Save

### 3. Set Up Data Table

1. In n8n, go to **Data Tables** → **Create**
2. Name it `telegram_posts`
3. Add columns according to the [schema](docs/data-table.md)

### 4. Connect Credentials

1. Open the imported workflow
2. Click on **Telegram Send** node
3. Select your Telegram credential
4. Save

### 5. Activate

Toggle the workflow to **Active**. It will start checking for posts every 15 minutes.

## Usage

### Adding a Post

In the `telegram_posts` Data Table, add a new row:

| Field | Value | Example |
|-------|-------|---------|
| `channel_id` | Channel ID or @username | `-1003875893894` |
| `post_id` | Unique number | `1` |
| `day_of_week` | 0=Sun, 1=Mon, … 6=Sat | `1` (Monday) |
| `time` | Target time HH:MM | `20:45` |
| `post_text` | Message text (HTML ok) | `Hello <b>world</b>` |
| `button_text` | Button label (optional) | `Join us` |
| `button_url` | Button URL (optional) | `https://example.com` |

### How It Works

```
Schedule Trigger (every 15 min)
    ↓
Get Pending Posts (from Data Table)
    ↓
Filter Posts (match day + time ±15 min, skip if sent <6 days ago)
    ↓
Prepare Buttons (attach inline keyboard if provided)
    ↓
Telegram Send
    ↓
Send Success? → Mark Sent (record sent_at) or Handle Error (retry)
    ↓
Update Status (write back to Data Table)
```

### Post States

| Status | Meaning |
|--------|---------|
| `pending` | Ready to send |
| `error` | Failed 3 times, needs manual check |

## Files

| File | Description |
|------|-------------|
| `weekly-telegram-poster.json` | n8n workflow definition |
| `verify.py` | Script to check workflow execution status |
| `docs/data-table.md` | Data Table schema reference |

## Troubleshooting

### Post not sending

1. Check `day_of_week` matches current day
2. Check `time` is within ±15 min of current time
3. Check `status` is `pending`
4. Check `sent_at` is older than 6 days

### Button not appearing

1. Both `button_text` and `button_url` must be filled
2. `button_url` should start with `https://`

### Wrong timezone

The workflow uses `Europe/Moscow`. Server runs in UTC. All time comparisons are timezone-aware.

## License

MIT
