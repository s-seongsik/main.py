from flask_restplus import Api,Namespace,fields
from apis.datasource import api as datasource
from apis.package import api as package
from apis.module import api as module
from apis.script import api as script
from apis.scenario import api as scenario
from apis.run import api as run

# Apis 모듈 집계
api = Api(
    title='넥스폼 데이터 처리 엔진',
    version='1.0',
    description='모니터링에 사용 될 Row Data Import/Processing/Analysis 처리 엔진'
    # All API metadatas
)
api.add_namespace(datasource)
api.add_namespace(package)
api.add_namespace(module)
api.add_namespace(script)
api.add_namespace(scenario)
api.add_namespace(run)