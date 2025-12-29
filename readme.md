# UpBack

**Backups made reliable, simple and developer-focused**

A lightweight, self-hosted backup service designed for developers who want predictable, automatable and restore-first backups without fighting their infrastructure.
This service scans tracked folders, performs secure backups, and exposes clear status and control primitives - no hidden magic, no vendor lock-in.

## ✨ Features

- 🔍 Tracked folders
Define exactly which directories are backed up  nothing more, nothing less.

- 🔁 Automated backups
Schedule backups using cron-style configuration.

- 📊 Observable
Clear backup state, progress, and failure reporting.

- 🧑‍💻 Developer-focused
Simple configuration, predictable behavior, and explicit control.
Clean and clear API.

```text
┌──────────────────┐
│ Tracked Directory│
│  /src/postgres   │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│ Scan & Collect   │
│ files + metadata │
└─────────┬────────┘
          │
          ▼
┌──────────────────────────┐
│ Timestamped ZIP Builder  │
│ postgres_2025-03-21.zip  │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────┐
│ Backup Storage   │
│ disk / NAS / S3  │
└──────────────────┘
```