from flask import Flask, request
from apis import api

app = Flask("NEXPOM") # Flask App 생성한다
api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)