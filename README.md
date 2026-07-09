# WeChall Ranking

Automatically collects daily snapshots of the WeChall global rankings, preserves historical data, and publishes an interactive website powered by GitHub Pages.

## Project Structure

```
wechall-ranking/
├── data/
│   └── history/           # Historical ranking snapshots
├── scripts/
│   └── fetch.py           # Main script for ranking collection
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

```bash
python scripts/fetch.py
```

## Features

- Daily snapshot collection of WeChall rankings
- Historical data preservation (stored in `data/history/`, currently in raw html format)
- Automated scheduling ready
- GitHub Pages integration

## Next Steps

1. Improve the data collection logic in `scripts/fetch.py` (add json format)
2. Test snapshot saving to `data/history/`
3. Configure automated scheduling (cron, GitHub Actions, etc.)
4. Create the website generation logic
5. Configure GitHub Pages deployment

![Daily Update](https://github.com/quangntenemy/wechall-ranking/actions/workflows/update.yml/badge.svg)
