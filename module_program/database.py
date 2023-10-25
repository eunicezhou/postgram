import mysql.connector
from mysql.connector import pooling
from module_program.env_key import *

con_password = os.getenv('DATABASE_PASSWORD')
con ={
    'user':'admin',
    'password':con_password,
    'host':'postgram.cragb4dlrndi.ap-northeast-1.rds.amazonaws.com',
    'database':'postgram',
}
# 建立連接池
connection_pool = pooling.MySQLConnectionPool(pool_name='postgram',pool_size=5,**con)

def connect(execute_str,execute_argument=None):
	connection = connection_pool.get_connection()
	cursor = connection.cursor()
	try:
		cursor.execute("USE postgram")
		cursor.execute(execute_str,execute_argument)
		result = cursor.fetchall()
		connection.commit()
	except Exception as err:
		print(err)
		result = None
	finally:
		cursor.close()
		connection.close()
	return result