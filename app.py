from flask import Flask
from flask import request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    url = request.args.get("url")
    headers = {"Range": "bytes=0-10"}
    try:
        r = requests.get(url, headers=headers)
    except:
        return {"Error": "Invalid url"}
    if "Accept-Ranges" in r.headers:
        return {"range": True}
    return {"range": False}


if __name__ == '__main__':
    app.run()
