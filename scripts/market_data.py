#!/usr/bin/env python3
"""Free/no-key market data helper for research notes.

This script avoids broker APIs, paid keys, cookies, and account credentials.
All endpoints are best-effort public sources and may be delayed, unavailable,
rate-limited, or unsuitable for commercial use.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from io import StringIO


USER_AGENT = "family-finance-copilot/1.0 research script"


def fetch_text(url: str, timeout: int = 15) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def stooq_quote(symbol: str) -> dict:
    normalized = symbol.lower()
    params = urllib.parse.urlencode({"s": normalized, "f": "sd2t2ohlcv", "h": "", "e": "csv"})
    url = f"https://stooq.com/q/l/?{params}"
    text = fetch_text(url)
    rows = list(csv.DictReader(StringIO(text)))
    if not rows:
        raise ValueError("Stooq returned no rows")
    row = rows[0]
    return {
        "source": "stooq",
        "symbol": symbol,
        "retrieved_at": now_iso(),
        "url": url,
        "data": row,
        "caveat": "Free public CSV; coverage and delay vary by market.",
    }


def stooq_history(symbol: str, interval: str) -> dict:
    normalized = symbol.lower()
    params = urllib.parse.urlencode({"s": normalized, "i": interval})
    url = f"https://stooq.com/q/d/l/?{params}"
    text = fetch_text(url)
    rows = list(csv.DictReader(StringIO(text)))
    if not rows:
        raise ValueError("Stooq returned no history rows")
    return {
        "source": "stooq",
        "symbol": symbol,
        "retrieved_at": now_iso(),
        "url": url,
        "rows": rows,
        "row_count": len(rows),
        "caveat": "Free public CSV; coverage and delay vary by market.",
    }


def yahoo_chart(symbol: str, range_: str, interval: str) -> dict:
    encoded = urllib.parse.quote(symbol)
    params = urllib.parse.urlencode({"range": range_, "interval": interval})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?{params}"
    payload = json.loads(fetch_text(url))
    chart = payload.get("chart", {})
    if chart.get("error"):
        raise ValueError(f"Yahoo chart error: {chart['error']}")
    result = (chart.get("result") or [None])[0]
    if not result:
        raise ValueError("Yahoo returned no chart result")
    meta = result.get("meta", {})
    timestamps = result.get("timestamp") or []
    quote = ((result.get("indicators") or {}).get("quote") or [{}])[0]
    rows = []
    for idx, ts in enumerate(timestamps):
        row = {"datetime": dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()}
        for field, values in quote.items():
            if idx < len(values):
                row[field] = values[idx]
        rows.append(row)
    return {
        "source": "yahoo_public_chart",
        "symbol": symbol,
        "retrieved_at": now_iso(),
        "url": url,
        "meta": meta,
        "rows": rows,
        "row_count": len(rows),
        "caveat": "Public Yahoo chart endpoint; intended for research/personal use and subject to Yahoo terms.",
    }


def eastmoney_fund(code: str) -> dict:
    if not re.fullmatch(r"\d{6}", code):
        raise ValueError("Eastmoney fund code should be 6 digits")
    url = f"https://fundgz.1234567.com.cn/js/{code}.js"
    text = fetch_text(url)
    match = re.search(r"jsonpgz\((.*)\);?", text)
    if not match:
        raise ValueError("Eastmoney returned an unexpected response")
    data = json.loads(match.group(1))
    return {
        "source": "eastmoney_public_fund_estimate",
        "code": code,
        "retrieved_at": now_iso(),
        "url": url,
        "data": data,
        "caveat": "Public web endpoint for fund estimate/NAV fields; best-effort and may change without notice.",
    }


def dump(payload: dict, output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch free/no-key market data as JSON.")
    sub = parser.add_subparsers(dest="command", required=True)

    quote = sub.add_parser("quote", help="Fetch latest quote.")
    quote.add_argument("--symbol", required=True)
    quote.add_argument("--source", choices=["stooq", "yahoo"], default="yahoo")
    quote.add_argument("--output")

    history = sub.add_parser("history", help="Fetch historical rows.")
    history.add_argument("--symbol", required=True)
    history.add_argument("--source", choices=["stooq", "yahoo"], default="yahoo")
    history.add_argument("--range", default="1mo", help="Yahoo range, e.g. 5d, 1mo, 1y.")
    history.add_argument("--interval", default="1d", help="Yahoo interval or Stooq interval d/w/m.")
    history.add_argument("--output")

    fund = sub.add_parser("fund", help="Fetch China public fund estimate/NAV fields.")
    fund.add_argument("--code", required=True)
    fund.add_argument("--source", choices=["eastmoney"], default="eastmoney")
    fund.add_argument("--output")

    args = parser.parse_args()

    try:
        if args.command == "quote":
            payload = stooq_quote(args.symbol) if args.source == "stooq" else yahoo_chart(args.symbol, "1d", "1d")
            dump(payload, args.output)
        elif args.command == "history":
            payload = (
                stooq_history(args.symbol, args.interval)
                if args.source == "stooq"
                else yahoo_chart(args.symbol, args.range, args.interval)
            )
            dump(payload, args.output)
        elif args.command == "fund":
            dump(eastmoney_fund(args.code), args.output)
    except Exception as exc:
        error = {
            "ok": False,
            "retrieved_at": now_iso(),
            "error": str(exc),
            "caveat": "Do not infer or fabricate current price when the source fails.",
        }
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
