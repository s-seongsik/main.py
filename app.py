import os.path
from flask import Flask, request
from flask_restplus import Api, Resource, fields, marshal

app = Flask("seongsik") # Flask App 생성한다
api = Api(app, version='1.0', title='넥스폼 데이터 처리 엔진', description='넥스폼에 사용될 데이터를 IMPORT/가공/분석 처리하는 파이썬 엔진 시스템') # API 만든다
datasource = api.namespace('datasource', description='') # /datasource/ 네임스페이스 생성

# 모델을 정의한다

datasource_model = api.model('Datasource', {
    'name': fields.String(required=True),
    'driver': fields.String(required=True),
    'url': fields.String(required=True),
    'userName': fields.String(required=True),
    'password': fields.String(required=True),
    'validationQeury': fields.String,
    'timeBetweenEvictionRunMillis': fields.Integer,
    'testWhileIdle': fields.Boolean,
    'minIdle': fields.Integer,
    'maxTotal': fields.Integer
})

class GoodsDAO(object):
    '''상품정보 Data Access Object'''
    def __init__(self):
        self.counter = 0
        self.rows = []

    def get_form(self):
        resource_fields={}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.Integer
        resource_fields['errorPos'] = []
        resource_fields['results'] = []

        return resource_fields

    def all_get(self):
        import json
        json_file_list = self.get_form()
        datasource_list = os.listdir('./resource/')
        for name in datasource_list:
            with open('./resource/{}'.format(name), 'r') as file:
                json_file = json.load(file)
                json_file_list['results'].append(json_file)
        json_file_list['code'] = 200
        json_file_list['message'] = 'successful operation'
        return json_file_list

    def get(self, name):
        import json
        json_file_list = self.get_form()
        json_file = name+'.json'
        datasource_list = os.listdir('./resource/')
        if json_file in datasource_list:
            with open('./resource/{}'.format(json_file), 'r') as file:
                json_data = json.load(file)
                json_file_list['results'].append(json_data)
                json_file_list['code'] = 200
                json_file_list['message'] = 'successful operation'
                return json_file_list
        else:
            api.abort(404, "{} doesn't exist".format(name)) # HTTPException 처리

    def create(self, data):
        import json
        json_data = marshal(data, datasource_model)# 정의한 datasource 모델 key와 자동 매핑 틀리면 error
        json_file = data["name"] + '.json'
        with open('./resource/{}'.format(json_file), 'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent="\t")
        return json_data

    def update(self, name, data):
        import json
        json_data = marshal(data, datasource_model)  # 정의한 datasource 모델 key와 자동 매핑 틀리면 error
        json_file = name + '.json'
        with open('./resource/{}'.format(json_file), 'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent="\t")
        return json_data

    def delete(self, name):
        json_file = './resource/{}'.format(name) + '.json'
        if os.path.isfile(json_file):
            os.remove(json_file)
        else:
            api.abort(404, "{} doesn't exist".format(name))  # HTTPException 처리


DAO = GoodsDAO() # DAO 객체를 만든다

@datasource.route('/') # 네임스페이스 x.x.x.x/goods 하위 / 라우팅
class GoodsListManager(Resource):
    # 마샬 리스트는 정의한 모델 객체를 목록으로 리턴해준다.
    # @datasource.marshal_list_with(datasource_model)
    def get(self):
        '''전체 datasource를 조회'''
        return DAO.all_get()

    @datasource.expect(datasource_model)
    @datasource.marshal_with(datasource_model, code=201)
    def post(self):
        '''새로운 datasource를 생성'''
        return DAO.create(api.payload), 201


@datasource.route('/<string:name>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@datasource.response(404, 'datasource name을 찾을 수가 없어요')
@datasource.param('name', 'datasource name을 입력해주세요')
class GoodsRUDManager(Resource):
    # @datasource.marshal_with(datasource_model)
    def get(self, name):
        '''해당 datasource를 조회'''
        return DAO.get(name)

    @datasource.response(204, 'Todo deleted')
    def delete(self, name):
        '''해당 datasource를 삭제'''
        DAO.delete(name)
        return '', 204

    @datasource.expect(datasource_model)
    @datasource.marshal_with(datasource_model)
    def put(self, name):
        '''해당 datasource를 수정'''
        return DAO.update(name, api.payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)