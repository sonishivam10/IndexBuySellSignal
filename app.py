from flask import Flask, abort, jsonify, request, render_template
from datetime import date, datetime, timedelta
from sklearn.externals import joblib
import numpy as np
import json
import pandas as pd
from pandas_datareader import data as pdr

todays_date = date.today()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


# def input_to_one_hot(data):
#     # initialize the target vector with zero values
#     enc_input = np.zeros(2)
#     # set the numerical input as they are
#     enc_input[0] = data['open1']-data['close']
#     enc_input[1] = data['high']-data['low']
#     return enc_input



@app.route('/api',methods=['POST'])
def get_delay():
    result=request.form
    indices=result['indices']
    feat_inp= pdr.get_data_yahoo(indices, start=todays_date , end=todays_date )     
    feat_inp=feat_inp.drop(['Volume','Adj Close'], axis=1)
    feat_inp=feat_inp[:1]
    feat_inp['Open-Close'] = feat_inp.Open - feat_inp.Close
    feat_inp['High-Low'] = feat_inp.High - feat_inp.Low
    a=feat_inp[['Open-Close','High-Low']]
    #indice model select
    if(indices=="^DJI"):
        gbr = joblib.load('DJI.pkl')
    elif(indices=="^GSPC"):
        gbr = joblib.load('model.pkl')
    elif(indices=="^IXIC"):
        gbr = joblib.load('Nasdaq.pkl')
    else:
        gbr = joblib.load('Nikkei.pkl')
    
    price_pred = gbr.predict(a)[0]
    if(price_pred==1):
        output="Buy"
    else:
        output="Sell"
    feat_inp=feat_inp.round(2)
    return json.dumps({'price':output, 'open':feat_inp['Open'][0], 'close':feat_inp['Close'][0], 'high':feat_inp['High'][0], 'low':feat_inp['Low'][0], })
    #d=feat_inp.to_dict('records')
    #d[0]['price'] = output
    #return json.dumps(d[0]);
    #return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':
    app.run(port=8080, debug=True)




