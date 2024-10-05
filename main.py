import streamlit as st
from api import authenticate, chats_for, create_user, messages_for
from streamlit_option_menu import option_menu

if 'user' not in st.session_state:
    st.session_state['user'] = None

def main():

    if not st.session_state['user']:
        login_form()
    else:
        # st.toast(f"welcome back {st.session_state['user'].capitalize()}!")
        home()


def signup_form():

    st.title('Sign Up')
    username=st.text_input('Username')
    password=st.text_input('New Password', type='password')
    password_repeat=st.text_input('Repeat Password', type='password')

    if st.button('sign up'):

        if password != password_repeat:
            st.error("passwords don't match!")
        else:
            create_user(username, password)


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

        chat = option_menu(
            'Chats',
            chats_for(st.session_state['user'])
        )

        st.header('Add friends')
        st.text_input('Enter the username')
        st.button('Add friend')
        
        st.header('Create group')
        st.text_input('Group name')
        st.text_input('Members (space separated usernames)')
        st.button('Create group')


    show_chat(chat)

def chat_list():

    with st.container(height=200):
        for c in chats_for(st.session_state['user']):
            
            if st.button(c, use_container_width=True):
                st.session_state['chat'] = c
                st.rerun()


def users_list():

    with st.container(height=200):
        st.button('user 1', use_container_width=True)
        st.button('user 2', use_container_width=True)
        st.button('user 3', use_container_width=True)
        st.button('user 4', use_container_width=True)
        st.button('user 5', use_container_width=True)
        st.button('user 6', use_container_width=True)
        st.button('user 7', use_container_width=True)

def show_chat(chat:str):

    with st.container(height=200):
        for m in messages_for(chat):
            st.button(m, use_container_width=True)

    st.chat_input()

if __name__ == '__main__':

    main()

