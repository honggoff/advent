import functools
import collections

RIGHT = 'R'
UP = 'U'
LEFT = 'L'
DOWN = 'D'
DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

class Point:
	def __init__(self, x=0, y=0):
		self.x = int(x)
		self.y = int(y)

	def move(self, direction):
		if direction == RIGHT:
			return Point(self.x + 1, self.y)
		elif direction == UP:
			return Point(self.x, self.y - 1)
		elif direction == LEFT:
			return Point(self.x - 1, self.y)
		elif direction == DOWN:
			return Point(self.x, self.y + 1)

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y)

	def __sub__(self, point):
		return Point(self.x - point.x, self.y - point.y)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "Point({}, {})".format(self.x, self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.x, self.y))


class Map:
	def __init__(self, map):
		self._map = map
		self.width = len(self._map[0])
		self.height = len(self._map)

	@classmethod
	def from_points(cls, points):
		xmin = min(p.x for p in points)
		ymin = min(p.y for p in points)
		xmax = max(p.x for p in points)
		ymax = max(p.y for p in points)
		width = xmax - xmin + 1
		height = ymax - ymin + 1
		offset = Point(xmin, ymin)
		result = cls.empty(width, height, '.')
		for p in points:
			result[p - offset] = '#'
		return result

	@classmethod
	def empty(cls, width, height, value = 0):
		return cls([[value for x in range(width)] for y in range(height)])

	def __getitem__(self, point):
		return self._map[point.y][point.x]

	def __setitem__(self, point, value):
		self._map[point.y][point.x] = value

	def __contains__(self, point):
		return point.x >= 0 and point.y >= 0 and point.y < len(self._map) and point.x < len(self._map[point.y])

	def __str__(self):
		return '\n'.join((''.join((str(e) for e in line)) for line in self._map))

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
		return Map.empty(self.width, self.height)

	def sum(self):
		return sum(sum(x) for x in self._map)

	def max(self):
		return max(max(x) for x in self._map)

Move = collections.namedtuple('Move', ['direction', 'distance'])


def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			tokens = line.split(" ")
			yield Move(tokens[0], int(tokens[1]))

def follow(head, tail):
	diff = head - tail
	direction = Point()
	if abs(diff.x) == 2:
		direction = Point(diff.x/2, diff.y)
	if abs(diff.y) == 2:
		direction = Point(diff.x, diff.y/2)
	return tail + direction

def follow_head(moves, knots):
	visited = set()
	head = Point()
	tails = [Point() for x in range(knots - 1)]
	visited.add(head)
	for move in moves:
		for i in range(move.distance):
			head = head.move(move.direction)
			last = head
			for i in range(len(tails)):
				tails[i] = follow(last, tails[i])
				last = tails[i]
			visited.add(last)
	return visited


def main(filename):
	moves = read_input(filename)
	visited = follow_head(moves, 2)
	print(visited)
	print(Map.from_points(visited))
	print(len(visited))

	moves = read_input(filename)
	visited = follow_head(moves, 10)
	print(Map.from_points(visited))
	print(len(visited))


if __name__ == "__main__":
	import sys
	main(sys.argv[1])
