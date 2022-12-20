import pprint
import functools

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self, direction):
		if direction == RIGHT:
			self.x += 1
		elif direction == UP:
			self.y -= 1
		elif direction == LEFT:
			self.x -= 1
		elif direction == DOWN:
			self.y += 1

	def __str__(self):
		return "Point({}, {})".format(self.x, self.y)


class Map:
	def __init__(self, map):
		self._map = map
		self.width = len(self._map[0])
		self.height = len(self._map)

	def __getitem__(self, point):
		return self._map[point.y][point.x]

	def __setitem__(self, point, value):
		self._map[point.y][point.x] = value

	def __contains__(self, point):
		return point.x >= 0 and point.y >= 0 and point.y < len(self._map) and point.x < len(self._map[point.y])

	def __str__(self):
		return pprint.pformat(self._map)

	def start_points(self, direction):
		if direction == RIGHT:
			return [Point(0, y) for y in range(self.height)]
		elif direction == UP:
			return [Point(x, self.height - 1) for x in range(self.width)]
		elif direction == LEFT:
			return [Point(self.width - 1, y) for y in range(self.height)]
		elif direction == DOWN:
			return [Point(x, 0) for x in range(self.width)]

	def clone_empty(self):
		return Map([[0 for x in range(self.width)] for y in range(self.height)])

	def sum(self):
		return sum(sum(x) for x in self._map)

	def max(self):
		return max(max(x) for x in self._map)

def read_input(filename):
	with open(filename, 'r') as f:
		return Map([list(int(x) for x in line.strip()) for line in f])


def find_visible(map):
	visible = map.clone_empty()
	for direction in DIRECTIONS:
		for point in map.start_points(direction):
			highest = -1
			while point in map:
				if map[point] > highest:
					visible[point] = 1
					highest = map[point]
				point.move(direction)
	return visible


def viewing_distance(map, point, direction):
	distance = 0
	height = map[point]
	while point in map:
		point.move(direction)
		if point not in map:
			break
		distance += 1
		if map[point] >= height:
			break
	return distance


def find_scenic_score(map):
	score = map.clone_empty()
	for x in range(1, map.width - 1):
		for y in range(1, map.height - 1):
			d = (viewing_distance(map, Point(x, y), direction) for direction in DIRECTIONS)
			score[Point(x, y)] = functools.reduce(lambda a, b: a*b, d)
	return score

def main(filename):
	map = read_input(filename)
	#print(map)
	visible = find_visible(map)
	score = find_scenic_score(map)
	print(visible.sum())
	print(score.max())


if __name__ == "__main__":
	import sys
	main(sys.argv[1])
