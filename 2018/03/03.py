
import re
from collections import namedtuple

claim = namedtuple('claim', ['id', 'x', 'y', 'w', 'h'])

def read_input(filename):
	p = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
	with open(filename) as f:
		for l in f:
			m = p.match(l)
			yield claim(*[int(g) for g in m.groups()])

def iterate_claim(claim):
	for x in range(claim.x, claim.x + claim.w):
		for y in range(claim.y, claim.y + claim.h):
			yield (x, y)

claims = list(read_input('input'))

claimed = set()
overlap = set()

for claim in claims:
	for f in iterate_claim(claim):
		if f in claimed:
			overlap.add(f)
		else:
			claimed.add(f)

print("Number of overlaps: {}".format(len(overlap)))

for claim in claims:
	if not any(f in overlap for f in iterate_claim(claim)):
		print("No overlap in claim {}".format(claim.id))

