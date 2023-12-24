import requests
import json

url = 'https://api.loyalty.squidloyalty.app/auth/login?type=user'
headers = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'accept': 'application/json',
    'content-type': 'application/json',
    'origin': 'https://api.loyalty.squidloyalty.app',
    'pragma': 'no-cache',
    'referer': 'https://api.loyalty.squidloyalty.app',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ru-RU;q=0.6,ru;q=0.5,fr;q=0.4',
    'cache-control': 'no-cache',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'authority': 'api.loyalty.squidloyalty.app',
    'sec-fetch-site': 'same-origin',
}

data = {
    'email': 'saidi.ireland@gmail.com',
    'password': 'bastienRES13'
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
