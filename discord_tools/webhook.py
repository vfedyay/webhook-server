# Sending messages to Discord channel
# using webhook created for channel

import requests

class Webhook:
	def __init__(self, channel_webhook: str = None):
		self.channel_webhook = channel_webhook

	def send_message(self, name_from: str = None, message: str = None):
		# compose message
		payload = {
			"username": name_from,
			"content": message
		}
		#send
		resp = requests.post(self.channel_webhook, json = payload)
		return resp.text
