import requests
import json
from typing import Any
import re

STATS_URL = "https://api.warframe.market/v1/items/{slug}/statistics"
ORDERS_URL = "https://api.warframe.market/v2/orders/item/{slug}/top"

testslug1 = "Okina Prime Handle"
testslug2 = "test"
testslug3 = "test"


def slugify (text: str) -> str:
    return re.sub(r'\W+', '_', text.lower()).strip('_')

def get_stats (fslug: str) -> dict[str, Any]:
    url = STATS_URL.format(slug = fslug)
    r = requests.get(url, timeout= 10)
    r.raise_for_status()
    payload = r.json()
    return payload.get("payload", {}).get("statistics_closed", {})

def get_orders (fslug: str) -> list[dict[str, Any]]:
    url = ORDERS_URL.format(slug = fslug)
    r = requests.get(url, timeout= 10)
    r.raise_for_status()
    payload = r.json()
    return payload.get("data", {})

def extract_recent_listings (orders: dict) -> list[int]:
    sell_orders = orders.get("sell", {})
    return [order["platinum"] for order in sell_orders] 

def extract_stats (stats: dict):
    days = stats.get("90days", [])
    if not days:
        return []
    
    recent = days[-10:]
    return [(entry["volume"], entry["avg_price"]) for entry in recent]

def calc_stats (orders: list[tuple]) -> dict:
    if not orders:
        return {}
    
    output = {}

    #latest entry
    output["rec_vol"] = orders[-1][0]
    output["rec_avg"] = orders[-1][1]

    #avg of latest 10 days / entries
    recent_avgs = [entry[1] for entry in orders]
    output["ten_day_avg"] = sum(recent_avgs) / len(recent_avgs)
    return output

def calc_listings (listings: list[int]) -> dict:
    output = {}
    output["min"] = listings[0]
    output["sell_orders_avg"] = sum(listings) / len(listings)
    return output

# def open_db():
    # pass

# def db_upsert():
#     pass

def driver(unformat_name: str):
    # use unformat name as dict key or find from unformat name
    # slugify, calc, upsert to database
    pass

if __name__ == "__main__":
    formatted = slugify(testslug1)

    orders = get_orders(formatted)
    stats = get_stats(formatted)

    orders_processed = extract_recent_listings(orders)
    stats_processed = extract_stats(stats)

    print(calc_listings(orders_processed))
    print(calc_stats(stats_processed))

