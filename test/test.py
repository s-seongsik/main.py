from pyspark import SparkContext, SparkConf, SQLContext
from pandas import DataFrame
import pandas as pd

'''
# 1. JDBC driver for SQL Server
# 설명 : JDBC는 자바에서 데이터베이스에 접속할 수 있도록 하는 자바 API이다. JDBC는 데이터베이스에서 자료를 쿼리하거나 업데이트하는 방법을 제공한다.
'''

appName = "PySpark SQL Server Example - via JDBC"
master = "local"
jdbc_path = "../JDBC_Driver/sqljdbc_8.4/kor/mssql-jdbc-8.4.1.jre8.jar"
conf = SparkConf()\
    .setAppName(appName) \
    .setMaster(master) \
    .set("spark.driver.extraClassPath",jdbc_path)
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession

host = "wizcore.iptime.org"
port = "4085"
database = "nexpom_mando"
table = "PROC_DTL"
user = "sa"
password  = "wizcore"

jdbcDF = spark.read.format("jdbc") \
    .option("url", f"jdbc:sqlserver://{host}:{port};databaseName={database}") \
    .option("dbtable", table) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load()
jdbcDF.show()

jdbcDF.select(jdbcDF.colRegex("IPT_NO","DTL_RESULT")).show()
jdbcDF.columns

"""
# 1. ODBC driver and pyodbc package
# 설명 : ODBC는 마이크로소프트가 만든, 데이터베이스에 접근하기 위한 소프트웨어의 표준 규격
"""
from pyspark import SparkContext, SparkConf, SQLContext
import pyodbc
import pandas as pd

appName = "PySpark SQL Server Example - via ODBC"
master = "local"
conf = SparkConf() \
    .setAppName(appName) \
    .setMaster(master)
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession

database = "test"
table = "dbo.Employees"
user = "zeppelin"
password  = "zeppelin"

conn = pyodbc.connect(f'DRIVER={{ODBC Driver 13 for SQL Server}};SERVER=localhost,1433;DATABASE={database};UID={user};PWD={password}')
query = f"SELECT EmployeeID, EmployeeName, Position FROM {table}"
pdf = pd.read_sql(query, conn)
sparkDF =  spark.createDataFrame(pdf)
sparkDF.show()

"""
# 1 : 
"""
from pyspark import SparkContext, SparkConf, SQLContext
import _mssql
import pandas as pd

appName = "PySpark SQL Server Example - via pymssql"
master = "local"
conf = SparkConf() \
    .setAppName(appName) \
    .setMaster(master)
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
spark = sqlContext.sparkSession

database = "test"
table = "dbo.Employees"
user = "zeppelin"
password  = "zeppelin"

conn = _mssql.connect(server='localhost:1433', user=user, password=password,database=database)
query = f"SELECT EmployeeID, EmployeeName, Position FROM {table}"
conn.execute_query(query)
rs = [ row for row in conn ]
pdf = pd.DataFrame(rs)
sparkDF = spark.createDataFrame(pdf)
sparkDF.show()
conn.close()









function_add

function_add.iloc[:,:]

function_add = pd.DataFrame({'input_data1':[100],'input_data2':[200],'input_data3':[300]})
spark.createDataFrame(function_add)
result = function_add['input_data1']+function_add['input_data2']+function_add['input_data3']
df.loc[:,:]