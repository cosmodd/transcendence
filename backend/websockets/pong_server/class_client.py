class Client:
	def __init__(self, websocket, token, username):
		self.ws = websocket
		self.token = token
		self.name = ""
		self.username = username
		self.ready = False