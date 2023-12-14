from pprint import pprint
import string
from collections import defaultdict

def read_input(filename):
	lines = []
	with open(filename, 'r') as f:
		for line in f:
			lines.append('.' + line.strip() + '.')
	l = len(lines[0])
	return ['.' * l] + lines + ['.' * l]


def numbers(schematic):
	for i in range(len(schematic)):
		line = schematic[i]
		j = 0
		while j < len(line):
			if line[j] in string.digits:
				start = j
				while line[j] in string.digits:
					j = j+1
				end = j-1
				yield (i, start, end)
			j = j+1


def neighbors(number):
	line, start, end = number
	yield (line, start-1)
	yield (line, end+1)
	for i in range(start-1, end+2):
		yield (line-1, i)
		yield (line+1, i)


def is_symbol(number, schematic):
	l, i = number
	c = schematic[l][i]
	return c not in string.digits and c != '.'


def is_gear(number, schematic):
	l, i = number
	c = schematic[l][i]
	return c == '*'


def is_part_number(number, schematic):
	return any(is_symbol(n, schematic) for n in neighbors(number))


def value(number, schematic):
	line, start, end = number
	return int(schematic[line][start:end+1])


def gear_ratios(schematic):
	gears = defaultdict(list)
	for number in numbers(schematic):
		for n in neighbors(number):
			if is_gear(n, schematic):
				gears[n].append(value(number, schematic))
	for gear, values in gears.items():
		if len(values) == 2:
			yield values[0] * values[1]


def main(filename):
	schematic = read_input(filename)
	pprint(schematic)
	print(sum(value(n, schematic) for n in numbers(schematic) if is_part_number(n, schematic)))
	print(sum(r for r in gear_ratios(schematic)))


import sys
main(sys.argv[1])
