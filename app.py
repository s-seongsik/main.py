import os.path
from flask import Flask, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__) # Flask App 생성한다
api = Api(app, version='1.0', title='넥스폼 데이터 처리 엔진', description='넥스폼에 사용될 데이터를 IMPORT/가공/분석 처리하는 파이썬 엔진 시스템') # API 만든다
ns  = api.namespace('datasource', description='') # /datasource/ 네임스페이스 생성

# REST Api에 이용할 데이터 모델을 정의한다
datasource_model = api.model('datasource', {
    'name' : fields.String(required=True, description='데이터소스 이름', help='데이터소스 필수'),
    'driver': fields.String(required=True, description='\t'+'oracle.jdbc.OracleDriver,' + '\n' + '\t' + 'net.sourceforge.jtds.jdbc.Driver', help='JDBC 드라이버'),
    'url': fields.String(required=True, description='jdbc:sqlserver://IP:PORT;databaseName=NAME', help='상품번호는 필수'),
    'userName': fields.String(required=True, description='DB User', help='DB USER 필수'),
    'password': fields.String(required=True, description='DB Password', help='DB Password 필수'),
    'validationQeury': fields.String(readOnly=True),
    'timeBetweenEvictionRunMillis': fields.Integer,
    'testWhileIdle': fields.Boolean,
    'minIdle': fields.Integer,
    'maxTotal': fields.Integer
})

class GoodsDAO(object):
    '''상품정보 Data Access Object'''
    def __init__(self):
        self.datasource_list = os.listdir('./resource/') # 전역변수 처리 필수
        self.counter = 0
        self.rows = []

    def all_get(self):
        import json
        json_file_list = []
        for name in self.datasource_list:
            with open('./resource/{}'.format(name), 'r') as file:
                json_file = json.load(file)
                json_file_list.append(json_file)
        return json_file_list

    def get(self, name):
        import json
        json_file = name+'.json'
        '''id를 이용하여 상품정보 조회한다'''
        if json_file in self.datasource_list:
            with open('./resource/{}'.format(json_file), 'r') as file:
                json_data = json.load(file)
                return json_data
        else:
            api.abort(404, "{} doesn't exist".format(name)) # HTTPException 처리

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

@ns.route('/') # 네임스페이스 x.x.x.x/goods 하위 / 라우팅
class GoodsListManager(Resource):
    @ns.marshal_list_with(datasource_model)
    def get(self):
        '''전체 datasource를 조회한다'''
        return DAO.all_get()

    @ns.expect(datasource_model)
    @ns.marshal_with(datasource_model, code=201)
    def post(self):
        '''새로운 id 추가한다'''
        # request.json[파라미터이름]으로 파라미터값 조회할 수 있다
        print('input goods_name is', request.json['goods_name'])
        return DAO.create(api.payload), 201


@ns.route('/<string:name>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@ns.response(404, 'datasource name을 찾을 수가 없어요')
@ns.param('name', 'datasource name을 입력해주세요')
class GoodsRUDManager(Resource):
    @ns.marshal_with(datasource_model)
    def get(self, name):
        '''해당 id 상품정보를 조회한다'''
        return DAO.get(name)

    def delete(self, id):
        '''해당 id 삭제한다'''
        DAO.delete(id)
        return '', 200

    @ns.expect(datasource_model)
    @ns.marshal_with(datasource_model)
    def put(self, id):
        '''해당 id 수정한다'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)