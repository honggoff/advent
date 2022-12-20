import functools
import collections

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
		return self._map[point[1]][point[0]]

	def __setitem__(self, point, value):
		self._map[point[1]][point[0]] = value

	def __contains__(self, point):
		return point.x >= 0 and point.y >= 0 and point.y < len(self._map) and point.x < len(self._map[point.y])

	def __str__(self):
		return '\n'.join((''.join((str(e) for e in line)) for line in self._map))


def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.strip().split(" ")

def execute(instructions):
	x = 1
	for instruction in instructions:
		if instruction[0] == 'noop':
			yield x
		elif instruction[0] == 'addx':
			number = int(instruction[1])
			yield x
			yield x
			x += number


def signal_strength(cycle, x):
	return cycle * x

def selected_strength(values):
	i = 0
	for k in range(20):
		v = next(values)
		i += 1
	print(i, v)
	yield signal_strength(i, v)
	while True:
		try:
			for k in range(40):
				v = next(values)
				i += 1
			print(i, v)
			yield signal_strength(i, v)
		except StopIteration:
			break


def draw_screen(values):
	screen = Map.empty(40, 6, '.')
	for y in range(screen.height):
		for x in range(screen.width):
			v = next(values)
			if x-1 <= v <= x+1:
				screen[x, y] = '#'
			print(x+1, v, screen[x, y])
	return screen


def main(filename):
	instructions = read_input(filename)
	#print(list(selected_strength(execute(instructions))))
	print(sum(selected_strength(execute(instructions))))

	instructions = read_input(filename)
	print(draw_screen(execute(instructions)))


if __name__ == "__main__":
	import sys
	main(sys.argv[1])
