from flask import Flask
import commands


class User:
	def __init__(self, u, p):
		self.u=u
		self.p=p

class server(Flask):
	def __init__(self, *args, **kwargs):
		super(server, self).__init__(*args, **kwargs)
		
		#self.users = [User('gemdude46'),User('sbneelu')]
		
		#self.messages = [Message('Server started: '+commands.getstatusoutput('date')[1],None)]

app = server(__name__)

@app.route('/')
def index():
	return '&lt; INSERT SITE HERE &gt;'
