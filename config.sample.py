# Configuration dictionaries

url_prefix = "" # some prefix for URLs, i.e. /api
				# it can be used when application is behind nginx proxy

webhooks = {
	# List of webhook's IDs (by Flask.route)
	"hook_name": "hook route", # some comment
	"autopay_orders": "hook route" #Receive AutoPay order payments information
}

tokens = {
	"tg-payments": "__token_here__", #Token for @some_bot
	"payments-chat": "__ID_here__", #Chat for sending payments info
	"admin_id": "__ID_here__", #Chat for sending errors info
	"discord-chat": "WebhookUrl", #Discord channel's webhook
	"bitrix-webhook": "WebhookUrl" #Bitrix webhook to send request to
}

# Not implemented yet
db_webhook_server = {
	"host": "host",
	"port": 3306,
	"database": "db_name",
	"login": "db_user",
	"password": "user_pass"
}
