import re

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Light:
        def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

	def at_time(t):
		return tuple(p + t * v for p,v in zip(self.position, self.velocity))

	def __str__(self):
		return "position={} velocity={}".format(self.position, self.velocity)


def read_input(filename):
	with open(filename, 'r') as f:
		for l in f:
			m = re.match('position=<(.+),(.+)> velocity=<(.+),(.+)>', l)
			yield Point((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4))))


print([str(p) for p in read_input('test_input')])
