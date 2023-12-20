import json

class MessageBuilder:
	def __init__(self, game):
		self.attached_game = game

	def PlayerPosition(self, current_player):
		position = self.attached_game.GetPlayerPosition(current_player)
		return json.dumps({
                    "type": "get",
                    "object": "paddle",
                    "position": [position[0], position[1]]
                })
