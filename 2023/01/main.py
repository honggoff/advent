import string

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.strip()


def get_value(line):
	numbers = [c for c in line if c in string.digits]
	return int(numbers[0] + numbers[-1])


def get_value2(line):
	names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
	numbers = []
	# print(line)
	for i in range(len(line)):
		c = line[i]
		if c in string.digits:
			# print(c)
			numbers.append(int(c))
		else:
			for l in (3, 4, 5):
				word = line[i:i+l]
				if word in names:
					# print(word)
					numbers.append(names.index(word) + 1)
					continue
	return numbers[0] * 10 + numbers[-1]


def main(filename):
	input = read_input(filename)
	# calibration_values = [get_value(i) for i in input]
	# print(calibration_values)
	# print(sum(calibration_values))

	calibration_values = [get_value2(i) for i in input]
	print(calibration_values)
	print(sum(calibration_values))


import sys
main(sys.argv[1])
