from datetime import datetime
from pathlib import Path

import requests

URL = "https://www.wechall.net/ranking"

# Create data/history if it doesn't exist
output_dir = Path("data") / "history"
output_dir.mkdir(parents=True, exist_ok=True)

# Output filename: YYYY-MM-DD.html
today = datetime.now().strftime("%Y-%m-%d")
output_file = output_dir / f"{today}.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

print(f"Downloading {URL}...")

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

output_file.write_text(response.text, encoding="utf-8")

print(f"Saved to {output_file}")
