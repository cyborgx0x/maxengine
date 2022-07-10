from flask.helpers import flash
from flask import render_template
from werkzeug.urls import url_parse
from app import app
from symbol import get_signal
import pandas as pd
import matplotlib.pyplot as plt
import os.path

@app.route("/")
def index():
    symbols_list = ["GBPUSD=X", "EURUSD=X", "GC=F", "JPY=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X","GBPJPY=X", "EURGBP=X", "EURCAD=X"]
    collection = []
    for s in symbols_list:
        file_name = s + "2Y1D.csv"
        picture = s + "2Y1D" + ".jpg"
        if os.path.exists("app/static/"+picture):
            collection.append(picture)
        else:
            pair = pd.read_csv(file_name, index_col="Date")
            pair=pair["Close"]
            plt.figure(num=file_name)
            plt.plot(pair)
            plt.savefig("app/static/"+ picture )
            collection.append(picture)
    return  render_template("home.html", picture = collection)

@app.route("/signal")
def trade_signal():
    symbols_list = ["GBPUSD=X", "EURUSD=X", "GC=F", "JPY=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X","GBPJPY=X", "EURGBP=X", "EURCAD=X"]
    x = []
    for s in symbols_list:
        n = get_signal(s)
        x.append(n)
    return render_template("signal.html", signal = x)