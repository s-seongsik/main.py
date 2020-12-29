from flask_cors import CORS
import os
import json
import datetime

from flask import Flask, jsonify, request, render_template,send_file
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(42)
CORS(app)

@app.route('/get_data', methods=['POST','GET'])
def main():
    # json형태로 request
    data = request.get_json()
    jsonData = json.dumps(data)
    dictData = json.loads(jsonData)
    return jsonify(dictData)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
