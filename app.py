'''
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
'''

# 필요한 모듈을 불러온다
from flask import Flask, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__) # Flask App 생성한다
api = Api(app, version='1.0', title='넥스폼 데이터 처리 엔진', description='넥스폼에 사용될 데이터를 IMPORT/가공/분석 처리하는 파이썬 엔진 시스템') # API 만든다
ns  = api.namespace('datasource', description='') # /datasource/ 네임스페이스 생성

# REST Api에 이용할 데이터 모델을 정의한다
model_goods = api.model('Datasource', {
    'name' : fields.String(readOnly=True, required=True, description='데이터소스 이름', help='데이터소스 필수'),
    'driver': fields.String(readOnly=True, required=True, description='JDBC 드라이버', help='JDBC 드라이버'),
    'url': fields.String(readOnly=True, required=True, description='jdbc:sqlserver://IP:PORT;databaseName=NAME', help='상품번호는 필수'),
    'userName': fields.String(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'password': fields.String(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'validationQeury': fields.String(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'timeBetweenEvictionRunMillis': fields.Integer(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'testWhileIdle': fields.Boolean(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'minIdle': fields.Integer(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'maxTotal': fields.Integer(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'id': fields.Integer(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'goods_name': fields.String(required=True, description='상품명', help='상품명은 필수')
})


class GoodsDAO(object):
    '''상품정보 Data Access Object'''
    def __init__(self):
        self.counter = 0
        self.rows    = []

    def get(self, id):
        '''id를 이용하여 상품정보 조회한다'''
        for row in self.rows:
            if row['id'] == id:
                return row
        api.abort(404, "{} doesn't exist".format(id))

    def create(self, data):
        '''신규 상품을 등록한다'''
        row = data
        row['id'] = self.counter = self.counter + 1
        self.rows.append(row)
        return row

    def update(self, id, data):
        '''입력 id의 data를 수정한다'''
        row = self.get(id)
        row.update(data)
        return row

    def delete(self, id):
        '''입력 id의 data를 삭제한다'''
        row = self.get(id)
        self.rows.remove(row)

DAO = GoodsDAO() # DAO 객체를 만든다
DAO.create({'goods_name': '삼성 노트북 9'}) # 샘플 1 데이터 만든다
DAO.create({'goods_name': 'LG 노트북 gram'}) # 샘플 2 데이터 만든다


@ns.route('/') # 네임스페이스 x.x.x.x/goods 하위 / 라우팅
class GoodsListManager(Resource):
    @ns.marshal_list_with(model_goods)
    def get(self):
        '''전체 리스트 조회한다'''
        return DAO.rows

    @ns.expect(model_goods)
    @ns.marshal_with(model_goods, code=201)
    def post(self):
        '''새로운 id 추가한다'''
        # request.json[파라미터이름]으로 파라미터값 조회할 수 있다
        print('input goods_name is', request.json['goods_name'])
        return DAO.create(api.payload), 201


@ns.route('/<int:id>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@ns.response(404, 'id를 찾을 수가 없어요')
@ns.param('id', '상품번호를 입력해주세요')
class GoodsRUDManager(Resource):
    @ns.marshal_with(model_goods)
    def get(self, id):
        '''해당 id 상품정보를 조회한다'''
        return DAO.get(id)

    def delete(self, id):
        '''해당 id 삭제한다'''
        DAO.delete(id)
        return '', 200

    @ns.expect(model_goods)
    @ns.marshal_with(model_goods)
    def put(self, id):
        '''해당 id 수정한다'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)