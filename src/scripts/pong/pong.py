from objects import Ball, Paddle

__all__ = ["PLAYER1", "PLAYER2", "Pong"]

PLAYER1, PLAYER2 = "p1", "p2"

class Pong:
	def __init__(self):
		self._players = {}
		self._players[PLAYER1] = Paddle([0., 0.])
		self._players[PLAYER2] = Paddle([0., 0.])
		#self.ball = Ball()
		self.score = [0, 0]

	def AssertNewPlayerPosition(self, current_player, new_position):
		# assert some game rules

		self._players[current_player].position = new_position	
		return self._players[current_player].position