# WeChall Ranking

Automatically collects daily snapshots of the WeChall global rankings, preserves historical data, and publishes an interactive website powered by GitHub Pages.

## Current Status

The project now includes:

- a local archive workflow under `data/history/`
- a fetch script at `scripts/fetch.py` that fetches the ranking from <https://www.wechall.net/ranking>
- a parser script at `scripts/parse.py` that reads an archived HTML ranking page and writes JSON
- a lightweight regression test at `tests/test_parse.py`

## Project Structure

```text
wechall-ranking/
├── data/
│   └── history/
│       ├── 2026-07-09.html
│       └── 2026-07-09.json
├── scripts/
│   ├── fetch.py
│   └── parse.py
├── tests/
│   └── test_parse.py
├── requirements.txt
└── README.md
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

## Usage

Fetch the latest ranking data from WeChall:

```bash
python scripts/fetch.py
```

Parse the latest archived HTML file:

```bash
python scripts/parse.py
```

Parse a specific archive date:

```bash
python scripts/parse.py 2026-07-09
```

Run the regression test:

```bash
python -m unittest discover -s tests -p "test_parse.py"
```

## Features

- Daily snapshot collection of WeChall rankings
- Historical data preservation (stored in `data/history/`, in raw html and json format)

## Next Steps

1. Create a static website or dashboard from the generated JSON
2. Configure GitHub Pages deployment

![Daily Update](https://github.com/quangntenemy/wechall-ranking/actions/workflows/update.yml/badge.svg)
