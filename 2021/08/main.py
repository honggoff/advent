from pprint import pprint
from collections import namedtuple

Entry = namedtuple("Entry", ("patterns", "outputs"))

def parse_entry(l):
	tokens = l.split()
	entry = Entry(set(), [])
	for i in range(10):
		entry.patterns.add(frozenset(tokens[i]))
	for i in range(11, 15):
		entry.outputs.append(frozenset(tokens[i]))
	return entry

def read_input(filename):
	entries = []
	with open(filename, 'r') as f:
		for l in f:
			entries.append(parse_entry(l))

	return entries

def find_of_length(collection, length):
	return (x for x in collection if len(x) == length)

def get_decoding(p):
	decoding = [None] * 10
	decoding[1] = next(find_of_length(p, 2))
	p.remove(decoding[1])
	decoding[4] = next(find_of_length(p, 4))
	p.remove(decoding[4])
	decoding[7] = next(find_of_length(p, 3))
	p.remove(decoding[7])
	decoding[8] = next(find_of_length(p, 7))
	p.remove(decoding[8])
	decoding[6] = next(x for x in find_of_length(p, 6) if len(x.intersection(decoding[1])) == 1)
	p.remove(decoding[6])
	decoding[0] = next(x for x in find_of_length(p, 6) if len(x.intersection(decoding[4])) == 3)
	p.remove(decoding[0])
	decoding[9] = next(x for x in find_of_length(p, 6))
	p.remove(decoding[9])
	decoding[3] = next(x for x in p if len(x.intersection(decoding[7])) == 3)
	p.remove(decoding[3])
	decoding[5] = next(x for x in p if len(x.intersection(decoding[9])) == 5)
	p.remove(decoding[5])
	decoding[2] = p.pop()
	return {code: i for i, code in enumerate(decoding)}

def count_simple(entries):
	count = 0
	for entry in entries:
		count += sum(1 for x in entry.outputs if len(x) in (2, 3, 4, 7))
	return count

def value(digits, decoding):
	ret = 0
	for index, digit in enumerate(reversed(digits)):
		ret += 10 ** index * decoding[digit]
	return ret

def decode(entries):
	for entry in entries:
		decoding = get_decoding(entry.patterns)
		v = value(entry.outputs, decoding)
		yield v

def main(filename):
	entries = read_input(filename)
	pprint(entries)
	print(count_simple(entries))
	print(sum(decode(entries)))

import sys
main(sys.argv[1])
