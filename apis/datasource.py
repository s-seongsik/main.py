import os.path
import json
from configparser import ConfigParser
from flask_restplus import Namespace, Resource, fields, marshal, Model

api = Namespace('datasource', description='데이터소스 관리') # /datasource/ 네임스페이스 생성

# 모델정의
datasource_model = api.model('Datasource', {
    'name': fields.String(required=True),
    'type': fields.String(required=True, description="JDBC/ODBC/pymssql"),
    'host': fields.String(required=True),
    'port': fields.String(required=True),
    'database': fields.String(required=True),
    'user': fields.String(required=True),
    'password': fields.String(required=True)
})

class DatasourceDAO(object):
    def __init__(self):
        self.dir_path = './resource/config/config.ini'

    def response_form(self):
        resource_fields={}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(datasource_model))
        return resource_fields

    def config(self):
        config = ConfigParser()
        config.read(self.dir_path, encoding='utf-8')
        return config

    def get(self, name):
        config = self.config()
        response_form = self.response_form()
        section_list = config.sections()
        get_data = []
        if name == None:
            for section in section_list:
                option_list = config.options(section)
                object = {}
                for option in option_list:
                    object[option] = config.get(section, option)
                get_data.append(object)
            response = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_data}
            result = marshal(response, response_form)
        else:
            if not config.has_section(name):
                api.abort(404, "{} doesn't exist".format(name))  # HTTPException 처리
            else:
                option_list = config.options(name)
                object = {}
                for option in option_list:
                    object[option] = config.get(name, option)
                get_data.append(object)
                response = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_data}
                result = marshal(response, response_form)
        return result

    def update(self, name, data):
        config = self.config()
        response_form = self.response_form()
        get_data = marshal(data, datasource_model)

        if not config.has_section(name):
            api.abort(404, "{} doesn't exist".format(name))  # HTTPException 처리
        else:
            for key in get_data.keys():
                value = get_data[key]
                config.set(name, key, value)
            with open(self.dir_path, "w") as file:
                config.write(file)
            response = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_data}
            result = marshal(response, response_form)
            return result

    def create(self, data):
        config = self.config()
        response_form = self.response_form()
        get_data = marshal(data, datasource_model)
        name = get_data["name"]
        # section 존재여부 확인
        if config.has_section(name):
            api.abort(404, "{} already exists".format(name))  # HTTPException 처리
        else:
            # ConfigParser section 생성
            config[name] = get_data
            with open(self.dir_path, "w") as file:
                config.write(file)

            response = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_data}
            result = marshal(response, response_form)
            return result

    def delete(self,name):
        config = self.config()
        if not config.has_section(name):
            api.abort(404, "{} doesn't exist".format(name))  # HTTPException 처리
        else:
            config.remove_section(name)
            with open(self.dir_path, "w") as file:
                config.write(file)
            return {"message" : "{} delete success".format(name)}  # HTTPException 처리

datasource = DatasourceDAO() # 인스턴스 생성

@api.route('/') # 네임스페이스 x.x.x.x/datasource/ 라우팅
class ListManager(Resource):
    # 마샬 리스트는 정의한 모델 객체를 목록으로 리턴해준다.
    # @datasource.marshal_list_with(datasource_model)
    @api.expect(datasource_model)
    def get(self):
        '''datasource 전체조회'''
        return datasource.get(None)

    @api.expect(datasource_model)
    # @api.marshal_with(datasource_model, code=201)
    def post(self):
        '''datasource 생성'''
        return datasource.create(api.payload), 201


@api.route('/<string:name>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@api.response(404, 'datasource name을 찾을 수가 없어요')
@api.param('name', 'datasource name을 입력해주세요')
class RUDManager(Resource):
    # @datasource.marshal_with(datasource_model)
    @api.expect(datasource_model)
    def get(self, name):
        '''datasource를 조회'''
        return datasource.get(name)

    @api.response(204, 'datasource deleted')
    def delete(self, name):
        '''datasource를 삭제'''
        return datasource.delete(name)

    @api.expect(datasource_model)
    # @api.marshal_with(datasource_model)
    def put(self, name):
        '''datasource를 수정'''
        return datasource.update(name, api.payload)