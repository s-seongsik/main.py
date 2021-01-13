import os.path
import json
from flask_restplus import Namespace, Resource, fields, marshal, Model

api = Namespace('datasource', description='데이터소스 관리') # /datasource/ 네임스페이스 생성

# 모델정의
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

response_model = api.inherit('Response', datasource_model, {
    'code': fields.String(required=True),
    'message': fields.String(required=True),
    'errorPos': fields.String(required=True),
    'results': fields.List
})

class DatasourceDAO(object):
    def response_form(self):
        resource_fields={}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(datasource_model))

        return resource_fields

    def all_get(self):
        response_form = self.response_form()
        get_list = []
        datasource_list = os.listdir('./resource/datasource/')

        for name in datasource_list:
            with open('./resource/datasource/{}'.format(name), 'r') as file:
                json_file = json.load(file)
                get_list.append(json_file)

        response_data = {'code': 200, 'message': 'success', 'results': get_list}
        result = marshal(response_data, response_form)

        return result

    def get(self, name):
        response_form = self.response_form()
        json_file = name+'.json'
        get_list = []
        datasource_list = os.listdir('./resource/datasource/')
        if json_file in datasource_list:
            with open('./resource/datasource/{}'.format(json_file), 'r') as file:
                json_data = json.load(file)
                get_list.append(json_data)
                response_data = {'code': 200, 'message': 'success', 'results': get_list}
                result = marshal(response_data, response_form)
                return result
        else:
            api.abort(404, "{} doesn't exist".format(name)) # HTTPException 처리

    def create(self, data):
        json_data = marshal(data, datasource_model)# 정의한 datasource 모델 key와 자동 매핑 틀리면 error
        json_file = data["name"] + '.json'
        with open('./resource/{}'.format(json_file), 'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent="\t")
        return json_data

    def update(self, name, data):
        json_data = marshal(data, datasource_model)  # 정의한 datasource 모델 key와 자동 매핑 틀리면 error
        json_file = name + '.json'
        with open('./resource/datasource/{}'.format(json_file), 'w',encoding='utf-8') as file:
            json.dump(json_data, file, indent="\t")
        return json_data

    def delete(self, name):
        json_file = './resource/datasource/{}'.format(name) + '.json'
        if os.path.isfile(json_file):
            os.remove(json_file)
        else:
            api.abort(404, "{} doesn't exist".format(json_file))  # HTTPException 처리


datasource = DatasourceDAO() # 인스턴스 생성

@api.route('/') # 네임스페이스 x.x.x.x/datasource/ 라우팅
class ListManager(Resource):
    # 마샬 리스트는 정의한 모델 객체를 목록으로 리턴해준다.
    # @datasource.marshal_list_with(datasource_model)
    def get(self):
        '''전체 datasource를 조회'''
        return datasource.all_get()

    @api.expect(datasource_model)
    @api.marshal_with(datasource_model, code=201)
    def post(self):
        '''새로운 datasource를 생성'''
        return datasource.create(api.payload), 201


@api.route('/<string:name>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@api.response(404, 'datasource name을 찾을 수가 없어요')
@api.param('name', 'datasource name을 입력해주세요')
class RUDManager(Resource):
    # @datasource.marshal_with(datasource_model)
    def get(self, name):
        '''해당 datasource를 조회'''
        return datasource.get(name)

    @api.response(204, 'datasource deleted')
    def delete(self, name):
        '''해당 datasource를 삭제'''
        datasource.delete(name)
        return '', 204

    @api.expect(datasource_model)
    @api.marshal_with(datasource_model)
    def put(self, name):
        '''해당 datasource를 수정'''
        return datasource.update(name, api.payload)