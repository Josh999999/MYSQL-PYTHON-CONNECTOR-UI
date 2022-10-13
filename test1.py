import mysql.connector

user = 'root'
password = 'Joshua100x'
host = '127.0.0.1'
database = 'world'


connector = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database)

curA = connector.cursor()
curA.execute("SELECT Code,Name,Continent FROM world.country WHERE Code = 'data'")
data = curA.fetchall()
print(data)
