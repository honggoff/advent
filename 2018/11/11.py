def power_level(x, y, serial):
	assert(x <= 300 and y <= 300)
	rack_id = x + 10
	temp = (rack_id * y + serial) * rack_id
	level = int(temp / 100) % 10 - 5
	return level

class Grid:
	def __init__(self, serial):
		self._values = [[power_level(x, y, serial) for y in range(1, 301)] for x in range(1, 301)]

	def _squares(self):
		for x in range(298):
			for y in range(298):
				yield (x, y)


	def maximum(self):
		max_level = -10
		for s in self._squares():
			level = 0
			for x in range(s[0], s[0] + 3):
				for y in range(s[1], s[1] +3):
					level += self._values[x][y]
			if level > max_level:
				max_level = level
				max_coordinate = s
		return max_coordinate

	def _all_squares(self):
		for x in range(300):
			for y in range(300):
				max_size = 300 - max(x, y)
				for s in range(1, max_size + 1):
					yield (x, y, s)


	def maximum_all_sizes(self):
		max_level = -10
		for s in self._all_squares():
			level = 0
			for x in range(s[0], s[0] + s[2]):
				for y in range(s[1], s[1] + s[2]):
					level += self._values[x][y]
			if level > max_level:
				max_level = level
				max_coordinate = s
		return max_coordinate


print(Grid(18).maximum())
print(Grid(42).maximum())
print(Grid(8979).maximum())

#print(Grid(18).maximum_all_sizes())
#print(Grid(42).maximum_all_sizes())
print(Grid(8979).maximum_all_sizes())
