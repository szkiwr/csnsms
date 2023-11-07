import re

def extract_username(url):
    pattern = r"(?:t\.me/|http://t\.me/)([\w\d]+[a-zA-Z])(?=\W|$)"
    match = re.search(pattern, url)
    if match:
        username = match.group(1)
        return username
    else:
        return None

def validate_username(username):
    pattern = r"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]"
    if re.match(pattern, username):
        return True
    else:
        return False
    
# Telegramのユーザネームを取得
def getTelegramUsername(source):
    # ユーザネームの抽出
    username = extract_username(source)
    # ユーザネームを検証し、ない場合は空文字列を返す
    if username:
        if(validate_username(username)):
            return username
    else:
        return ""
