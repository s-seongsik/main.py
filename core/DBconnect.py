from configparser import ConfigParser
from pyspark.sql import SparkSession
import pandas as pd


class connect_to_sql:
    def __init__(self, datasource, sql):
        self.JDBC_Driver_PATH = "./JDBC_Driver/sqljdbc_8.4/kor/mssql-jdbc-8.4.1.jre8.jar"
        self.config_name = datasource
        self.query = sql

    def set_config(self):
        config = ConfigParser()
        config.read('./resource/config/config.ini', encoding='utf-8')
        return config

    def run(self):
        config = self.set_config()
        url = f"jdbc:sqlserver://{config.get(self.config_name, 'host')}:{config.get(self.config_name, 'port')};database={config.get(self.config_name, 'database')}"
        spark = (SparkSession
                 .builder
                 .appName("PySpark with SQL server")
                 .config("spark.driver.extraClassPath", self.JDBC_Driver_PATH)
                 .getOrCreate())
        # Enable Arrow-based columnar data transfers
        spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

        # PySpark와 pandas 데이터 프레임 간의 변환 최적화
        sdf = spark.read\
            .format("jdbc")\
            .option("url",url)\
            .option("dbtable",'(' + self.query + ')' + ' AS TEST')\
            .option("user",config.get(self.config_name, 'user'))\
            .option("password",config.get(self.config_name, 'password')) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .load()
        pdf = sdf.select("*").toPandas()

        return pdf
