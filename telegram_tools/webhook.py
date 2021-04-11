# Sending messages to Telegram
# using webhook
# to chat or directly to user (depends on chat ID)

import requests

class Webhook: #(token: str=None)
	def __init__(self, token: str = None, chat_id: str = None):
		self.token = token
		self.chat_id = chat_id

	def send_message(self, message: str = None):
		url = 'https://api.telegram.org/bot' + self.token + '/sendMessage'
		payload = {
			"chat_id": self.chat_id,
			"text": message,
			"disable_web_page_preview": "true",
			"disable_notification": "false"
		}
		#send
		resp = requests.post(url, json = payload)
		return resp.text
