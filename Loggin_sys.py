###MYSQL-Python-User_Interface###:
import Euler_algor
import Config_handler
import os
import csv
import MYSQL_Connection


##Login system##
data_path = '\\Data\\'
filename = 'Config.ini'
data_path2 = '\\Data\\'
filename2 = 'user_passwords.csv'
curfile = str(__file__)


def get_user_csv(filename3, data_path3, curfile3):
     path = os.path.realpath(os.path.dirname(curfile3)) + data_path3 + filename3
     user_array = []
     with open(path, newline = '') as csvfile:
          csv_data = csv.reader(csvfile, delimiter=',', quotechar='|')
          user_array = list(csv_data)
     return user_array


def write_user_csv(filename3, data_path3, curfile3, write_data3):
     path = os.path.realpath(os.path.dirname(curfile3)) + data_path3 + filename3
     fieldnames = ['username','password','host','database']
     with open(path, 'a', newline = '') as csvfile:
          csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
          csv_writer.writerow(write_data3)


def get_user_csv_dict(filename3, data_path3, curfile3):
     path = os.path.realpath(os.path.dirname(curfile3)) + data_path3 + filename3
     user_dict = []
     with open(path, newline = '') as csvfile:
          csv_data = csv.DictReader(csvfile)
          for row in csv_data:
               user_dict.append(row)
     return user_dict


def clean_csv_arrays(string):
     string = string.replace(',', '')
     string = string.replace('[', '')
     string = string.replace(']', '')
     string = string.split(' ')
     array = list(map(int, string))
     return array
     


def check_Euler(config_obj):
     #Check Euler object has been created for the system:
     header = 'log-in'
     var = 'Euler_created'
     is_Euler = bool(config_obj.return_value(header, var))
     Euler_obj = None
     if not is_Euler:
          Euler_obj = Euler_algor.Euler_algor_obj(True)
          Euler_obj.write_vars_to_config()
          config_obj.refresh_config_obj()
     else:
          Euler_obj = Euler_algor.Euler_algor_obj(False)
     config_obj.write_to_config('log-in', ['euler_created'], ['1'])
     return Euler_obj





class session_user():
     def __init__(self, username, password, host, database):
          self.username = username
          self.password = password
          self.host = host
          self.database = database
          self.connection_name = 'connection1'
          self.connection_obj = MYSQL_Connection.mysql_connection(self.username, self.password, self.host, self.database)


         

class login_handler():
     def __init__(self):
          #Create the config object for the log-in system:
          self.config_obj =  Config_handler.config_obj(data_path, filename, curfile)
          self.Euler_obj = check_Euler(self.config_obj)
          self.valid_user = False
          self.username = ''
          self.password = ''
          self.host = ''
          self.database = ''
          self.user_obj = None
          self.is_user = False

     def take_username_and_password(self, username, password):
          self.username = username
          self.password = password

     def check_username_password(self):
          user_found = False
          password_found = False
          user_array = get_user_csv_dict(filename2, data_path2, curfile)
          for row in user_array:
               act_user = self.Euler_obj.decrypt_string(clean_csv_arrays(row['username']))
               act_password = self.Euler_obj.decrypt_string(clean_csv_arrays(row['password']))
               if act_user == self.username and act_password == self.password:
                    user_found = password_found = True
                    self.username = act_user
                    self.password = act_password
                    self.host = row['host']
                    self.database = row['database']
                    break
               
          if user_found and password_found:
               self.valid_user = True

     def create_session_user(self):
          if self.valid_user:
               new_user = session_user(self.username, self.password, self.host, self.database)
               self.user_obj = new_user
               return self.user_obj
          else:
               return False





class create_new_user_handler():
     def __init__(self, username, password, host, database):
          self.config_obj = Config_handler.config_obj(data_path, filename, curfile)
          self.Euler_obj = check_Euler(self.config_obj)
          self.valid_user = False
          self.username = username
          self.password = password
          self.host = host
          self.database = database
          self.unacceptable_characters = [':',';','.',',','[',']','{','}','/','?','|', '"\"', '"', "'", '=' ,'+', '#', '~', '@', '*', '&', '^', '%', '$,' ,'£', '!']
          self.csv_data = {
               'username': self.Euler_obj.encrypt_string(self.username),
               'password': self.Euler_obj.encrypt_string(self.password),
               'host': self.host,
               'database': self.database
               }

     def check_username(self):
          acceptable_user = True
          already_user = False
          
          #Check acceptable:
          for i in self.username:
               if i in self.unacceptable_characters:
                    acceptable_user = False
          print(acceptable_user)
                    
          #Check in use:
          user_array = get_user_csv_dict(filename2, data_path2, curfile)
          for row in user_array:
               act_user = self.Euler_obj.decrypt_string(clean_csv_arrays(row['username']))
               if act_user == self.username:
                    print(act_user, self.username)
                    already_user = True
          print(already_user)

          is_connected = self.check_connection()
          print(is_connected)
                    
          if not acceptable_user or already_user or not is_connected:
               self.valid_user = False
          else:
               self.valid_user = True
               self.write_to_users_csv()

     def check_connection(self):
          connector = MYSQL_Connection.mysql_connection(self.username, self.password, self.host, self.database)
          is_connected = connector.test_connection()
          return is_connected

     def write_to_users_csv(self):
          #Josh64,Joshua100,127.0.0.1,world
          user_dict = get_user_csv_dict(filename2, data_path2, curfile)
          write_user_csv(filename2, data_path2, curfile, self.csv_data)

     def create_session_user(self):
          if self.valid_user:
               new_user = session_user(self.username, self.password, self.host, self.database)
               self.user_obj = new_user
               return self.user_obj
          else:
               return False



"""
#Test1: Create User:
username = 'James24'
password = 'Joshua100x'
host = '127.0.0.2'
database = 'world'
user = create_new_user_handler(username, password, host, database)
TF = user.check_username()
print(TF)



#Test1:
login_obj = login_handler()
username = 'James24'
password = 'Joshua100T'
login_obj.take_username_and_password(username, password)
TF = login_obj.check_username_password()
print(TF)


#Test2:
login_obj = login_handler()
username = 'James24'
password = 'Joshua100x'
login_obj.take_username_and_password(username, password)
TF = login_obj.check_username_password()
print(TF)
"""
