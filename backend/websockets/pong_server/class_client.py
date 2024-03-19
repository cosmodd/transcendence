class Client:
	def __init__(self, websocket, token):
		self.ws = websocket
		self.token = token
		self.name = ""
		#self.username