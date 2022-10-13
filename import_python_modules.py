###Python-MYSQL-User_Interface###:
import pip
import importlib.util
import subprocess
import sys
import os
try:
     from Config_handler import config_obj
except:
     os.system('cmd /c "pip install Config_handler"')


##Import_python_modules##:
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
flat_installed_packages = [r.decode().split('==')[0] for r in installed_packages.split()]
print(flat_installed_packages)
data_path = '/Data/'
filename = 'Config.ini'
curfile = str(__file__)
header = 'Modules'
var = 'Modules'


class imports_handler:
     def __init__(self):
          self.modules_array = self.Import_python_modules_array()
          self.file_installed_packages = []
          self.uninstalled_packages = []
          
     def Import_python_modules_array(self):
          import_config_obj = config_obj(data_path, filename, curfile)
          modules_array = import_config_obj.return_optionVal_array(header, var)
          if not modules_array:
               raise Exception("------------"+filename,"has no value",var,"at header",header)
          return modules_array

     def Check_modules_installed(self):
          for module in self.modules_array:
               if module in flat_installed_packages:
                    self.file_installed_packages.append(module)
               else:
                    self.uninstalled_packages.append(module)

          if hash(str(self.file_installed_packages)) == hash(str(self.modules_array)):
               return True
          return False

     def add_uninstalled_module_S(self, check):
          if check:
               self.Check_modules_installed()
          for module in self.uninstalled_packages:
               self.add_module_S(module)

     def install_uninstalled_module_S(self, check):
          if check:
               self.Check_modules_installed()
          for module in self.uninstalled_packages:
               self.install_module(module)  

     def install_module(self, module):
          print(self.uninstalled_packages)
          try:
               if hasattr(pip, 'main'):
                    pip.main(['install', module])
               else:
                    pip._internal.main(['install', module])
          except:
               raise Exception("module:",module,". Does not exist")
          
     def add_module_S(self, modules):
          if type(modules) == str:
               spec = importlib.util.find_spec(modules)
               module = importlib.util.module_from_spec(spec)
               sys.modules[module] = module
               spec.loader.exec_module(module)
               print(f"{module!r} has been imported")
          elif type(modules) == list:
               for module in modules:
                    self.add_module_S(module)
          else:
               raise Exception("type:",type(modules),"not accepted")

"""
#Test1:              
i = imports_handler()
print(i.modules_array)
i.install_uninstalled_module_S(True)
"""
