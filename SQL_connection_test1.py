###SQL connection test1###:
import mysql.connector

user = 'root'
password = 'Joshua100x'
host = '127.0.0.1'
database = 'world'
select_all_table_data = ("SELECT * FROM {}")
table_name = 'new_table1'

connector = mysql.connector.connect(
                user = user,
                password = password,
                host = host,
                database = database)


#Get table data test:
curA = None
#create cursor:
curA = connector.cursor(buffered=True)
select_table_data_statement = select_all_table_data.format(table_name)
curA.execute(select_table_data_statement)
data = curA.fetchall()
if curA:
     curA.close()
