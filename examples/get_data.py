#!/usr/bin/python

from atilgan.brooker import factory


def run():
    binance_brooker = factory.create_brooker('user_api_keys.json', factory.BINANCE)
    eth_price = binance_brooker.get_historical_price('ETHUSDT', 60, "1 Jan, 2021")
    print(eth_price.head())
