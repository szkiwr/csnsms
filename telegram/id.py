import configparser
from telethon import TelegramClient
import re
import time

config = configparser.ConfigParser()
config.read('config/config.ini')
telegram_api_id = config.get('telegram', 'api_id')
telegram_api_key = config.get('telegram', 'api_key')
BOT_TOKEN = config.get('telegram', 'bot_token')

def extract_seconds(text):
    pattern = r"(\d+) seconds"
    match = re.search(pattern, text)
    if match:
        seconds = int(match.group(1))
        return seconds
    else:
        return None

# need to fix
async def getTelegramID(username):
    client = TelegramClient("Session", telegram_api_id, telegram_api_key)

    await client.start(bot_token=BOT_TOKEN)

    try:
        peer = await client.get_entity(username)
    # 存在しない場合
    except ValueError:
        return ""
    # その他のエラーで取得制限が来た時
    except Exception as e:
        if "seconds" in str(e):
            time.sleep(int(extract_seconds(str(e))))

    await client.disconnect()
    
    return peer.id