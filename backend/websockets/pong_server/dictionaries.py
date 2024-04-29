import asyncio

class UsernameToRoom:
	def __init__(self):
		self.dict = {}
		self.lock = asyncio.Lock()
	
	async def AddToDict(self, username, game):
		async with self.lock:
			self.dict[username] = game
	
	async def GetFromDict(self, username):
		game = None
		async with self.lock:
			game = self.dict[username]
		return game
	 
	async def HasInDict(self, username):
		async with self.lock:
			return username in self.dict
	
	async def DeleteInDict(self, username):
		async with self.lock:
			del self.dict[username]