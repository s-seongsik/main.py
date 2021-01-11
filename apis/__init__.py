from flask_restplus import Api,Namespace,fields
from apis.datasource import api as datasource
from apis.package import api as package
from apis.module import api as module
from apis.script import api as script

# Apis 모듈 집계
api = Api(
    title='넥스폼 데이터 처리 엔진',
    version='1.0',
    description='넥스폼에 사용될 데이터를 IMPORT/가공/분석 처리하는 파이썬 엔진 시스템'
    # All API metadatas
)
api.add_namespace(datasource)
api.add_namespace(package)
api.add_namespace(module)
api.add_namespace(script)