class Client:
	def __init__(self, websocket, uuid, name):
		self.ws = websocket
		self.uuid = uuid
		self.name = name