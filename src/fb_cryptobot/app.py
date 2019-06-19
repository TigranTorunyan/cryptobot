from flask import Flask, request, jsonify
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from models import CryptoCurrency
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
port = '5000'

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = '5mLaIgaGrZOK//TARbN74bYYpZDFyfM0r0IC8lnBeGA=' # <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAASACHW7vmEBAGIlMszcVklC47CIZBf4IpQZAKWfboNi8FHcZBC9ZALgmW8QYBQZAuKLRVAV4InSb5t52ZCdpTbJM97LFkBlV1IKwA2JKumXLl0ghDbOzhZALMXGinUuB11ZCAfOT2VDdFmre6mF7KI6sBLDVBlaETvLAZAdBmVjTcwZDZD' # paste your page access token here>"



def verify_webhook(request):
    # return request.args.get("hub.challenge")
    '''if request.args.get("hub.verify_token") != VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return "incorrect"'''
    #print(request.args.get("hub.verify_token"))
    #print(request.args.get("hub.challenge"))
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook")
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
       return verify_webhook(request)
       #print(request.args.get("hub.verify_token"))
       #return request.args.get("hub.challenge")

    if request.method == 'POST':
        data = request.get_data(as_text=True)
        api_data = request.get_data(as_text=True).split(':')[1][1:-1]
        valid_data = api_data.upper()
        #payload = request.json
        #event = payload['entry'][0]['messaging']
        r = requests.get("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(valid_data))
        
        for x in data:
            if is_user_message(x):
                #text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, valid_data)
        return jsonify(
           status=200,
           replies=[{
             'type': 'text',
             'content': r.json()['USD']
           }]
          )

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=r
    )

    return response.json()

if __name__ == '__main__':
    app.run()
