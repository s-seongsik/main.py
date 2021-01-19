import os.path
import pandas as pd
import json
from core import sql_run
from flask_restplus import Namespace, Resource, fields,marshal
api = Namespace('run', description='시나리오 구동')

# 모델정의
Run_model = api.model('Run', {
    'scenarioId' : fields.String(required=True),
    'data' : fields.List
})

class RunDAO(object):
    def __init__(self):
        self.dir_path = './resource/scenario/'

    def get(self, scenarioId):
        scenario_json = scenarioId.split(".")[0]+'.json'
        with open(self.dir_path + scenario_json, 'r') as file:
            json_file = json.load(file)
        datasource = json_file["recipes"]['datasource']
        query = json_file["recipes"]['sql']
        pdf = sql_run(datasource, query)
        return_data = json.loads(pdf.head(20).to_json())
        return {"data" : return_data}

Run = RunDAO() # DAO 객체를 만든다

@api.route('/<string:scenarioId>') # 네임스페이스 x.x.x.x/package/ 라우팅
@api.response(404, 'scenarioId를 찾을 수가 없어요')
@api.param('scenarioId', 'scenarioId를 입력해주세요')
class ListManager(Resource):

    def get(self, scenarioId):
        '''script 생성'''
        return Run.get(scenarioId)
