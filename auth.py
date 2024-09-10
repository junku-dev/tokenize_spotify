import base64, urllib
from requests import post
from dotenv import load_dotenv

redirect:str = "http://localhost:5432/usercode"

def encode_auth(id:str, secret:str) -> str:
    auth_string:str = id+ ":" + secret
    auth_bytes:str = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')
    return auth_base64


def get_code(client_id:str)->str:
    scope:str = "user-read-recently-played"
    
    url:str="https://accounts.spotify.com/authorize?"
    params:dict = {
        'response_type': 'code',
        'client_id': client_id,
        'scope':scope,
        'redirect_uri': redirect,
    }

    return url + urllib.parse.urlencode(params)

def get_tokens(base_64:str, code:str) -> dict: 
    url:str = "https://accounts.spotify.com/api/token"
    headers:dict = {
        'content-type': 'application/x-www-form-urlencoded',
        "Authorization": "Basic " + base_64
    }

    payload:dict = {
        'code':code,
        'redirect_uri':redirect,
        'grant_type': 'authorization_code'
    }
    
    request = post(url, headers=headers, data=payload)
    print(request)
    if(request.status_code == 200):
        response = request.json()
        print(response)
        return response
    else:
        print(request.json())
        return request.json()


def refresh(base_64:str, data:dict) -> dict:
    token = data['refresh']
    url:str = "https://accounts.spotify.com/api/token"

    headers:dict = {
       "Authorization": "Basic " + base_64
    }

    payload:dict = {
        'grant_type':'refresh_token',
        'refresh_token': token
    }

    request = post(url, headers=headers, data=payload)
    if(request.status_code == 200):
        response = request.json()
        return response
    else:
        return request.json()
    

if __name__ == "__main__":
    #print(get_code(client_id, redirect_uri))
    # tokens = get_tokens(client_id, client_secret)
    # print(tokens)
    # r= refresh(client_id, tokens)
    print('test')