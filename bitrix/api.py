# API for Bitrix through  webhooks
# 
# using fast-bitrix24 
# documentation with examples are at
# https://pypi.org/project/fast-bitrix24/

from fast_bitrix24 import Bitrix

#import requests

class Create:
	def __init__(self, webhook_url: str = None):
		self.webhook_url = webhook_url


