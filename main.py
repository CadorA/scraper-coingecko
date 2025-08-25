import json
import requests
import pandas as pd
import time
from pycoingecko import CoinGeckoAPI

COINGECKO_URL = 'https://www.coingecko.com/'


if __name__ == '__main__':
	print(f'Started running {__file__}')

	cg = CoinGeckoAPI()

	with open('config.json', 'r') as f:
		config = json.load(f)

	# get current price 
	print(f'Downloading: ids={config["ids"]}')
	current_data = cg.get_price(
		ids=config['ids'],
		vs_currencies='usd',
		include_market_cap='true',
		include_24hr_vol='true',
		include_24hr_change='true',
		include_last_updated_at='true'
	)

	# add symbol and name
	print(f'Downloading the mapping for: ids={config["ids"]}')
	coin_info = cg.get_coins_list()
	coin_info = [ci for ci in coin_info if ci['id'] in config['ids']]
	for ci in coin_info:
		current_data[ci['id']]['symbol'] = ci['symbol']
		current_data[ci['id']]['name'] = ci['name']

	# for k, v in current_data.items():		
	# 	print(k, v)

	# download the history for each
	for cid, ci in current_data.items():
		print(f'Fetching: {cid} ({ci["symbol"]})')
		history = cg.get_coin_market_chart_by_id(id=cid, vs_currency='usd', days=config['n_days'])
		df_coin = pd.DataFrame(history['prices'], columns=['time', 'price'])
		df_coin['time'] = pd.to_datetime(df_coin['time'], unit='ms', utc=True).dt.tz_convert('Europe/Amsterdam')
		print(df_coin.tail())

		time.sleep(1)


	# # get top 5 coins
	# market_data = cg.get_coins_markets(vs_currency='usd', per_page=5, page=1)
	# for coin in market_data:
	# 	print(f"{coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']} | Market Cap: ${coin['market_cap']}")