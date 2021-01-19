from configparser import ConfigParser
from pyspark.sql import SparkSession

config = ConfigParser()
config.read('./resource/config/config.ini', encoding='utf-8')

jdbc_url = f"jdbc:sqlserver://{config.get('mydb', 'host')}:{config.get('mydb', 'port')};database={config.get('mydb', 'database')}"
connection_properties = {
    "user": config.get('mydb', 'username'),
    "password": config.get('mydb', 'password')
}


jars = ["./JDBC_Driver/sqljdbc_8.4/kor/mssql-jdbc-8.4.1.jre8.jar",]
spark = (SparkSession
  .builder
  .appName("PySpark with SQL server")
  .config("spark.driver.extraClassPath", ":".join(jars))
  .getOrCreate())

schema = 'dbo'
table = 'PROC_DTL'

df = spark \
    .read \
    .jdbc(jdbc_url,
          f"{schema}.{table}",
          properties=connection_properties)
