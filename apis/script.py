import os.path
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('script', description='파이썬 스크립트 관리')
# 모델정의
Script_model = api.model('Script', {
    'packageName' : fields.String(required=True),
    'moduleName' : fields.String(required=True),
    'extension' : fields.String(required=True)
})

class ScriptDAO(object):
    def __init__(self):
        self.dir_path = './app/'
        self.ALLOWED_EXTENSIONS = ['py']

    def response_form(self):
        resource_fields = {}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(Script_model))

        return resource_fields

    def RequestParser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files', action='append')
        args = parser.parse_args()
        script = args['script']
        return script

    def create(self, packageName):
        script = self.RequestParser()
        package_path = self.dir_path + packageName

        if os.path.isdir(package_path):
            for file in script:
                extension = file.filename.split('.')[-1]
                if extension in self.ALLOWED_EXTENSIONS:  # 확장자 검사
                    file.save(package_path + '/' + secure_filename(file.filename)) # ./app/package/module.py
                else:
                    api.abort(404, "{} is an unusable extension.".format(extension))  # HTTPException 처리
        else:
            api.abort(404, "{} packageName doesn't exist".format(packageName))  # HTTPException 처리

    def update(self, packageName, moduleName):
        response_form = self.response_form()
        script = self.RequestParser()
        package_path = self.dir_path + packageName
        module_path = package_path + '/' + moduleName
        get_list=[]
        if os.path.isdir(package_path): # 패키지 존재여부
            if os.path.exists(module_path): # 모듈 존재여부
                for file in script:
                    if file.filename != moduleName:
                        api.abort(404, "[{}] to [{}] : The file name must be the same.".format(file.filename, moduleName))
                    else:
                        extension = file.filename.split('.')[-1]
                        if extension in self.ALLOWED_EXTENSIONS:  # 확장자 검사
                            file.save(package_path + '/' + secure_filename(file.filename))  # ./app/package/module.
                            data = marshal({'packageName': packageName, 'moduleName': moduleName, 'extension': extension}, Script_model)
                            get_list.append(data)
                        else:
                            api.abort(404, "{} is an unusable extension.".format(extension))  # HTTPException 처리

                response_data = {'code': 200, 'message': 'update success', 'errorPos': [], 'results': get_list}
                result = marshal(response_data, response_form)
                return result
            else:
                api.abort(404, "{} module doesn't exist".format(module_path))  # HTTPException 처리
        else:
            api.abort(404, "{} package doesn't exist".format(package_path))  # HTTPException 처리



def delete(self, packageName, moduleName):

    return

script = ScriptDAO() # DAO 객체를 만든다

@api.route('/<string:packageName>') # 네임스페이스 x.x.x.x/package/ 라우팅
@api.response(404, 'package를 찾을 수가 없어요')
@api.param('packageName', 'package를 입력해주세요')
class GoodsListManager(Resource):
    @api.expect(Script_model)
    @api.marshal_with(Script_model, code=201)
    def post(self, packageName):
        '''새로운 package 생성'''
        return script.create(packageName), 201


@api.route('/<string:packageName>/<string:moduleName>') # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'package를 찾을 수가 없어요')
@api.param('packageName', 'packageName을 입력해주세요')
@api.param('moduleName', 'moduleName을 입력해주세요')
class GoodsRUDManager(Resource):
    @api.response(204, 'package.module deleted')
    def delete(self, packageName, moduleName):
        '''해당 package 삭제'''
        script.delete(packageName, moduleName)
        return '', 204

    # @api.expect(Script_model)
    # @api.marshal_with(Script_model) : 정의 된 API 모델 형식을 그대로 반환
    def put(self, packageName, moduleName):
        '''해당 package 수정'''
        return script.update(packageName, moduleName)
