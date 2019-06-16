from flask import Flask, request, jsonify
import json
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
port = '5000'

@app.route('/', methods=['POST'])
def index():
  # print(request.get_data(as_text=True))
  data = request.get_data(as_text=True).split(':')[1][1:-1]
  valid_data = data.upper()
  # print("DATA - {}\n".format(data))  
 
  r = requests.get("https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(valid_data))

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': r.json()['USD']
    }]
  )

@app.route('/errors', methods=['POST'])
def errors():
  return jsonify(status=200)

app.run(port=port)
