
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def fullchapter():
    message = "Hello, World"
    return  render_template('Tam-Thốn-Nhân-Gian.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)

# def app(environ, start_response):
#     data = b"Hello,World!\n"
#     start_response ("200 OK", [("Content-Type", "text/plain"),
#                                ("Content-Length", str(len(data)))
#                                ])
#     return  iter([data])
