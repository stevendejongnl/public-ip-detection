import sys
import os
import requests
import logging


CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def detect_public_ip():
    import requests

    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_info = response.json()
        return ip_info['ip']
    except requests.RequestException as e:
        logging.info(f"Error fetching public IP: {e}")
        return None

def write_ip_to_file(ip, filename='public_ip.txt'):
    try:
        with open(filename, 'w') as file:
            file.write(ip)
    except IOError as e:
        logging.info(f"Error writing IP to file: {e}")

def detect_ip_change(filename='public_ip.txt'):
    try:
        with open(filename, 'r') as file:
            old_ip = file.read().strip()
        return old_ip
    except FileNotFoundError:
        return None

def notify_telegram_on_ip_change(ip, chat_id, token):
    message = f"Public IP has changed to: {ip}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.info(f"Error sending notification: {e}")

def main():
    logging.info("Starting public IP change detection...")
    if not CHAT_ID or not TOKEN:
        logging.info("Telegram credentials are not set in environment variables.")
        return

    public_ip = detect_public_ip()
    if not public_ip:
        logging.info("Could not detect public IP.")
        return
    old_ip = detect_ip_change()
    if old_ip == public_ip:
        logging.info("Public IP has not changed.")
        return

    write_ip_to_file(public_ip)

    logging.info(f"Public IP has changed to: {public_ip}")
    notify_telegram_on_ip_change(public_ip, CHAT_ID, TOKEN)


if __name__ == "__main__":
    main()
