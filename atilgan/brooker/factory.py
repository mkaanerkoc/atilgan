import json
from binance.client import Client

import Binance

# Add more exchanges when needed
BINANCE = 1


def create_brooker(config_file_path, brooker_type):
    if brooker_type == BINANCE:
        with open(config_file_path) as f:
            data = json.load(f)
            api_key = data["api_key"]
            api_secret = data["api_secret"]
            brooker = Binance.Binance(Client(api_key, api_secret))
            return brooker
    else:
        raise Exception("Unsupported Brooker Type")
