###MYSQL-Python-User_Interface###:
import Euler_algor
import Config_handler
import os
import csv
import mysql.connector

##MYSQL-Connection##
class mysql_connection():
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.connection_name = ''
        self.connection_details = {}
        self.connection = None
        self.uncommited_changes = True
        self.turn_off_autocommit = ("SET autocommit = 0")
        self.create_table_statement = ("CREATE TABLE {} ({})")
        self.delete_table_statement = ("DROP TABLE IF EXISTS {}")
        self.create_database_statement = ("CREATE DATABASE {}")
        self.delete_database_statement = ("DROP DATABASE {}")
        self.show_databases_statement = ("SHOW DATABASES")
        self.show_tables_in_database_statement = ("SHOW TABLES IN {}")
        self.show_columns_in_table_statement = ("SHOW COLUMNS IN {}")
        self.select_all_table_data = ("SELECT * FROM {}")
        self.database_blacklist = ['information_schema', 'mysql', 'performance_schema', 'sakila', 'sys']
        self.use_database_statement = ("USE {}")
        self.last_statement = ""


    def use_database(self, database, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            curA = connector.cursor(buffered=True)
            use_statement = self.use_database_statement.format(database)
            curA.execute(use_statement)
            curA.close()
        except:
            print("use_database")
            return1 = False
        else:
            return1 = True
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
            


    def pass_back_cursor(self, connection_name):
        return1 = None
        curA = None
        try:
            connector = self.connection
            curA = connector.cursor(buffered=True)
            curA.close()
        except:
            return1 = False
        else:
            return1 = curA
        finally:
            if curA:
                curA.close()
            return return1
        

    def get_database_names(self, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        try:
            databases = list(self.connection_details.keys())
        except:
            return1 = False
        else:
            return1 = databases
        finally:
            self.terminate_all_connections()
            return return1


    def run_select_statement(self, connection_name, statement):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            curA = connector.cursor(buffered=True)
            curA.execute(str(statement))
            data = curA.fetchall()
            return1 = data
        except:
            return1 = False
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
            
        

    def get_table_names(self, database_name, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        try:
            table_names = list(self.connection_details[database_name].keys())
        except:
            return1 = False
        else:
            return1 = table_names
        finally:   
            self.terminate_all_connections()
            return return1

    def get_table_attributes(self, table_name, connection_name):
        return1 = None
        print('1')
        self.setUp_connection(connection_name)
        print('2')
        curA = None
        try:
            connector = self.connection
            print('2')
            #create cursor
            curA = connector.cursor(buffered=True)
            print('2')
            select_table_attribute = self.show_columns_in_table_statement.format(table_name)
            print('2')
            curA.execute(select_table_attribute)
            print('3')
        except:
            print('4')
            return1 = False
        else:
            data = curA.fetchall()
            print('5')
            attributes = [attribute[0] for attribute in data]
            print('6')
            return1 = attributes
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
            

    def get_table_data(self, table_name, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            #create cursor:
            curA = connector.cursor(buffered=True)
            select_table_data_statement = self.select_all_table_data.format(table_name)
            curA.execute(select_table_data_statement)
        except:
            return1 = False
        else:
            data = curA.fetchall()
            return1 = data
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
        

    def refresh_connection(self, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        try:
            connector = self.connection
            connector.config(database = self.database)
            #This will rollback any uncommited changes
            connector.reconnect()
            self.get_connection_details(connection_name)
        except:
            return1 = False
        else:
            return1 = True
        finally:
            self.terminate_all_connections()
            return return1
        

    def commit_changes(self, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        try:
            connector = self.connection
            connector.commit()
        except:
            return1 = False
        else:
            return1 = True
        finally:
            self.terminate_all_connections()
            return return1
        

    def rollback_changes(self, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        try:
            connector = self.connection
            connector.rollback()
        except:
            return1 = False
        else:
            return1 = True
        finally:
            self.terminate_all_connections()
            return return1
        
    
    def create_new_database(self, database_name, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            #create cursor:
            curA = connector.cursor(buffered=True)
            #Turn off autcommit:
            curA.autocommit = False
            database_creation_statement = self.create_database_statement.format(database_name)
            curA.execute(database_creation_statement)
            curA.close()
            self.connection_details.update({database_name:{}})
            self.last_statement = database_creation_statement
        except:
            return1 = False
        else:
            return1 = True
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
        

    def delete_database(self, database_name, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            #create cursor:
            curA = connector.cursor(buffered=True)
            #Turn off autcommit:
            curA.autocommit = False
            database_deletion_statement = self.delete_database_statement.format(database_name)
            curA.execute(database_deletion_statement)
            self.last_statement = database_deletion_statement
        except:
            return1 = False
        else:
            return1 = True
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1
        

    def create_new_table(self, table_name, attributes, attribute_types, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        if len(attributes) != len(attribute_types):
            raise Exception("attibutes and attribute_types, are not the same length")
        else:
            try:
                attributes_types_string = ''
                for i in range(len(attributes)):
                    attributes_types_string += attributes[i] + ' ' + attribute_types[i]
                    if i != 0 or len(attributes) -1:
                        attributes_types_string += ','
                connector = self.connection
                #create cursor:
                curA = connector.cursor(buffered=True)
                #Turn off autcommit:
                curA.autocommit = False
                table_creation_statement = self.create_table_statement.format(self.database+"."+table_name, attributes_types_string[:-1])
                curA.execute(table_creation_statement)
                curA.close()
                self.connection_details[self.database].update({table_name:attributes})
                self.last_statement = table_creation_statement
            except:
                return1 = False
            else:
                return1 = True
            finally:
                if curA:
                    curA.close()
                self.terminate_all_connections()
                return return1
        return False


    def delete_table(self, table_name, connection_name):
        return1 = None
        self.setUp_connection(connection_name)
        curA = None
        try:
            connector = self.connection
            #create cursor:
            curA = connector.cursor(buffered=True)
            #Turn off autcommit:
            curA.autocommit = False
            table_deletion_statement = self.delete_table_statement.format(table_name)
            curA.execute(table_deletion_statement)
            curA.close()
            self.connection_details[self.database].pop(table_name)
            self.last_statement = table_deletion_statement
        except:
            return1 = False
        else:
            return1 = True
        finally:
            if curA:
                curA.close()
            self.terminate_all_connections()
            return return1

    def get_connection_details(self, connection_name):
        return1 = None
        curA = None
        curB = None
        curC = None
        try:
            connection_details_dict = {}
            #Get Databases:
            connector = self.connection
            curA = connector.cursor(buffered=True)
            curB = connector.cursor(buffered=True)
            curC = connector.cursor(buffered=True)
            
            curA.execute(self.show_databases_statement)
            for database in curA:
                if database[0] not in self.database_blacklist:
                    database_tables_query = self.show_tables_in_database_statement.format(database[0])
                    connection_details_dict.update({database[0]: {}})
                    curB.execute(database_tables_query)
                    
                    for table in curB:
                        columns_table_query = self.show_columns_in_table_statement.format(database[0]+'.'+table[0])
                        curC.execute(columns_table_query)
                        
                        attribute_array = [attribute[0] for attribute in curC]
                        
                        connection_details_dict[database[0]].update({table[0]: attribute_array})
        except:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return1 = False
        else:
            self.connection_details = connection_details_dict
            return1 = True
        finally:
            if curA:
                curA.close()
            if curB:
                curB.close()
            if curC:
                curC.close()
            return return1


    def setUp_connection(self, connection_name):
        return1 = None
        try:
            connector = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database)
            self.connection = connector
        except:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return1 = False
        else:
            is_connected = self.get_connection_details(connection_name)
            print(is_connected)
            self.connection_name = connection_name
            return1 = True
        return return1


    def change_database(self, database_name, connection_name):
        return1 = None
        if database_name == self.database:
            return True, 1
        try:
            connector = self.connection
            connector.config(database = database_name)
            #This will rollback any uncommited changes
            connector.reconnect()
            self.database = database_name
        except:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return1 = False, 1
        else:
            return1 = True, 2
        finally:
            self.terminate_all_connections()
            return return1

            
    def test_connection(self):
        return1 = None
        connector = None
        try:
            connector = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database)
            connector.close()
        except:
            return1 = False
        else:
            return1 = True
        finally:
            if connector:
                connector.close()
            return return1
                

    def terminate_all_connections(self):
        if not self.connection:
            return False
        connector = self.connection
        connector.close()
        self.connection = None
        return True

    def turn_off_clients_autocommit(self):
        config_obj = Config_handler.config_obj(data_path, filename, curfile)
        config_obj.find_mysql_config_file()
        status_code = config_obj.set_auto_commit_zero()
        return status_code[-1]



"""
#Test1:
user = 'root'
password = 'Joshua100x'
host = '127.0.0.1'
database = 'world'
connection_name = 'connection1'
mysql_connector = mysql_connection(user, password, host, database)
mysql_connector.setUp_connection(connection_name)
mysql_connector.get_connection_details(connection_name)
for connection in mysql_connector.connection_details.items():
    print('\n', connection,'\n')


#Test2:
table_name = 'clients'
user = 'root'
password = 'Joshua100x'
host = '127.0.0.1'
database = 'sql_invoicing'
connection_name = 'connection1'
mysql_connector = mysql_connection(user, password, host, database)
mysql_connector.setUp_connection(connection_name)
mysql_connector.get_connection_details(connection_name)

#Test table attribues and data
table_connections = mysql_connector.get_table_data(table_name, connection_name)
table_attributes = mysql_connector.get_table_attributes(table_name, connection_name)
table_names = mysql_connector.get_table_attributes(table_name, connection_name)
print(table_names)
print(table_attributes)
print(table_connections)

#Test table and database creation:
database_names = mysql_connector.get_database_names(connection_name)
print(database_names)

#Test if the connector can add a new database (and if it apears in connection_details) and if it only existis in the session like its supposed to:
database_names = mysql_connector.get_database_names(connection_name)
print(database_names)
mysql_connector.create_new_database('database1', connection_name)
database_names = mysql_connector.get_database_names(connection_name)
print(database_names)
mysql_connector.refresh_connection(connection_name)
database_names = mysql_connector.get_database_names(connection_name)
print(database_names)


#Tets if the connector can add a new table (and if it apears in connection_details) and if it only existis in the session like its supposed to:
print('hi')
table_name = 'customers'
attributes = ['name']
attribute_types = ['VARCHAR(25)']
table_names = mysql_connector.get_table_names(database, connection_name)
print(table_names)
is_created = mysql_connector.create_new_table(table_name, attributes, attribute_types, connection_name)
print(is_created)
table_names = mysql_connector.get_table_names(database, connection_name)
print(table_names)
mysql_connector.terminate_all_connections()

#Test to see if the tables are on autocommit:
#Result: They are :(:
mysql_connector.refresh_connection(connection_name)
table_names = mysql_connector.get_table_names(database, connection_name)
print(table_names)


#Delete table:
table_name = 'customers'
table_names = mysql_connector.get_table_names(database, connection_name)
print(table_names)
is_deleted = mysql_connector.delete_table(table_name, connection_name)
print(is_deleted)
table_names = mysql_connector.get_table_names(database, connection_name)
print(table_names)
"""

