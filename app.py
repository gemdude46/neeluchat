from flask import Flask, request
import commands
import hashlib
import os

def hash(data,algo="sha512"):
	h = eval("hashlib."+algo)()
	h.update(data)
	return h.digest()

def htmlify(t):
	s=''
	for l in t:
		if   l == '&': s+='&amp;'
		elif l == '<': s+='&lt;'
		elif l == '>': s+='&gt;'
		elif l == ' ': s+='&nbsp;'
		elif l =='\n': s+='<br />'
		else:          s+=l
	return s

def hexify(t):
	s=''
	for l in t: s += chr(65+ord(l)/16)+chr(65+ord(l)%16)
	return s

class User:
	def __init__(self, u, p, c=None):
		self.u=u
		self.p=p
		self.c=(c,'gray')[c is None]

	def auth(self,pw):
		return hash(pw)==self.p

	def __str__(self):
		return self.u

class server(Flask):
	def __init__(self, *args, **kwargs):
		super(server, self).__init__(*args, **kwargs)
		
		self.users = [
			User('gemdude46','H\x90\xa7\x02\xa28\x91(\xa4\xed\xcd)\xa0\xfeW\xe1\xcc\xf9\xda\xd6\xe6\x9d\x90\xe6\xbe\xb8x\xcb{\xfc4\xa6\x81qTZ\xf9\x7f\x84\xf9<D$!9\xd5\xaa\xa1X\xa1\x13\xfez\x9d\x18~\xaes\xf1\xbd\x176\xda\xfe','#400'),
			User('sbneelu','\xffeH\xf4\xf0\xfa\xe7\xe4K=o{\xdd\xde3\x98\\B\xf6\xb774Y\r\xdb\x1d#\xb3\x90}\x94\xd3\xb9v`\xd9#\xfb\x06\x1cI\xe3\xe1\x99\xfbu\x92\t\xbe\xf3\xd9\xb8#\x99r#\x94\xdc3\xe2\xe1l\xb3\xfd','green')
		]
		
		#self.messages = [Message('Server started: '+commands.getstatusoutput('date')[1],'[SERVER]')]

		self.sids = {}

app = server(__name__)

def getUser(n):
	for u in app.users:
		if u.u==n: return u

@app.route('/')
def index():
	return 'HELLO, PERSON! Y U HERE?'


@app.route('/chat/')
def chat():
	return chatpage

@app.route('/chat/sid')
def sid():
	u=getUser(request.args['u'])
	if u.auth(request.args['p']):
		r=hexify(os.urandom(256))
		app.sids[r]=u
		return r
	raise ValueError
		
@app.route('/chat/msghtml')
def msghtml():
	u=app.sids[request.args['s']]
	while True:
		try:
			f = open('msgs.txt','r')
			t = f.read()
			f.close()
			return t
		except IOError: pass

@app.route('/chat/sendmsg')
def sendmsg():
	u = app.sids[request.args['s']]
	putmsg('<b style="color:'+u.c+';" >'+str(u)+'</b>: '+htmlify(request.args['m']))

def putmsg(msg):
	opened = False
	while not opened:
		opened = True
		try: f = open('msgs.txt','a')
		except IOError: opened = False
	f.write(msg+'<br />')
	f.close()

f = open('chatlogin.html','r')
chatpage = f.read()
f.close()

f = open('chat.js','r')
chatpage = chatpage.replace('{JS}',f.read())
f.close()

f = open('chat.html','r')
chatpage = chatpage.replace('{HTML}',f.read().replace('\\','\\\\').replace('\'','\\\'').replace('\n',' '))
f.close()
