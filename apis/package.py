import os.path
from flask_restplus import Namespace, Api, Resource, fields, marshal

api = Namespace('package', description='파이썬 패키지 관리') # /datasource/ 네임스페이스 생성

# 모델을 정의한다
Package_model = api.model('Package', {
    'name': fields.String(required=True)
})

class GoodsDAO(object):
    def all_get(self):
        resource_fields = {}
        resource_fields['result'] = os.listdir('./app/')
        return resource_fields
    '''
    def get(self, name):

    def create(self, data):

    def update(self, name, data):

    def delete(self, name):
    '''

package = GoodsDAO() # DAO 객체를 만든다

@api.route('/') # 네임스페이스 x.x.x.x/package/라우팅
class GoodsListManager(Resource):
    def get(self):
        '''전체 package 조회'''
        return package.all_get()

    @api.expect(Package_model)
    @api.marshal_with(Package_model, code=201)
    def post(self):
        '''새로운 package 생성'''
        return package.create(api.payload), 201


@api.route('/<string:name>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@api.response(404, 'package name을 찾을 수가 없어요')
@api.param('name', 'package name을 입력해주세요')
class GoodsRUDManager(Resource):
    # @datasource.marshal_with(datasource_model)
    def get(self, name):
        '''해당 package 조회'''
        return package.get(name)

    @api.response(204, 'Todo deleted')
    def delete(self, name):
        '''해당 package 삭제'''
        package.delete(name)
        return '', 204

    @api.expect(Package_model)
    @api.marshal_with(Package_model)
    def put(self, name):
        '''해당 package 수정'''
        return package.update(name, api.payload)
