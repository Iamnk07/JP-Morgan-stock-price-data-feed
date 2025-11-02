#!/usr/bin/env python3
import json
import urllib.request

def getDataPoint(quote):
    """Extracts stock name, bid price, ask price, and average price."""
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price

def getRatio(price_a, price_b):
    """Returns ratio of price_a to price_b. Returns None if price_b is 0."""
    if price_b == 0:
        return None
    return price_a / price_b

# -------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------
QUERY = "http://localhost:8080/query?id=1"

def main():
    for _ in range(500):
        with urllib.request.urlopen(QUERY) as response:
            quotes = json.loads(response.read().decode('utf-8'))

        prices = {}
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            prices[stock] = price
            print(f"Quoted {stock} at (bid: {bid_price}, ask: {ask_price}, price: {price})")

        print(f"Ratio {getRatio(prices['ABC'], prices['DEF'])}\n")

if __name__ == "__main__":
    main()
