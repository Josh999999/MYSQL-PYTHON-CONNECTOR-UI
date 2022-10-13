###Python-MYSQL-User_Interface###:
from Config_handler import config_obj
import os.path

##Find Primes file - Turn to array

def check_prime(primes_array_var):
     prime_checkers = [2,3,5,7,11]
     #Quick test for a short list:
     for i in prime_checkers:
          if primes_array_var not in prime_checkers and primes_array_var % i == 0:
               return False
     return True

def cull_non_primes(primes_array):
     for i in range(len(primes_array)):
          is_prime = check_prime(primes_array[i])
          if not is_prime:
               primes_array = primes_array.pop(i)
     return primes_array
     
def find_primes_turn_to_array(data_path, filename, curfile, header, var):
     import_config_obj = config_obj(data_path, filename, curfile)
     primes_array = []
     try:
          primes_array = list(map(int, import_config_obj.return_optionVal_array(header, var)))
     except:
          raise Exception("Not all of these are integers")
     org_primes_array = primes_array
     primes_array = cull_non_primes(primes_array)
     #Code to check if numbers have been removed: print(same_list(org_primes_array, primes_array))
     return primes_array

def same_list(org, new):
     if hash(str(org)) == hash(str(new)):
          return True
     return False

def find_Eulers_numbers(data_path, filename, curfile, header):
     Eulers_numbers = {
          'p':0,
          'q':0,
          'n':0,
          'thi':0,
          'e':0,
          'd':0
          }
     import_config_obj = config_obj(data_path, filename, curfile)
     items = list(import_config_obj.config_obj[header].items())
     for item in items:
          if item[0] in Eulers_numbers.keys():
               Eulers_numbers[item[0]] = int(item[1])
     return Eulers_numbers
     
