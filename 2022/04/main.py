
def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			pair = []
			for s in line.split(','):
				r = [int(b) for b in s.split('-')]
				s = set(range(r[0], r[1] + 1))
				pair.append(s)
			yield pair


def print_generator(g):
	print([e for e in g])

def count_fully_contained(sets):
	return sum(map(lambda x: x[0].issubset(x[1]) or x[0].issuperset(x[1]), sets))

def count_overlapped(sets):
	return sum(map(lambda x: bool(x[0].intersection(x[1])), sets))

def main(filename):
	d = list(read_input(filename))
	print(count_fully_contained(d))
	print(count_overlapped(d))
	print_generator(d)

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
