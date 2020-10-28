from flask import Flask, request, Response
from flask_request_params import bind_request_params
import pandas as pd
import sys 
sys.path.append("..") 
from crawler import table

app = Flask(__name__)
app.before_request(bind_request_params)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/table', methods=['GET'])
def get_holders_df():
    #text = request.args.get('id')
    df = get_table()
    return df.to_html(header="true", table_id="table")

def get_table():
    df = table.run()
    return df

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)