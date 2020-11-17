from config import TOKEN, NGROK_URL
import requests

TELEGRAM_BASE = 'https://api.telegram.org'

TELEGRAM_INIT_WEBHOOK_URL = f'{TELEGRAM_BASE}/bot{TOKEN}/setWebhook?url={NGROK_URL}'

TELEGRAM_SEND_WEBHOOK_URL = '{}/bot{}/sendMessage?'.format(TELEGRAM_BASE, TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)