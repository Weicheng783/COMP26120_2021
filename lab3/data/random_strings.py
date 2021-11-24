import string
import random

length=49
number=10000

for i in range(number):
  print(''.join(random.choices(string.ascii_lowercase, k=length)))
