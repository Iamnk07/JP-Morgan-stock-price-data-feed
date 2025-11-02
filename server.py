#!/usr/bin/env python3
import random
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time

# -------------------------------------------------------------------
#  Utility functions
# -------------------------------------------------------------------

def getDataPoint(quote):
    """Produce the stock, bid_price, ask_price, and price (average)."""
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """Return ratio of price_a to price_b. Handle divide-by-zero."""
    if price_b == 0:
        return None
    return price_a / price_b


# -------------------------------------------------------------------
#  Fake data feed (for simulation)
# -------------------------------------------------------------------

quotes = [
    {
        "stock": "ABC",
        "top_bid": {"price": 120.48, "size": 100},
        "top_ask": {"price": 121.2, "size": 110}
    },
    {
        "stock": "DEF",
        "top_bid": {"price": 117.87, "size": 200},
        "top_ask": {"price": 119.02, "size": 210}
    }
]


# -------------------------------------------------------------------
#  HTTP Server
# -------------------------------------------------------------------

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run(routes, host='0.0.0.0', port=8080):
    """Runs a class as a server whose methods have been decorated with @route."""
    class RequestHandler(BaseHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            # Disable default logging
            return

        def do_GET(self):
            # Respond with random simulated quote data
            content = []
            for q in quotes:
                # Simulate slight price fluctuation
                q['top_bid']['price'] = round(q['top_bid']['price'] * (0.99 + 0.02 * random.random()), 2)
                q['top_ask']['price'] = round(q['top_ask']['price'] * (0.99 + 0.02 * random.random()), 2)
                stock, bid, ask, price = getDataPoint(q)
                content.append({
                    'stock': stock,
                    'top_bid': {'price': bid},
                    'top_ask': {'price': ask},
                    'price': price
                })

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(content).encode('utf-8'))

    server = ThreadedHTTPServer((host, port), RequestHandler)
    print(f"HTTP server started on port {port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()


# -------------------------------------------------------------------
#  Main entry point
# -------------------------------------------------------------------

if __name__ == '__main__':
    run(routes=None, port=8080)
