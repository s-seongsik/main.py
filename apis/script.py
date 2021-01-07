import os.path
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('script', description='파이썬 스크립트 관리')
# 모델정의
Script_model = api.model('Script', {
    'packageName': fields.String(required=True),
    'moduleName': fields.List(fields.String,required=True)
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

    def create(self, packageName):
        parser = reqparse.RequestParser()
        parser.add_argument('script', type=FileStorage, location='files', action='append')
        args = parser.parse_args()
        script = args['script']

        for image in script:
            extension = image.filename.split('.')[-1]

            if extension in self.ALLOWED_EXTENSIONS:  # 확장자 검사
                image.save('./uploads/{0}'.format(secure_filename(image.filename)))
            else:
                return {"status": "false", "result": "Not allowed extension"}

        return {"status": "true", "result": "Upload success", "file": secure_filename(image.filename)}


    def update(self, packageName, data):
        return

    def delete(self, packageName):
        return

script = ScriptDAO() # DAO 객체를 만든다

@api.route('/') # 네임스페이스 x.x.x.x/package/ 라우팅
class GoodsListManager(Resource):
    @api.expect(Script_model)
    @api.marshal_with(Script_model, code=201)
    def post(self):
        '''새로운 package 생성'''
        return script.create(api.payload), 201


@api.route('/<string:packageName>') # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'package를 찾을 수가 없어요')
@api.param('packageName', 'package를 입력해주세요')
class GoodsRUDManager(Resource):
    @api.response(204, 'package deleted')
    def delete(self, packageName):
        '''해당 package 삭제'''
        script.delete(packageName)
        return '', 204

    @api.expect(Script_model)
    @api.marshal_with(Script_model)
    def put(self, packageName):
        '''해당 package 수정'''
        return script.update(packageName, api.payload)
