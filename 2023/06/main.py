from pprint import pprint


def read_input(filename):
	with open(filename, 'r') as f:
		line = next(f)
		times = [int(s) for s in line.split(':')[1].split()]
		line = next(f)
		distances = [int(s) for s in line.split(':')[1].split()]

		return [d for d in zip(times, distances)]


def read_input2(filename):
	with open(filename, 'r') as f:
		line = next(f)
		time = int(''.join(line.split(':')[1].split()))
		line = next(f)
		distance = int(''.join(line.split(':')[1].split()))

		return (time, distance)


def calculate_distance(time, acceleration):
	return (time - acceleration) * acceleration


def number_wins(time, record):
	wins = 0
	for a in range(time+1):
		if calculate_distance(time, a) > record:
			wins += 1
	return wins


def product(numbers):
	p = 1
	for n in numbers:
		p *= n
	return p


def main(filename):
	data = read_input(filename)
	print(product(number_wins(*d) for d in data))

	data = read_input2(filename)
	print(number_wins(*data))


import sys
main(sys.argv[1])
