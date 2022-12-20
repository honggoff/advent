from pprint import pprint
import copy

max_elevation = ord('z') - ord('a')

def read_input(filename):
	map = []
	with open(filename, 'r') as f:
		for line in f:
			map.append([ord(c) - ord('a') for c in line.strip()])
	return map


def find_start_end(map):
	for i in range(len(map)):
		for j in range(len(map[i])):
			if map[i][j] == ord('S') - ord('a'):
				start = (i, j)
				map[i][j] = 0
			elif map[i][j] == ord('E') - ord('a'):
				end = (i, j)
				map[i][j] = max_elevation
	return start, end


def visited_from_map(map, point):
	visited = [[False for j in map[0]] for i in map]
	visited[point[0]][point[1]] = True
	return visited


def neighbors(map, i, j):
	if i > 0:
		yield (i - 1, j)
	if i < len(map) - 1:
		yield (i + 1, j)

	if j > 0:
		yield(i, j - 1)
	if j < len(map[0]) - 1:
		yield(i, j + 1)


def step(map, visited):
	next_visited = copy.deepcopy(visited)
	for i in range(len(map)):
		for j in range(len(map[i])):
			if visited[i][j]:
				for x, y in neighbors(map, i, j):
					if not visited[x][y]:
						if map[x][y] <= map[i][j] + 1:
							next_visited[x][y] = True
	return next_visited


def step_down(map, visited):
	next_visited = copy.deepcopy(visited)
	for i in range(len(map)):
		for j in range(len(map[i])):
			if visited[i][j]:
				for x, y in neighbors(map, i, j):
					if not visited[x][y]:
						if map[x][y] >= map[i][j] - 1:
							next_visited[x][y] = True
	return next_visited


def find_end(map, start, end):
	visited = visited_from_map(map, start)
	#pprint(visited)
	steps = 0
	while not visited[end[0]][end[1]]:
		visited = step(map, visited)
		#pprint(visited)
		steps += 1
	return steps


def lowest_point_reached(map, visited):
	for i in range(len(map)):
		for j in range(len(map[i])):
			if map[i][j] == 0 and visited[i][j]:
				return True
	return False


def find_start(map, end):
	visited = visited_from_map(map, end)
	#pprint(visited)
	steps = 0
	while not lowest_point_reached(map, visited):
		visited = step_down(map, visited)
		#pprint(visited)
		steps += 1
	return steps


def main(filename):
	map = read_input(filename)
	start, end = find_start_end(map)
	#pprint(map)
	pprint(start)
	pprint(end)
	count = find_end(map, start, end)
	print(count)
	print(find_start(map, end))


if __name__ == "__main__":
	import sys
	main(sys.argv[1])
