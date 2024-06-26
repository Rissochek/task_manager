import requests
import json
import base64
import uuid
import urllib3

from todo.config import settings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client_id = settings.client_id
secret = settings.secret.get_secret_value()
auth = settings.auth.get_secret_value()

credentials = f"{client_id}:{secret}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    payload = {
        'scope': scope
    }

    try:
        return requests.post(url, headers=headers, data=payload, verify=False)
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


response = get_token(auth)
if response != 1:
    giga_token = response.json()['access_token']


def get_chat_completion(auth_token, user_message):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 50,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    try:
        return requests.request("POST", url, headers=headers, data=payload, verify=False)
    except requests.RequestException as e:
        print(f"Произошла ошибка: {str(e)}")
        return -1
