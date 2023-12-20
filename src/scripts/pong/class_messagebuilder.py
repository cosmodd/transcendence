import json

from constants import *

class MessageBuilder:
	def __init__(self, game):
		self.attached_game = game

	def PlayerPosition(self, current_player):
		position = self.attached_game.GetPlayerPosition(current_player)
		return json.dumps({
                    METHOD: FROM_SERVER,
                    OBJECT: OBJECT_PADDLE,
                    DATA_POSITION: [position[0], position[1]]
                })
