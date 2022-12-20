import re


def parse_range(text):
	r = [int(e) for e in text.split('..')]
	if len(r) == 1:
		r = r * 2
	return range(r[0], r[1] + 1)


def read_input(filename):
	entries = []
	with open(filename, 'r') as f:
		for l in f:
			m = re.match('(.)=(.+), .=(.+)', l)
			if m.group(1) == 'x':
				x = parse_range(m.group(2))
				y = parse_range(m.group(3))
			else:
				x = parse_range(m.group(3))
				y = parse_range(m.group(2))
			entries.append((x, y))
