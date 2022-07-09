from flask.helpers import flash
from fetch import Parser, extract
from flask import render_template
from werkzeug.urls import url_parse
from app import app
from app.form import ParserForm
from symbol import get_signal


@app.route("/", methods=["POST","GET"])
def index():
    form = ParserForm()
    if form.validate_on_submit():
        name = extract(form.data['link'])
        supported = ["truyenfull.vn", "webtruyen.com", "dantri.com.vn", "localhost"]
        if name in supported:
            result = Parser(name, form.data['link'])
            return  render_template("result.html", result=result)
        else:
            flash("website is not supported")
    return  render_template("home.html", form = form)

@app.route("/signal")
def trade_signal():
    symbols_list = ["GBPUSD=X", "EURUSD=X", "GC=F", "JPY=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X","GBPJPY=X", "EURGBP=X", "EURCAD=X"]
    x = {}
    for s in symbols_list:
        n = get_signal(s)
        x[s] = n
    return x