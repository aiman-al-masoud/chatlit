
def destroy_db(name:str):
    import os
    os.popen(f'rm {name}').read()

destroy_db('my_database.db')

from api import  *

create_user('capra', 'password')
create_user('somaro', 'password')
create_user('asino', 'password')
create_chat('capra-somaro', ['capra', 'somaro'])
create_text_message('capra', 'ciao mondo!', 'capra-somaro')
chats = chats_for('somaro')
ms=messages_for('capra-somaro')
# print(ms.__class__)
# for m in ms:
#     print(m)





