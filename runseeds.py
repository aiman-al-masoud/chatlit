import os
os.popen('rm my_database.db').read()

from api import  create_user

create_user('capra', 'password')
create_user('somaro', 'password')

