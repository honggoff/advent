from collections import Counter
from operator import add

def add_criteria(c1, c2):
	return [a + b for a,b in zip(c1, c2)]

def criteria(string):
	c = Counter(string)
	return (2 in c.values(), 3 in c.values())

def checksum(filename):
	s = (0, 0)
	with open(filename) as f:
		for l in f:
			s = add_criteria(s, criteria(l))
	return s[0] * s[1]

print(checksum('test_input'))
print(checksum('input'))


def are_similar(a, b):
	d = sum( i != j for i, j in zip(a, b))
	return d == 1

def find_similar(filename):
	with open(filename) as f:
		ids = [l.strip() for l in f]
	for a in ids:
		for b in ids:
			if (a != b) and are_similar(a, b):
				return a, b

def identical(a, b):
	return "".join(i for i, j in zip(a, b) if i == j)


similar = find_similar('test_input2')
print(similar, identical(*similar))

similar = find_similar('input')
print(similar)
print(identical(*similar))
