import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			l = int(len(line.strip())/2)
			yield set(line[0:l]), set(line[l:2*l])

def priority(element):
	e = ord(element)
	if element.islower():
		return e - ord('a') + 1
	return e - ord('A') + 27

def find_common(rucksacks):
	for rucksack in rucksacks:
		yield rucksack[0].intersection(rucksack[1])

def find_badge(rucksacks):
	i = iter(rucksacks)
	try:
		while True:
			r = next(i)
			common = r[0].union(r[1])
			for _ in range(2):
				r = next(i)
				c = r[0].union(r[1])
				common = common.intersection(c)
			yield common
	except StopIteration:
		return

def score(c):
	return sum(priority(e.pop()) for e in c)

def print_generator(g):
	print([e for e in g])

def main(filename):
	d = list(read_input(filename))
	print(d)
	print(score(find_common(d)))
	print(score(find_badge(d)))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
