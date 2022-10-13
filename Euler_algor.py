###Python-MYSQL-User_Interface###:
from find_primes_to_array import find_primes_turn_to_array
from find_primes_to_array import check_prime
from find_primes_to_array import find_Eulers_numbers
import Config_handler
import random
import math

##Euler_algor##:
data_path = '/Data/'
filename = 'Config.ini'
curfile = str(__file__)
header = 'Euler'
var = 'primes'


#Math functions:
def cacl_hcf(num1, num2):
     hcf = 1
     for i in range(1, min(num1, num2)+1):
          if num1 % i == 0 and num2 % i == 0:
               hcf = i
     return hcf


#Euler Object:
class Euler_algor_obj:
     def __init__(self, new_or_cur):
          self.primes = find_primes_turn_to_array(data_path, filename, curfile, header, var)
          self.len_primes = len(self.primes)
          self.p = None
          self.p_index = None
          self.q = None
          self.n = None
          self.thi = None
          self.e = None
          self.d = None
          
          if new_or_cur:
               self.p = self.calc_p()[0]
               self.p_index = self.calc_p()[1]
               self.q = self.calc_q()
               self.n = self.calc_n()
               self.thi = self.calc_thi()
               self.e = self.calc_e()
               self.d = self.calc_d()
          else:
               Eulers_numbers_import = find_Eulers_numbers(data_path, filename, curfile, header)
               self.p = Eulers_numbers_import['p']
               self.q = Eulers_numbers_import['q']
               self.n = Eulers_numbers_import['n']
               self.thi = Eulers_numbers_import['thi']
               self.e = Eulers_numbers_import['e']
               self.d = Eulers_numbers_import['d']
               
          self.publicKey = (self.e, self.n)
          self.privateKey = (self.d, self.p, self.q)
          self.org_nums = []
          self.cypher_nums = []
          self.config_names = ['p', 'q', 'n', 'thi', 'e', 'd']
          self.config_values = [self.p, self.q, self.n, self.thi, self.e, self.d]
               

     def set_defaults(self):
          self.p = self.defaults[0]
          self.q = self.defaults[1]
          self.n = self.defaults[2]
          self.thi = self.defaults[3]
          self.e = self.defaults[4]
          self.d = self.defaults[5]


     def calc_p(self):
          rand_pos = random.randrange(self.len_primes // 4, self.len_primes // 2)
          p = self.primes[rand_pos]
          return [p, rand_pos]

     def calc_q(self):
          q = self.primes[self.p_index -1]
          return q

     def calc_n(self):
          n = self.p * self.q
          return n

     def calc_thi(self):
          pn1 = self.p-1
          qn1 = self.q-1
          thi = pn1 * qn1
          return thi

     def calc_e(self):
          e_options_array = []
          for i in self.primes:
               if i < self.thi and cacl_hcf(self.thi, i) == 1 and cacl_hcf(self.n, i) == 1:
                    e_options_array.append(i)
          e = e_options_array[-1]
          return e

     def calc_d(self):
          d = self.e + 1
          while (d * self.e) % self.thi != 1 or not check_prime(d):
               d = d + 1
          return d

     def encrypt_num(self, m):
          #c = m^e mod n
          c = (m ** self.e) % self.n
          self.org_nums.append(m)
          self.cypher_nums.append(c)
          return c

     def decrypt_num(self, c):
          #m = c^d mod n
          m = (c ** self.d) % self.n
          return m

     def encrypt_string(self, string):
          letter_ascii_nums = [ord(i) for i in string]
          encrypted_letter_ascii_nums = [self.encrypt_num(i) for i in letter_ascii_nums]
          return encrypted_letter_ascii_nums

     def decrypt_string(self, string_array):
          decrypted_nums = [self.decrypt_num(i) for i in string_array]
          decrypted_nums_to_ascii_letters = [chr(i) for i in decrypted_nums]
          substr = ''
          for i in decrypted_nums_to_ascii_letters:
               substr+=i
          return substr

     def write_vars_to_config(self):
          config_write_obj = Config_handler.config_obj(data_path, filename, curfile)
          config_write_obj.write_to_config(header, self.config_names, self.config_values)


          
"""
#test1.1:
Euler = Euler_algor_obj()
num = 30
print(num)
cypher = Euler.encrypt_num(num)
print(cypher)
org_num = Euler.decrypt_num(cypher)
print(org_num)

#test2:
Euler = Euler_algor_obj()
string = 'HiMyNameIsSlim_Shady'
cypher = Euler.encrypt_string(string)
org_string = Euler.decrypt_string(cypher)
"""
