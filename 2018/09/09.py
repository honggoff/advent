from blist import blist

inputs = [
	(9, 25),
	(10, 1618),
	(13, 7999),
	(17, 1104),
	(21, 6111),
	(30, 5807),
	(432, 71019),
	(432, 71019 * 100),
]


class MarbleCircle:
	def __init__(self):
		self.position = 0
		self.marbles = blist([0])

	def move(self, offset):
		self.position = (self.position + offset) % len(self.marbles)

	def remove(self):
		ret = self.marbles.pop(self.position)
		self.position = self.position % len(self.marbles)
		return ret

	def insert(self, marble):
		self.marbles.insert(self.position % len(self.marbles), marble)

	def __str__(self):
		p = self.position % len(self.marbles)
		return " ".join(("({})" if i == p else " {} ").format(m) for i, m in enumerate(self.marbles))


def turns(number_players):
	while True:
		for p in range(number_players):
			yield p


def play(number_players, number_turns):
	scores = [0] * number_players
	circle = MarbleCircle()
	for marble, player in zip(range(1, number_turns + 1), turns(number_players)):
		if marble % 23:
			# normal turn
			circle.move(2)
			circle.insert(marble)
		else:
			# special turn
			scores[player] += marble
			circle.move(-7)
			scores[player] += circle.remove()
		#print("[{}] {}".format(player, circle))
	return max(scores)


for number_players, number_turns in inputs:
	print("{} players; last marble is worth {} points: high score is {}".format(number_players, number_turns, play(number_players, number_turns)))
