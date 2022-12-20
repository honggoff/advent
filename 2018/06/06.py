from collections import Counter
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


def read_input(filename):
	with open(filename, 'r') as f:
		for l in f:
			yield Point._make(int(i) for i in l.split(','))


def neighbours(p):
	yield Point(p.x + 1, p.y)
	yield Point(p.x - 1, p.y)
	yield Point(p.x, p.y + 1)
	yield Point(p.x, p.y - 1)


def visualize(covered, areas, p_min, p_max):
	print('-- {} points --'.format(len(covered)))
	canvas = [[' '] * p_max.x for l in range(p_max.y)]
	for p in covered:
		canvas[p.y-1][p.x-1] = '.'
	c = ord('0')
	for a in areas:
		for p in a:
			canvas[p.y-1][p.x-1] = chr(c)
		c += 1
	for l in canvas:
		print(''.join(l))


def filter_infinite(areas, p_min, p_max):
	filtered = []
	for a in areas:
		if not any(p.x == p_min.x or p.x == p_max.x or p.y == p_min.y or p.y == p_max.y for p in a):
			filtered.append(a)
		else:
			filtered.append(set())
	return filtered


def get_boundaries(points):
	p_min = Point(min(p.x for p in points), min(p.y for p in points))
	p_max = Point(max(p.x for p in points), max(p.y for p in points))
	return p_min, p_max

def areas(points):
	p_min, p_max = get_boundaries(points)

	def inside(p):
		return p_min.x <= p.x <= p_max.x and p_min.y <= p.y <= p_max.y

	area = (p_max.x - p_min.x + 1) * (p_max.y - p_min.y + 1)
	areas = [set((p,)) for p in points]
	covered = set(points)
	growing = True
	while len(covered) < area:
		#visualize(covered, areas, p_min, p_max)
		candidates = [set() for p in points]
		current = Counter()
		for a, c in zip(areas, candidates):
			for p in a:
				for n in neighbours(p):
					if n not in covered and inside(n):
						c.add(n)
			current.update(c)
		for a, c in zip(areas, candidates):
			for p in c:
				if current[p] == 1:
					a.add(p)
				#else:
					#print('sorted out {} with count {}'.format(p, current[p]))
				covered.add(p)
	visualize(covered, areas, p_min, p_max)
	filtered_areas = filter_infinite(areas, p_min, p_max)
	visualize(set(), filtered_areas, p_min, p_max)
	return filtered_areas


def largest(areas):
	return max(len(a) for a in areas)


def count_closest(points, threshold):
	p_min, p_max = get_boundaries(points)
	count = 0
	for x in range(p_min.x, p_max.x + 1):
		for y in range(p_min.y, p_max.y + 1):
			c = sum(abs(p.x - x) + abs(p.y - y) for p in points)
			if c < threshold:
				count += 1
	return count

test_points = list(read_input('test_input'))
points = list(read_input('input'))

print("{} closest in test input".format(count_closest(test_points, 32)))

print("{} closest in real input".format(count_closest(points, 10000)))
exit()
print("largest in test input: {}".format(largest(areas(test_points))))

print("largest in real input: {}".format(largest(areas(points))))
