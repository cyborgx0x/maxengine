from flask.helpers import flash
from flask import render_template
from werkzeug.urls import url_parse
from app import app
from symbol import get_signal, Symbol
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import datetime

@app.route("/")
def index():
    symbols_list = ["GBPUSD=X"]
    collection = []
    for s in symbols_list:
        daily_dt = Symbol(s, "2Y", "1D")
        hour_dt = Symbol(s, "20D", "60m")
        fif_dt = Symbol(s, "5D", "15m")
        collection.append(daily_dt.graph_abs)
        collection.append(hour_dt.graph_abs)
        collection.append(fif_dt.graph_abs)
    return  render_template("home.html", picture = collection)

@app.route("/signal")
def trade_signal():
    symbols_list = ["GBPUSD=X", "EURUSD=X", "GC=F", "JPY=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X","GBPJPY=X", "EURGBP=X", "EURCAD=X"]
    x = []
    for s in symbols_list:
        n = get_signal(s)
        x.append(n)
    return render_template("signal.html", signal = x)