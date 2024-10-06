import streamlit as st
from api import Message, TextMessage, authenticate, chats_for, create_chat, create_text_message, create_user, messages_for
from streamlit_option_menu import option_menu

if 'user' not in st.session_state:
    st.session_state['user'] = None

def main():

    if not st.session_state['user']:

        login, signup = st.tabs(['Login', 'Sign Up'])

        with login:
            login_form()
        with signup:
            signup_form()

    else:
        # st.toast(f"welcome back {st.session_state['user'].capitalize()}!")
        home()


def signup_form():

    st.title('Sign Up')
    username=st.text_input('Username', key='usernamesignup')
    password=st.text_input('New Password', type='password', key='password1')
    password_repeat=st.text_input('Repeat Password', type='password', key='password2')

    if st.button('sign up'):

        if password != password_repeat:
            st.error("passwords don't match!")
        else:
            create_user(username, password)
            st.success('Success! Now please login with your new credentials.')


def login_form():

    st.title('Login')
    username=st.text_input('Username')
    password=st.text_input('Password', type='password')
    
    if st.button('login'):

        if authenticate(username, password):
            st.session_state['user'] = username
            st.rerun()
        else:
            st.error('wrong username or password')


def home():

    with st.sidebar:

        st.title(f"Welcome back {st.session_state['user']}!")

        chat = option_menu(
            'Your Chats',
            [str(c.name) for c in chats_for(st.session_state['user'])],
            menu_icon='chat',
        )

        st.divider()

        st.header('Add friends')
        new_friend = st.text_input('Enter the username')
        if st.button('Add friend'):
            create_chat(st.session_state['user']+new_friend, [st.session_state['user'], new_friend])
            st.rerun()

        st.divider()

        st.header('Create group')
        group_name=st.text_input('Group name')
        members=st.text_input('Members (space separated usernames)')
        if st.button('Create group'):
            create_chat(group_name, members.split())

        st.divider()

        st.header('Manage your data')
        st.button('download all')
        st.button('delete all', type='primary')


    show_chat(chat)

def show_chat(chat:str):

    st.header(chat)

    with st.container(height=200):
        for m in messages_for(chat):
            show_message(m)

    if message := st.chat_input():
        create_text_message(st.session_state['user'], message, chat)
        st.rerun()

def show_message(m:Message):
    
    if isinstance(m, TextMessage):
        st.button(str(m.text)+'  '+ ' ('+ str(m.sender.username)+') ' +str(m.created_at), use_container_width=True)

if __name__ == '__main__':

    main()

