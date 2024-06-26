import asyncio

class Client:
	def __init__(self, websocket, username):
		self.ws = websocket
		self.name = ""
		self.username = username
		self.ready = False
		self.ready_lock = asyncio.Lock()
		self.game = None
	
	async def IsReady(self):
		async with self.ready_lock: return self.ready == True
	
	async def SetReadyState(self, new_state: bool):
		async with self.ready_lock: self.ready = new_state