import os.path
from flask_restplus import Namespace, Api, Resource, fields, marshal

api = Namespace('package', description='파이썬 패키지 관리') # /datasource/ 네임스페이스 생성

# 모델정의
Package_model = api.model('Package', {
    'packageName': fields.String(required=True),
    'modules': fields.List(fields.String,required=True)
})


class GoodsDAO(object):
    def __init__(self):
        self.dir_path = './app/'

    def response_form(self):
        resource_fields = {}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(Package_model))

        return resource_fields

    def all_get(self):
        response_form = self.response_form()
        get_list = []
        package_list = os.listdir(self.dir_path)

        for package in package_list:
            module_list = os.listdir(self.dir_path+package)
            data = marshal({'packageName': package, 'modules': module_list}, Package_model)
            get_list.append(data)

        response_data = {'code' : 200, 'message' : 'success', 'errorPos' : [], 'results' : get_list}
        result = marshal(response_data, response_form)

        return result

    def get(self, packageName):
        response_form = self.response_form()
        get_list = []
        get_path = self.dir_path+packageName
        if os.path.isdir(get_path):
            module_list = os.listdir(get_path)
            data = marshal({'packageName': packageName, 'modules': module_list}, Package_model)
            get_list.append(data)

            response_data = {'code': 200, 'message': 'success', 'errorPos' : [], 'results': get_list}
            result = marshal(response_data, response_form)
            return result
        else:
            api.abort(404, "{} doesn't exist".format(packageName))  # HTTPException 처리

    def create(self, data):
        response = marshal(data, Package_model)
        packageName = data["packageName"]
        create_path = self.dir_path+packageName

        if not os.path.exists(create_path):
            os.makedirs(create_path)
            return response
        else:
            api.abort(404, "{} already exists".format(packageName))  # HTTPException 처리

    def update(self, packageName, data):
        response = marshal(data, Package_model)
        updateName = response['packageName']
        update_path = self.dir_path+packageName

        if os.path.exists(update_path):
            os.rename(update_path, self.dir_path+updateName)
            return response
        else:
            api.abort(404, "{} already exists".format(packageName))  # HTTPException 처리

    def delete(self, packageName):
        delete_path = self.dir_path+packageName

        if os.path.exists(delete_path):
            os.rmdir(delete_path)
        else:
            api.abort(404, "{} doesn't exists".format(packageName))  # HTTPException 처리

package = GoodsDAO() # DAO 객체를 만든다

@api.route('/') # 네임스페이스 x.x.x.x/package/ 라우팅
class GoodsListManager(Resource):
    def get(self):
        '''전체 package 조회'''
        return package.all_get()

    @api.expect(Package_model)
    @api.marshal_with(Package_model, code=201)
    def post(self):
        '''새로운 package 생성'''
        return package.create(api.payload), 201


@api.route('/<string:packageName>') # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'package를 찾을 수가 없어요')
@api.param('packageName', 'package를 입력해주세요')
class GoodsRUDManager(Resource):
    # @datasource.marshal_with(datasource_model)
    def get(self, packageName):
        '''해당 package 조회'''
        return package.get(packageName)

    @api.response(204, 'package deleted')
    def delete(self, packageName):
        '''해당 package 삭제'''
        package.delete(packageName)
        return '', 204

    @api.expect(Package_model)
    @api.marshal_with(Package_model)
    def put(self, packageName):
        '''해당 package 수정'''
        return package.update(packageName, api.payload)
