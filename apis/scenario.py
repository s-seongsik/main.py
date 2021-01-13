import os.path
import json
from flask_restplus import Namespace, Resource, fields, marshal

api = Namespace('scenario', description='파이썬 패키지 관리')
# 모델정의
Scenario_model = api.model('Scenario', {
    'scenarioId' : fields.String(required=True),
    'datasourceName' : fields.String(required=True),
    'packageName': fields.String(required=True)
})

class ScenarioDAO(object):
    def __init__(self):
        self.dir_path = './resource/scenario/'

    def response_form(self):
        resource_fields={}
        resource_fields['code'] = fields.Integer
        resource_fields['message'] = fields.String
        resource_fields['errorPos'] = fields.List(fields.Integer)
        resource_fields['results'] = fields.List(fields.Nested(Scenario_model))
        return resource_fields

    def get(self, scenarioId):
        response_form = self.response_form()
        get_list = []
        if scenarioId == None:  # 전체조회
            scenario_list = os.listdir(self.dir_path)
            for scenario in scenario_list:
                with open(self.dir_path+scenario, 'r') as file:
                    json_file = json.load(file)
                    get_list.append(json_file)
            response_data = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_list}
            result = marshal(response_data, response_form)
            return result

        else:  # 해당id 조회
            scenario_json = scenarioId.split(".")[0]+'.json'
            with open(self.dir_path + scenario_json, 'r') as file:
                json_file = json.load(file)
                get_list.append(json_file)
            response_data = {'code': 200, 'message': 'success', 'errorPos': [], 'results': get_list}
            result = marshal(response_data, response_form)
            return result

    def update(self, packageName, data):
        return

    def create(self, data):
        json_data = marshal(data, Scenario_model)
        json_file = json_data["scenarioId"] + '.json'
        scenario_path = self.dir_path + json_file
        if os.path.exists(scenario_path):
            api.abort(404, "{} already exists".format(scenario_path))  # HTTPException 처리
        else:
            with open(scenario_path, 'w',encoding='utf-8') as file:
                json.dump(json_data, file, indent="\t")
            return json_data

    def delete(self, scenarioId):
        scenario_path = self.dir_path + scenarioId.split(".")[0] + '.json'
        if os.path.exists(scenario_path):
            os.remove(scenario_path)
        else:
            api.abort(404, "{} module doesn't exists".format(scenario_path))  # HTTPException 처리

scenario = ScenarioDAO() # DAO 객체를 만든다

@api.route('/') # 네임스페이스 x.x.x.x/package/ 라우팅
class ListManager(Resource):
    def get(self):
        ''' scenario 조회 '''
        return scenario.get(None)

    @api.expect(Scenario_model)
    @api.marshal_with(Scenario_model, code=201)
    def post(self):
        '''새로운 scenario 생성'''
        return scenario.create(api.payload), 201


@api.route('/<string:scenarioId>') # 네임스페이스 x.x.x.x/package/name 라우팅
@api.response(404, 'scenarioId를 찾을 수가 없어요')
@api.param('scenarioId', 'scenarioId를 입력해주세요')
class RUDManager(Resource):
    def get(self, scenarioId):
        return scenario.get(scenarioId)

    def put(self, scenarioId):
        scenario.update(scenarioId, api.payload)
        return

    @api.response(204, 'scenario deleted')
    def delete(self, scenarioId):
        '''해당 scenario 삭제'''
        scenario.delete(scenarioId)
        return '', 204
