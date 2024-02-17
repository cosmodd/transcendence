class Client:
	def __init__(self, websocket, uuid):
		self.ws = websocket
		self.uuid = uuid