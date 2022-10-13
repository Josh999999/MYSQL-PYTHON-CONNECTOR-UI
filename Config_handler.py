###Python-MYSQL-User_Interface###:
from configparser import ConfigParser
import os.path
import shutil

data_path = '\\Data\\'
filename = 'Config.ini'
curfile = str(__file__)

##Config_handler##:
class config_obj:
     def __init__(self, data_path, filename, curfile):
          self.special_characters = [':',';','.',',','[',']','{','}','/','?','|', '"\"', '"', "'", '=' ,'+', '#', '~', '@', '*', '&', '^', '%', '$,' ,'£', '!']
          self.data_path = data_path
          self.filename = filename
          self.curfile = curfile
          self.config_filepath = ''
          self.mysql_config_default_path = "C:\ProgramData\MySQL\MySQL Server 8.0\my.ini"
          self.mysql_config_file = 'my.ini'
          self.mysql_config_filepaths = []
          self.mysql_act_config_filepath = ''
          self.config_obj = self.create_config_obj(False)
          self.mysql_config_obj = self.create_mysql_config_obj()
          self.mysql_config_header = 'mysqld'

     def create_mysql_config_obj(self):
          self.find_mysql_config_file()
          config_obj = self.create_config_obj(True)
          print(self.mysql_act_config_filepath)
          print('hi')
          return config_obj
          
     def create_config_obj(self, mysql):
          print('hi')
          config_filepath = self.mysql_act_config_filepath
          print('hi')
          dir_path = os.path.dirname(os.path.realpath(self.curfile))
          print('hi')
          print(config_filepath)
          print('hi')
          
          if mysql is False:
               print('hi')
               config_filepath = dir_path + self.data_path + self.filename
               self.config_filepath = config_filepath
               print(config_filepath)
               print('hi')
          print(config_filepath)
               
          exists = os.path.exists(config_filepath)
          config = None
          if exists:
               print("------------Config.ini exists at:", dir_path + self.data_path)
               config = ConfigParser(allow_no_value=True)
               print('hi')
               config.read(config_filepath, encoding='utf-8')
               print('hi')
          else:
               raise Exception("------------Config.ini does not exists at:", dir_path + self.data_path)
          return config

     def refresh_config_obj(self):
          config = ConfigParser()
          config.read(self.config_filepath, encoding='utf-8')
          self.config_obj = config

     def return_optionVal_array(self, header, var):
          if type(self.config_obj[header][var]) == str:
               clean_array = self.Clean_config_arrays(header, var)
               return clean_array
          else:
               print(self.config_obj[header][var], 'is type:', str(type(self.config_obj[header][var]))+'.', 'Not <list>')
          return None

     def Clean_config_arrays(self, header, var):
          try:
               string = self.config_obj[header][var]
               string = string.replace(',', '')
               string = string.replace('[', '')
               string = string.replace(']', '')
               array = string.split(' ')
               print(array)
               return array
          except:
               return None

     def return_value(self, header, var):
          return self.config_obj[header][var]

     def write_to_config(self, header, keys, values):
          available_keys = list(self.config_obj[header].keys())
          try:
               for i in range(len(keys)):
                    if keys[i] in available_keys:
                         self.config_obj[header][keys[i]] = str(values[i])
                         print(values[i])
                    else:
                         self.config_obj[header].update({keys[i]:str(values[i])})
               with open(self.config_filepath, 'w') as file_object:
                    self.config_obj.write(file_object)
          except:
               raise Exception("Number of keys and pairs do not math")


     def find_mysql_config_file(self):
          #Create and array of all directories:
          directories = os.path.dirname(self.mysql_config_default_path).split("\\")[1:]
          
          #Attempt1: Try to use the standard filepath for this (The configparser can hanlde .cnf and .ini files):
          if os.path.exists(self.mysql_config_default_path):
               self.mysql_config_filepaths = [self.mysql_config_default_path]
               self.mysql_act_config_filepath = self.mysql_config_default_path
               return True

          #Attempt2: Go through the main MYSQL download location and look for it there:
          paths1 = None
          looked_paths = []
          if not file_found:
               for i in range(len(directories), 0, -1):
                    check_looked_at = True
                    bypass = False
                    if i >= len(directories):
                         check_looked_at = False
                         bypass = True

                    prev_direct_index = 'C:\\' +  '\\'.join(directories[0:i + 1])
                    direct_index = 'C:\\' +  '\\'.join(directories[0:i])
                    difference_index_num = len(prev_direct_index)
                    
                    paths2 = self.walk_file_tree(direct_index, check_looked_at, difference_index_num, looked_paths, bypass)
                    if paths2 and paths1:
                         paths1 += paths2
                    elif paths2 and not paths1:
                         paths1 = []
                         paths1 += paths2
                    looked_paths.append(direct_index)

               if paths1:
                    self.mysql_config_filepaths = paths1
                    self.mysql_act_config_filepath = paths1[0]
                    return paths1
          return None

     def walk_file_tree(self, directory, check_looked_at, difference_index_num, looked_paths, bypass):
          paths = None
          tree = os.walk(directory)
          for i, j, k in tree:
               if check_looked_at and i[0:difference_index_num] not in looked_paths or bypass:
                    if self.mysql_config_file in k and not paths:
                         paths = []
                         path = i + "\\" + self.mysql_config_file
                         paths.append(path)
                    elif self.mysql_config_file in k and paths and k not in paths:
                         path = i + "\\" + self.mysql_config_file
                         paths.append(path)
          return paths

     def set_auto_commit_zero(self):
          try:  
               self.mysql_config_obj[self.mysql_config_header]['autocommit'] = 0
               assert os.path.isfile(self.mysql_act_config_filepath)
               with open(self.mysql_act_config_filepath, 'w') as file_object:
                    self.mysql_config_obj.write(file_object)
          except:
               #raise Exception("python does not have permission to change the config file, or --: " + self.mysql_act_config_filepath + " is not a file (it could be a directory, or a reference point)")
               return False, 1
          else:
               return True, 0
          
               
#Test0: See if it works:
config_test_obj = config_obj(data_path, filename, curfile)
paths = config_test_obj.find_mysql_config_file()
print(paths)


"""
#Tets1: Returns the users home directory:
print(os.environ)
print(os.environ['HOME'])

#Test2:
print(os.fspath('C:\ProgramData\MySQL\MySQL Server 8.0'))
print(os.fspath('my.ini'))

dict1 = {'PATH':'my.ini'}
print(os.get_exec_path(dict1))
"""

"""
#Test3: Add another file called 'my.ini. in the default directory:
config_test_obj = config_obj(data_path, filename, curfile)
paths = config_test_obj.find_mysql_config_file()
print(paths)

#Test4: set autocommit to 0:
config_test_obj = config_obj(data_path, filename, curfile)
paths = config_test_obj.find_mysql_config_file()
print(paths)
config_test_obj.set_auto_commit_zero()
"""
