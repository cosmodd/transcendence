import json

from constants import *

class MessageBuilder:
	def __init__(self, game):
		self.attached_game = game

	def PlayerPosition(self, player, inverted: bool):
		position = self.attached_game.GetPlayerPosition(player)
		if (inverted):
			position[0] *= -1.0
		return json.dumps({
                    METHOD: FROM_SERVER,
                    OBJECT: OBJECT_PADDLE,
                    DATA_POSITION: [position[0], position[1]]
                })
