from flask import Flask, request, Response
from flask_request_params import bind_request_params
import pandas as pd
import holders
import crawler_api

app = Flask(__name__)
app.before_request(bind_request_params)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/holders', methods=['GET'])
def get_holders_df():
    #text = request.args.get('id')
    df = get_holders()
    return df.to_html(header="true", table_id="table")

@app.route('/crawler', methods=['GET'])
def get_crawler_df():
    #text = request.args.get('id')
    df = get_crawler()
    return df.to_html(header="true", table_id="table")

def get_holders():
    df = holders.run()
    return df

def get_crawler():
    df = crawler_api.run()
    return df

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')