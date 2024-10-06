from typing import Iterable, List
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

class Chat(BaseModel):
    name = CharField(unique=True)

class Message(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.now)
    chat = ForeignKeyField(Chat)
    sender = ForeignKeyField(User)

class TextMessage(Message):
    text = CharField(max_length=10_000)

class Membership(BaseModel):
    user = ForeignKeyField(User)
    chat = ForeignKeyField(Chat)


def create_user(username:str, password:str):
    
    salt=str(randint(0,1_000_000))
    password=sha1(password+salt)
    user=User.create(username=username, password=password, salt=salt)
    create_chat('self-'+username, [username])
    return user

def authenticate(username:str, password:str):

    user=User.get_or_none(username=username)
    if not user: return False
    return user.password == sha1(password+user.salt)


def chats_for(username:str)->Iterable[Chat]:

    chats = Chat.select().join(Membership).where(Membership.user == User.get(username=username))
    return chats

def messages_for(chat:str)->Iterable[Message]:

    text_messages=TextMessage.filter(chat=Chat.get(name=chat))
    return text_messages

def create_chat(name:str, members:List[str])->Chat:

    chat = Chat.create(name=name)
    
    for member in members:
        Membership.create(chat=chat, user=User.get(username=member))
    
    return chat

def create_text_message(sender:str, text:str, chat:str):
    return TextMessage.create(sender=User.get(username=sender), text=text, chat=Chat.get(name=chat))

db.connect()
db.create_tables([
    User,
    Chat,
    Message,
    TextMessage,
    Membership,
])
