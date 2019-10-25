from flask import Flask
from flask import request
from flask_cors import CORS
import requests

BYTE_RANGE_ONE = '0-10'
BYTE_RANGE_TWO = '15-20'

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    url = request.args.get("url")
    headers_single = {"Range": "bytes={}".format(BYTE_RANGE_ONE)}
    headers_multi = {"Range": "bytes={}, {}".format(BYTE_RANGE_ONE, BYTE_RANGE_TWO)}
    try:
        r_single = requests.get(url, headers=headers_single)
        r_multi = requests.get(url, headers=headers_multi)
    except Exception as e:
        return {'error': True, 'log': str(e)}
    data = {'single': {}, 'multi': {}}

    r_multi_content = r_multi.content.decode('UTF-8')

    data['single']['content'] = r_single.content.decode('UTF-8')
    data['multi']['content'] = r_multi_content

    data['single']['code'] = r_single.status_code
    data['multi']['code'] = r_multi.status_code

    content_type = 'Content-Type'
    if content_type in r_single.headers:
        data['single']['content_type'] = r_single.headers[content_type]
    if content_type in r_multi.headers:
        data['multi']['content_type'] = r_single.headers[content_type]

    if 'Content-Range: bytes {}'.format(BYTE_RANGE_ONE) in r_multi_content and \
            'Content-Range: bytes {}'.format(BYTE_RANGE_TWO) in r_multi_content:
        data['multi']['multipart'] = True

    return data


if __name__ == '__main__':
    app.run()
