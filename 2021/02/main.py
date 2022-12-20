
def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			command, step = line.split(" ")
			yield command, int(step)

def main(filename):
	depth = 0
	position = 0
	aim = 0
	for command, distance in read_input(filename):
		if command == "up":
			aim -= distance
		elif command == "down":
			aim += distance
		elif command == "forward":
			position += distance
			depth += distance * aim

	print(position, depth)
	print(position * depth)


import sys
main(sys.argv[1])
