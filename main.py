import base64,os

from flask import Flask, redirect ,url_for, request
from flask_cors import CORS, cross_origin

from auth import get_code, get_tokens, refresh, encode_auth
from utility import generate_keys, random_key, write_to_txt,read_file 

app=Flask(__name__)
CORS(app, resources={r"/*/*/*": {"origins": "*"}})

client_keys:list = []
keys:list = generate_keys()
rk:str = random_key()
info:dict = {}

if os.path.exists("util/out.txt"):
    info:dict = read_file()

@app.route('/', methods=['GET'])
def bad_request()->str:
     return '''
        <html><body>
                <div>
                    <h1>Bad Request</h1>
                    <p>no key in url or wrong key entered. </p>
                    <p><a href="/help">help</a></p>
                </div>
            </body><html>
    '''

@app.route('/help', methods=['GET'])
def help()->str:
    return '''
            <html><body>
                <div>
                    <h1>App key</h1>
                    <p>Store using an env file in your app root directory. Use at your own risk</p>
                    <p>key: <a href="/key">use key</a></p>
                    <h2>Server Directory:</h2>
                    <ul>/help -> show help</ul>
                    <ul>/key/client_id/client_secret -> get auth code</ul>
                </div>
            </body><html>
        '''

@app.route('/key', methods=['GET'])
def index()->str:
    return {
            "key":rk,
            "readme":"add /key/client_id/client_secret to url -> get auth code"}

@app.route('/<key>/<id>/<secret>', methods=['GET'])
def redirect_to_code(key,id,secret):
    if key in keys:
        client_keys.append(key)
        client_keys.append(id)
        client_keys.append(secret)
        return redirect(get_code(id))
    else:
        return redirect(url_for(bad_request))

@app.route('/usercode', methods=['GET'])
def get_user_code():
    key = client_keys[0]
    if key in keys:
        base_64 = encode_auth(get_id(), get_secret())
        client_keys.append(base_64)
        code = request.full_path.split("=")[1]
        tokens = get_tokens(base_64, code)
        userinfo:dict = {str(get_id()):{
                'url': request.base_url + '/' + key +'/' + get_id(),
                'code':code,
                'refresh':tokens['refresh_token'],
                'access':tokens['access_token'],
                'scope':tokens['scope'],
                'type':tokens['token_type'],
                'base_64':base_64,
                'readme':'SAVE REFRESH TOKEN. HIDE USING ENV.'
            }}
        info.update(userinfo)
        write_to_txt(info)
        return tokens
    else:
        redirect(url_for(bad_request))

@app.route('/<key>/<id>', methods=['GET'])
def get_user(key,id):
    if key in keys and id and info:
        return info[id]
    else:
        return redirect(url_for(bad_request))
    
@app.route('/<key>/<id>/refresh', methods=['GET'])
def get_refresh(key,id):
    if key in keys:
        return refresh(info[id]['base_64'], info[id])
        
    else:
        return {"error":"something went wrong. make sure you have added your credentials first."}


def get_id() -> str:
    return client_keys[1]

def get_secret() -> str:
    return client_keys[2]

def get_base64()-> str:
    return client_keys[3]

if __name__ == "__main__":
    app.run(port="5432", debug=True)