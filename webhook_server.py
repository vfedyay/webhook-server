from flask import Flask
from flask import request, jsonify
import json
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

import config
import telegram_tools.webhook as tg_wh
#import bitrix.api
from fast_bitrix24 import Bitrix

tg_inform = tg_wh.Webhook(config.tokens["tg-payments"], config.tokens["payments-chat"])
tg_admin = tg_wh.Webhook(config.tokens["tg-payments"], config.tokens["admin_id"])
#b24 = bitrix.api.Create(config.tokens["bitrix-webhook"])
b24 = Bitrix(config.tokens["bitrix-webhook"])

app = Flask(__name__)
app.config["DEBUG"] = False

@app.route("/")
def index():
	return "It works!"

@app.route(config.url_prefix + "/")
def base_index():
	return "It works!"

@app.route(config.url_prefix + "/" + config.webhooks["autopay_orders"], methods=['POST']) # ['GET', 'POST']
def autopay_order_payed():
	## recieved message from autopay is forming to text message for sending to Telegram chat
	## for debugging this message also will be writen to requests.log
	## in case of parsing error (i.e. requesting nonexistent field) full incoming message
	## will be dumped to log file and additionally will be sent to Telegram to admin
	
	## also lead must be created in Bitrix CRM

	# get message from autopay in JSON
	hook_req = request.json
	f = open("requests.log", "a")
	now = datetime.now()
	d1 = now.strftime("%Y-%m-d %H:%M:%S")
	f.write("\n\n********\n"+d1+"\n")
	message = "Получена оплата на Autopay:\n"
	try:
		message += "order id " + str(hook_req['order_id'])+"\n"
		message += "сумма " + str(hook_req['credentials']['amount']) + " " + hook_req['credentials']['currency'] + "\n"
		message += "товар " + hook_req['basket'][0]['good_name'] + "\n"
		message += "id товара " + str(hook_req['basket'][0]['good_id']) + "\n\n"
		message += "имя " + hook_req['customer']['given_name'] + "\n"
		message += "phone " + hook_req['customer']['phone'] + "\n"
		message += "e-mail " + hook_req['customer']['email'] + "\n"
		message += "IP " + str(hook_req['credentials']['ip'])
	except:
		message += "!!! Error parsing request !!!\n"
		tg_admin.send_message(message)
		tg_admin.send_message(hook_req)
	
	f.write(message + "\n")
	json.dump(hook_req, f)
	f.close()

	#Send information to Telegram
	tg_inform.send_message(message)

	# prepare request for creating lead in BitrixCRM
	# ToDo - goods information to lead - find good by ID in BitrixCRM and create lead with good attached
	# ToDo - move this functionality to bitrix/api.py
	tasks = [
		{
			'fields': {
				'TITLE': 'Получена оплата с Autopay',
				'NAME': hook_req['customer']['given_name'],
				'STATUS_ID': 'NEW',
				'PHONE': hook_req['customer']['phone'],
				'EMAIL': hook_req['customer']['email'],
				'WEB': str(hook_req['credentials']['ip']),
				'COMMENTS': hook_req['basket'][0]['good_name'] + ", id товара " + str(hook_req['basket'][0]['good_id'])
			},
			'params': { 'REGISTER_SONET_EVENT': 'N' } # do not publish lead adding in Bitrix news feed
		}
	]

	method = 'crm.lead.add'
	b24.call(method, tasks)

	return ""
	

if __name__ == "__main__":
	app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
	app.run(host="127.0.0.1", port=8888)
