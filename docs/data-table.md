# Data Table Schema: telegram_posts

## Overview

The `telegram_posts` Data Table stores all posts that the bot manages. Each row represents one post that can be published on a specific day and time.

## Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `channel_id` | String | Yes | Telegram channel ID (e.g., `-1003875893894`) or @username (e.g., `@mychannel`) |
| `post_id` | Number | Yes | Unique identifier for the post |
| `day_of_week` | Number | Yes | Day of week: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday |
| `time` | String | Yes | Target time in `HH:MM` format (24-hour, e.g., `"20:45"`) |
| `post_text` | String | Yes | Message text. HTML formatting supported when `parse_mode` is HTML |
| `status` | String | Yes | Post status: `pending` (ready to send) or `error` (failed 3 times) |
| `sent_at` | String | No | ISO 8601 timestamp of last successful send (e.g., `"2026-06-18T11:07:17.627Z"`) |
| `retry_count` | Number | No | Number of failed send attempts (resets to 0 on success) |
| `button_text` | String | No | Inline button label. If empty, no button is attached |
| `button_url` | String | No | Inline button URL. Must start with `https://`. If empty, no button is attached |

## Auto-generated Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | Number | Auto-increment row ID |
| `createdAt` | String | ISO 8601 timestamp of row creation |
| `updatedAt` | String | ISO 8601 timestamp of last update |

