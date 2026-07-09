#!/usr/bin/env python3
"""Parse an archived WeChall ranking HTML file into structured JSON."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag


SOURCE_URL = "https://www.wechall.net/ranking"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Parse a WeChall ranking HTML archive")
    parser.add_argument("date", nargs="?", help="Date in YYYY-MM-DD format")
    return parser.parse_args()


def resolve_date(date_value: str | None) -> str:
    """Resolve the target date from the provided argument or today."""
    if date_value:
        return date_value
    return datetime.now().strftime("%Y-%m-%d")


def parse_numeric(value: str) -> int | float | None:
    """Convert a text value to int/float when possible."""
    text = value.strip()
    if not text:
        return None
    cleaned = text.replace(",", "")
    try:
        if "." in cleaned:
            return float(cleaned)
        return int(cleaned)
    except ValueError:
        return None


def normalize_text(value: str | None) -> str:
    """Trim and normalize text values."""
    if value is None:
        return ""
    return " ".join(value.split())


def parse_row(row: Tag, header_names: list[str]) -> dict[str, Any] | None:
    """Parse a single ranking row into a dictionary."""
    cells = [cell for cell in row.find_all(["td", "th"]) if cell.name in {"td", "th"}]
    if len(cells) < 3:
        return None

    row_data: dict[str, Any] = {}
    try:
        rank_value = normalize_text(cells[0].get_text(" ", strip=True))
        row_data["rank"] = int(rank_value) if rank_value.isdigit() else None
    except (ValueError, IndexError):
        return None

    for header_name, cell in zip(header_names, cells):
        if not header_name or header_name == "#":
            continue

        text = normalize_text(cell.get_text(" ", strip=True))
        if not text:
            continue

        if header_name == "Username":
            row_data["username"] = text
        elif header_name == "Sites":
            row_data["sites"] = parse_numeric(text)
        elif header_name == "Totalscore":
            row_data["totalscore"] = parse_numeric(text)
        else:
            parsed_value = parse_numeric(text)
            row_data[header_name] = parsed_value if parsed_value is not None else text

    username_cell = row.find("a")
    if username_cell is not None:
        username = normalize_text(username_cell.get_text(" ", strip=True))
        if username:
            row_data.setdefault("username", username)

    country_cell = row.find("img", class_="flag")
    if country_cell is not None:
        country_text = normalize_text(country_cell.get("title") or country_cell.get("alt") or "")
        if country_text:
            row_data.setdefault("country", country_text)

    return row_data


def find_ranking_table(soup: BeautifulSoup) -> Tag:
    """Locate the ranking table from the parsed HTML."""
    tables = soup.find_all("table")
    for table in tables:
        headers = [normalize_text(th.get_text(" ", strip=True)) for th in table.find_all("th")]
        if "Username" in headers and "Totalscore" in headers and "Sites" in headers:
            return table
    raise ValueError("Ranking table with Username, Sites, and Totalscore headers was not found")


def get_header_names(table: Tag) -> list[str]:
    """Extract the column names from the ranking table header row."""
    for row in table.find_all("tr"):
        headers = [normalize_text(th.get_text(" ", strip=True)) for th in row.find_all("th")]
        if "Username" in headers and "Sites" in headers and "Totalscore" in headers:
            return headers
    raise ValueError("Ranking table header row was not found")


def parse_html_file(html_path: Path, date_value: str) -> dict[str, Any]:
    """Parse a single archived HTML file into a structured JSON document."""
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    print(f"Reading HTML input from {html_path}")
    with html_path.open("r", encoding="utf-8") as handle:
        soup = BeautifulSoup(handle, "html.parser")

    table = find_ranking_table(soup)
    header_names = get_header_names(table)

    users: list[dict[str, Any]] = []
    for row in table.find_all("tr"):
        if row.find_all(["th"]) or not row.find_all(["td"]):
            continue
        try:
            parsed_row = parse_row(row, header_names)
        except Exception as exc:  # pragma: no cover - defensive branch
            print(f"Warning: failed to parse row: {exc}", file=sys.stderr)
            continue
        if parsed_row is not None:
            users.append(parsed_row)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    return {
        "date": date_value,
        "source": SOURCE_URL,
        "generated_at": generated_at,
        "users": users,
    }


def write_json(output_path: Path, data: dict[str, Any]) -> None:
    """Write parsed data to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    """CLI entry point."""
    args = parse_args()
    date_value = resolve_date(args.date)
    input_path = Path("data") / "history" / f"{date_value}.html"
    output_path = Path("data") / "history" / f"{date_value}.json"

    print(f"Parsing ranking data for {date_value}")
    try:
        parsed = parse_html_file(input_path, date_value)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - defensive branch
        print(f"Error: failed to parse HTML successfully: {exc}", file=sys.stderr)
        return 1

    write_json(output_path, parsed)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
