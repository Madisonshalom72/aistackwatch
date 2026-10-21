#!/usr/bin/env python3
"""Fetch end-of-day data for the AI StackWatch 31 public tickers from the
Yahoo Finance chart API (free, no key). Writes data/prices.json.
Never invents a value: failed tickers are recorded with status 'pending'."""
import json, time, urllib.request, datetime, sys, os

TICKERS = ["OKLO","GEV","VST","BE","CEG","NEE",
           "NVDA","AVGO","TSM","AMD","MU","ASML",
           "AMZN","MSFT","ORCL","EQIX","VRT","ANET",
           "GOOGL","META",
           "PLTR","SNOW","CRM","ADBE","NOW",
           "PATH","DUOL","SOUN","APP","RBLX","TWLO"]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "prices.json")

def fetch(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=3mo&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    out = {"source": "Yahoo Finance (chart API, end-of-day)",
           "fetched_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
           "tickers": {}}
    ok = 0
    for sym in TICKERS:
        try:
            d = fetch(sym)
            res = d["chart"]["result"][0]
            meta = res["meta"]
            ts = res["timestamp"]
            closes = res["indicators"]["quote"][0]["close"]
            rows = [(t, c) for t, c in zip(ts, closes) if c is not None]
            if len(rows) < 2:
                raise ValueError("insufficient rows")
            (t1, c1), (t0, c0) = rows[-2], rows[-1]
            dt = datetime.datetime.fromtimestamp(t0, datetime.timezone.utc)
            hist = [{"d": datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d"),
                     "c": round(c, 2)} for t, c in rows[-30:]]
            out["tickers"][sym] = {
                "status": "ok",
                "long_name": meta.get("longName", sym),
                "exchange": meta.get("fullExchangeName", ""),
                "currency": meta.get("currency", "USD"),
                "close": round(c0, 2),
                "prev_close": round(c1, 2),
                "change": round(c0 - c1, 2),
                "change_pct": round((c0 - c1) / c1 * 100, 2),
                "as_of": dt.strftime("%Y-%m-%d"),
                "day_high": meta.get("regularMarketDayHigh"),
                "day_low": meta.get("regularMarketDayLow"),
                "volume": meta.get("regularMarketVolume"),
                "wk52_high": meta.get("fiftyTwoWeekHigh"),
                "wk52_low": meta.get("fiftyTwoWeekLow"),
                "history": hist,
            }
            ok += 1
            print(f"OK   {sym:6s} {c0:>10.2f}  {(c0-c1)/c1*100:+.2f}%  {dt.strftime('%Y-%m-%d')}")
        except Exception as e:
            out["tickers"][sym] = {"status": "pending", "error": str(e)[:120]}
            print(f"FAIL {sym:6s} {e}")
        time.sleep(0.4)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n{ok}/{len(TICKERS)} tickers fetched -> {OUT}")

if __name__ == "__main__":
    main()
