# webhook-server

Сервер для обробки вебхуків

Наведена реалізація:
* приймає вебхуки від системи Autopay про вдалі платежі у системі
* провідомляє інформацію у Telegram або Discord
* створює лід у Бітрікс CRM через вхідний вебхук

для роботи потрібні:
* pip install flask
* pip install requests
* pip install fast_bitrix24

для встановлення:
* створити файл **config.py** за зразком **config.sample.py**
