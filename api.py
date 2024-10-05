from peewee import *
import datetime
from cryptohash import sha1
from random import randint

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    salt = CharField(max_length=50)

# class Tweet(BaseModel):
#     user = ForeignKeyField(User, backref='tweets')
#     message = TextField()
#     created_date = DateTimeField(default=datetime.datetime.now)
#     is_published = BooleanField(default=True)

db.connect()
db.create_tables([User])


def create_user(username:str, password:str):
    
    salt=str(randint(0,1_000_000))
    password=sha1(password+salt)
    user=User.create(username=username, password=password, salt=salt)
    return user

def authenticate(username:str, password:str):

    user=User.get_or_none(username=username)
    if not user: return False
    return user.password == sha1(password+user.salt)


def chats_for(username:str):

    return ['chat 1', 'chat 2', 'chat 3', 'chat 4', 'chat 5', 'chat 6']


def messages_for(chat:str):
    return ['ciao mondo!'+chat, 'ri-ciao!'+chat, '... a tutti!!!'+chat]
