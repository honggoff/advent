'''
Documentation, License etc.

@package adv2018_01
'''

def read_all(filename):
	with open(filename, 'r') as f:
		return [int(i) for i in f]

def repeat_sequence(sequence):
	while True:
		for i in sequence:
			yield i

input = read_all('input')
print(sum(input))

f = 0
reached = set()
sequence = repeat_sequence(input)
while f not in reached:
	reached.add(f)
	f += next(sequence)

print(f)
