from flask import Flask
from flask import render_template
from flask import request, redirect
import engine
import urlprocessing
import writefile
from app import app

app = Flask(__name__)

@app.route("/")
def index():
    return  render_template("form.html")

@app.route("/", methods=['POST'])
def callfunc():
    link = request.form['url']
    urlslist = urlprocessing.get_url(link)
    message = ""
    for url in urlslist:
        b = engine.chaptername(url)
        a = engine.createname(b)
        c = engine.chaptercontent(url)
        with open(a, 'w', encoding='utf-8') as f:
            f.write(b + c )
            f.flush()
        message = message + "<a href=\""+ a + "\">" + b + "</a> <br>"
    return message



if __name__ == "__main__":
    app.run(debug=True)

# def app(environ, start_response):
#     data = b"Hello,World!\n"
#     start_response ("200 OK", [("Content-Type", "text/plain"),
#                                ("Content-Length", str(len(data)))
#                                ])
#     return  iter([data])
