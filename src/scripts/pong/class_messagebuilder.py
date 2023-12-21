import json

from constants import *

class MessageBuilder:
	def __init__(self, game):
		self.attached_game = game

	def PlayerPosition(self, player):
		position = self.attached_game.GetPlayerPosition(player)
		return json.dumps({
                    METHOD: FROM_SERVER,
                    OBJECT: OBJECT_PADDLE,
					DATA_PLAYER: player,
                    DATA_POSITION: [position[0], position[1]]
                })
