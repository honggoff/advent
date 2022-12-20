import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		current = []
		for line in f:
			if line.strip():
				current.append(int(line))
			else:
				yield current
				current = []

		if current:
			yield current

def sum_per_elf(numbers):
	for elf_items in numbers:
		yield sum(elf_items)

def main(filename):
	sums = sorted(sum_per_elf( read_input(filename)))

	print(sums[-3:])
	print(max(sums))
	print(sum(sums[-3:]))


import sys
main(sys.argv[1])
