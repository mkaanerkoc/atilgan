from datetime import datetime
from dateutil import tz
from dateutil.relativedelta import relativedelta

import binance.exceptions
from binance.client import Client
from binance.exceptions import BinanceAPIException

import pandas as pd

import atilgan


def create_data_frame(price_data):
    datetime_list = [datetime.fromtimestamp(x[0] / 1000, tz=tz.UTC) for x in price_data]
    candlesticks = {"open": [float(x[1]) for x in price_data],
                    "high": [float(x[2]) for x in price_data],
                    "low": [float(x[3]) for x in price_data],
                    "close": [float(x[4]) for x in price_data],
                    "base_volume": [float(x[5]) for x in price_data],
                    "quote_volume": [float(x[7]) for x in price_data],
                    "trade_count": [float(x[8]) for x in price_data]}
    return pd.DataFrame(candlesticks, index=datetime_list)


def create_timestamp_for_days_before(param):
    now = datetime.now()
    days_before = now.replace(hour=0, minute=0, second=0, microsecond=0)
    days_before += relativedelta(days=-1 * param)
    days_before_timestamp = datetime.timestamp(days_before)
    return days_before_timestamp

class Binance(object):
    time_frame_key = {
        15: Client.KLINE_INTERVAL_15MINUTE,
        30: Client.KLINE_INTERVAL_30MINUTE,
        60: Client.KLINE_INTERVAL_1HOUR,
        120: Client.KLINE_INTERVAL_2HOUR,
        240: Client.KLINE_INTERVAL_4HOUR,
        360: Client.KLINE_INTERVAL_6HOUR,
        720: Client.KLINE_INTERVAL_12HOUR,
        1440: Client.KLINE_INTERVAL_1DAY
    }

    def __init__(self, client):
        self.__client = client
        self.__market_info = None

    def get_account_info(self):
        return self.__client.get_account()

    def get_avg_price(self, symbol_name):
        return_value = 0
        try:
            return_value = float(self.__client.get_avg_price(symbol=symbol_name)["price"])
        except BinanceAPIException:
            print(symbol_name)
            print(BinanceAPIException)
        return return_value

    def get_deposits(self, asset, day_count):
        response = self.__client.get_deposit_history(asset=asset)
        all_deposits = response["depositList"]
        day_before_ts = create_timestamp_for_days_before(day_count)
        return list(filter(lambda x: int(x["insertTime"]) / 1000 >= day_before_ts, all_deposits))

    def get_withdraws(self, asset, day_count):
        response = self.__client.get_withdraw_history(asset=asset)
        all_withdraws = response["withdrawList"]
        day_before_ts = create_timestamp_for_days_before(day_count)
        return list(filter(lambda x: int(x["applyTime"]) / 1000 >= day_before_ts, all_withdraws))

    def get_orders(self, symbol_name, limit=500):
        try:
            all_orders = self.__client.get_all_orders(symbol=symbol_name, limit=limit)
            return all_orders
        except binance.exceptions.BinanceAPIException as e:
            print('Exception thrown for symbol : {}'.format(symbol_name))
            print(e.message)

    def get_market_info(self):
        if self.__market_info is None:
            self.__market_info = self.__client.get_exchange_info()
        return self.__market_info

    def get_aggregated_trades(self, parity_name):
        return self.__client.get_aggregate_trades(symbol=parity_name)

    @atilgan.timeit
    def get_price(self, symbol, interval_in_minutes, limit):
        price_data = self.__client.get_klines(symbol=symbol,
                                              interval=self.time_frame_key[interval_in_minutes],
                                              limit=limit)

        return create_data_frame(price_data)

    @atilgan.timeit
    def get_historical_price(self, symbol, interval_in_minutes, start, end=''):
        if end:
            price_data = self.__client.get_historical_klines(symbol, self.time_frame_key[interval_in_minutes], start,
                                                             end)
        else:
            price_data = self.__client.get_historical_klines(symbol, self.time_frame_key[interval_in_minutes], start)

        return create_data_frame(price_data)


