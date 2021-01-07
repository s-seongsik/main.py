import os.path
from flask_restplus import Namespace, Resource, fields, marshal

api = Namespace('module', description='파이썬 모듈 관리') # /module/ 네임스페이스 생성

# 모델정의
module_model = api.model('Module', {
    'packageName': fields.String(required=True),
    'moduleName' : fields.String(required=True),
    'size' : fields.String(required=True)
})

class ModuleDAO(object):
    def __init__(self):
        self.dir_path = './app/'

    def get_size(self,package_path, moduleName):
        import os

        try:
            # print(n / 1024, "KB")  # 킬로바이트 단위로
            # print("%.2f MB" % (n / (1024.0 * 1024.0)))  # 메가바이트 단위로
            size = os.path.getsize(package_path + '/' + moduleName) # './app/module.py'
            result = str(size/1024)+' KB'
            return result
        except os.error:
            return 404

    def response_form(self):
        resource_fields = {}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(module_model))

        return resource_fields

    def all_get(self):
        response_form = self.response_form()
        get_list = []
        package_list = os.listdir(self.dir_path)

        for packageName in package_list:
            package_path = self.dir_path + packageName
            module_list = os.listdir(package_path)
            for moduleName in module_list:
                result = self.get_size(package_path,moduleName)
                size="file doesn't exists" if result==404 else result
                data = marshal({'packageName':packageName, 'moduleName':moduleName, 'size':size}, module_model)
                get_list.append(data)

        response_data = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_list}
        result = marshal(response_data, response_form)

        return result

    def get(self, packageName, moduleName):
        response_form = self.response_form()
        get_list = []
        package_path = self.dir_path + packageName

        if os.path.isdir(package_path):
            if moduleName==None: # /package/{packageName}
                module_list = os.listdir(package_path)
                for moduleName in module_list:
                    result = self.get_size(package_path, moduleName)
                    size = "file doesn't exists" if result == 404 else result
                    data = marshal({'packageName': packageName, 'moduleName': moduleName, 'size': size}, module_model)
                    get_list.append(data)
                response_data = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_list}
                result = marshal(response_data, response_form)
                return result
            else: # /package/{packageName}/{moduleName}
                mudule_path = package_path + '/' + moduleName
                if os.path.exists(mudule_path):
                    result = self.get_size(package_path, moduleName)
                    size = "file doesn't exists" if result == 404 else result
                    data = marshal({'packageName': packageName, 'moduleName': moduleName, 'size': size}, module_model)
                    get_list.append(data)
                    response_data = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_list}
                    result = marshal(response_data, response_form)
                    return result
                else:
                    api.abort(404, "{} moduleName doesn't exist".format(moduleName))  # HTTPException 처리
        else:
            api.abort(404, "{} packageName doesn't exist".format(packageName))  # HTTPException 처리

    def update(self, packageName, moduleName, data):
        response = marshal(data, module_model)
        updateName = response['moduleName']
        package_path = self.dir_path + packageName
        module_path = package_path + '/' + moduleName
        module_update_path = package_path + '/' + updateName

        if os.path.isdir(package_path):
            if os.path.exists(module_path):
                os.rename(module_path, module_update_path)
                return response
            else:
                api.abort(404, "{} moduleName doesn't exists".format(moduleName))  # HTTPException 처리
        else:
            api.abort(404, "{} packageName doesn't exist".format(packageName))  # HTTPException 처리

module = ModuleDAO() # DAO 객체를 만든다

@api.route('/') # 네임스페이스 x.x.x.x/package/ 라우팅
class GoodsListManager(Resource):
    def get(self):
        '''전체 package 조회'''
        return module.all_get()

@api.route('/<string:packageName>') # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'package를 찾을 수가 없습니다.')
@api.param('packageName', 'package를 입력해주세요')
class ModuleRManager(Resource):
    # @datasource.marshal_with(datasource_model)
    def get(self, packageName):
        '''해당 package.module 조회'''
        return module.get(packageName, None)

@api.route('/<string:packageName>/<string:moduleName>')  # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'package를 찾을 수가 없습니다.')
@api.param('packageName', 'package를 입력해주세요')
@api.param('moduleName', 'moduleName를 입력해주세요')
class ModuleUManager(Resource):
    @api.expect(module_model)
    @api.marshal_with(module_model)
    def put(self, packageName, moduleName):
        '''해당 package.module name 수정'''
        return module.update(packageName, moduleName, api.payload)
