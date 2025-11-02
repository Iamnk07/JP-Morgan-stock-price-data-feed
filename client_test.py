#!/usr/bin/env python3
import unittest
from client import getDataPoint, getRatio

class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36},
             'top_bid': {'price': 120.48, 'size': 109},
             'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4},
             'top_bid': {'price': 117.87, 'size': 81},
             'stock': 'DEF'}
        ]
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            self.assertEqual(price, (bid_price + ask_price) / 2)

    def test_getRatio_calculateRatio(self):
        self.assertEqual(getRatio(10, 2), 5)
        self.assertEqual(getRatio(2, 10), 0.2)
        self.assertIsNone(getRatio(10, 0))

if __name__ == '__main__':
    unittest.main()
