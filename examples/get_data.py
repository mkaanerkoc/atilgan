#!/usr/bin/python

from atilgan.brooker import factory
from atilgan.utils import timeit

import pandas as pd


@timeit.timeit
def run():
    symbol_name = 'ETHUSDT'
    binance_brooker = factory.create_brooker('user_api_keys.json', factory.BINANCE)
    eth_price = binance_brooker.get_historical_price(symbol_name, 60, "2020/01/01")
    eth_price = eth_price.tz_convert('UTC')  # https://github.com/pandas-dev/pandas/issues/25423
    eth_price.to_parquet(f'data/{symbol_name}.parquet', compression='GZIP', engine='fastparquet')


    load_from_pq = pd.read_parquet(f'data/{symbol_name}.parquet', engine='fastparquet')
    print(load_from_pq.head())
    print(load_from_pq.tail())
