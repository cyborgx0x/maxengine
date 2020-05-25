from flask import Flask
from flask import render_template
from flask import request, redirect
import engine

app = Flask(__name__)

@app.route("/")
def index():
    message = """
                <h1>insert link here</h1> <br>
                <form method="POST">
                    <input name="url">
                </form>
            """
    return  message

@app.route("/", methods=['POST'])
def callfunc():
    link = request.form['url']
    
    return engine.chaptername(link) + engine.chaptercontent(link)


if __name__ == "__main__":
    app.run(debug=True)

# def app(environ, start_response):
#     data = b"Hello,World!\n"
#     start_response ("200 OK", [("Content-Type", "text/plain"),
#                                ("Content-Length", str(len(data)))
#                                ])
#     return  iter([data])
