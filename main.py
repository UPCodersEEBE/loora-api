from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/ping", methods=["POST"])
def search():
    response = "Ping is added to db (not really but wouldn't it be nice)"

    return response


if __name__ == "__main__":
    app.run()