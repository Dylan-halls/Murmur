from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty 
import socket

Builder.load_file('Secure-Chat.kv') 

class Chat_Client(object):

	def __init__(self):
		global s, host
		host = '192.168.1.115'
		port = 8090
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))

	def _login(self, user):
		#TODO: Add password support
		s.send(user.encode('utf-8'))
		if len(s.recv(1024).decode('utf-8')) > 0:
			rply = s.recv(1024).decode('utf-8')
			if rply == "Ready For Message":
				return True
			else:
				return False


class LoginScreen(FloatLayout):
    def __init__(self, **kwargs):
    	global chat
    	chat = Chat_Client()
    	status=ObjectProperty(None) 
        super(LoginScreen, self).__init__(**kwargs)

    def _login_handler(self, username, password):
    	if len(username) and len(password) > 1:
    		logged_in = chat._login(username)
    		if logged_in == True:
    			print("Logged in")
    		elif logged_in == False:
    			print("Failed")


class SecureChat(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    SecureChat().run()