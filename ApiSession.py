import asyncio
from flask import Flask, request
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded

client = None
loop = asyncio.get_event_loop()
app = Flask(__name__)

@app.route('/SendCode/')
def send_login_code():
    try:
        phone_number = request.args.get('n')
        api_id = request.args.get('api_id')
        api_hash = request.args.get('api_hash')
        asyncio.set_event_loop(loop)
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
        client.connect()
        return {'code': client.send_code(phone_number).phone_code_hash}
    except Exception as e:
        return {'error': str(e)}

@app.route('/loginOutPass/')
def login_without_password():
    try:
        phone_number = request.args.get('n')
        phone_code = request.args.get('c')
        hash_code = request.args.get('h')
        api_id = request.args.get('api_id')
        api_hash = request.args.get('api_hash')
        asyncio.set_event_loop(loop)
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
        client.connect()
        LoginUser = client.sign_in(phone_number, hash_code, phone_code)
        return {'session': client.export_session_string()}
    except Exception as e:
        return {'error': str(e)}

@app.route('/loginWithPass/')
def login_with_password():
    try:
        phone_number = request.args.get('n')
        phone_code = request.args.get('c')
        hash_code = request.args.get('h')
        passwordAcc = request.args.get('p')
        api_id = request.args.get('api_id')
        api_hash = request.args.get('api_hash')
        asyncio.set_event_loop(loop)
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
        client.connect()
        try:
            LoginUser = client.sign_in(phone_number, hash_code, phone_code)
        except SessionPasswordNeeded:
            client.check_password(passwordAcc)
        return {'session': client.export_session_string()}
    except Exception as e:
        return {'error': str(e)}

def run():
    app.run(host="0.0.0.0", port=8003)

if __name__ == '__main__':
    run()
