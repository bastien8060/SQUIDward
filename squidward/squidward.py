import requests
import json
import os

class RequestClient:
    def __init__(self, base_url=None):
        self.base_url = base_url if base_url else 'https://api.loyalty.squidloyalty.app'
        self.token = None
        self.refresh_token = None

    def get_authorization(self, authed):
        if not authed:
            return {}
        
        if not self.token:
            raise Exception("No JWT Token available to pass auth")
        
        return {
            'Authorization': f'Bearer {self.token}'
        }      

    def updateTokens(self, token=None, refresh_token=None):
        if token:
            self.token = token

        if refresh_token:
            self.refresh_token = refresh_token

    def fetch(self, resource, authed=False, headers=None, params=None, payload=None, method="GET"):
        url = f"{self.base_url}{resource}"
        auth = self.get_authorization(authed)
        default_headers = {
            'accept': 'application/json',
            'content-type': 'application/json',  # Update this line
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
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

        if payload:
            payload = json.dumps(payload)

        if auth:
            default_headers.update(auth)

        if headers:
            default_headers.update(headers)

        if method == "GET":
            return requests.get(url, headers=default_headers, params=params)
        elif method == "POST":
            return requests.post(url, headers=default_headers, data=payload, params=params)  # Update this line
        else: 
            raise ValueError(f"{method} HTTP method is not available")


class DataStore:
    def __init__(self, path='~/.config/squidward/store.json'):
        os.makedirs(os.path.dirname(os.path.expanduser(path)), exist_ok=True)
        self.file = os.path.expanduser(path)
        self.store = {}

        self.syncInit()

    def __ensure_dir(self, path):
        abs_path = os.path.expanduser(path)
        directory = os.path.dirname(abs_path)
        os.makedirs(directory, exist_ok=True)

    def set(self, key, value):
        self.store[key] = value
        self.syncWrite()
        return value

    def get(self, key, default):
        return self.store.get(key, default)
    
    def syncWrite(self):
        with open(self.file, 'w') as f:
            f.write(json.dumps(self.store))

    def syncInit(self):
        f = open(self.file, 'r')
        try:
            self.store = json.loads(f.read())
        except Exception as e:
            self.store = {}
        finally:
            f.close()

class Client:
    def __init__(self):
        self.server = RequestClient()
        self.store = DataStore()
        self.authPresent = False

        authData = self.store.get('authData', None)
        if authData:
            self.authPresent = True
            self.server.updateTokens(authData.get('token'), authData.get('refreshToken'))

    def login(self, email, password):
        response = self.server.fetch("/auth/login", payload = {
            'email': email,
            'password': password
        }, method="POST", params={"type": "user"})
        
        if response.status_code == 200:
            resp = response.json()

            self.store.set('authData', resp)
            self.server.updateTokens(resp.get('token'), resp.get('refreshToken'))

            return resp
        else:
            return response.text
        
    def getActivity(self):
        return self.server.fetch("/account/activity", headers={
            "Authorization": "Bearer " + self.server.token
        }, method="GET").json()
    
    def getWallet(self, schemeID=None):
        url = f"/wallet/${schemeID}" if schemeID else "/wallet"

        return self.server.fetch(url, headers={
            "Authorization": "Bearer " + self.server.token
        }, method="GET").json()
    
    def refreshToken(self):
        response = self.server.fetch("/auth/refresh?type=user", payload={
            'refreshToken': self.refreshToken
        }, method='GET').json()

        if response:
            print(response)

    def checkTag(self, tagId):
        return self.server.fetch(f"/tags/{tagId}/?type=live", headers={
            "Authorization": "Bearer " + self.server.token
        }, method="GET").json()




