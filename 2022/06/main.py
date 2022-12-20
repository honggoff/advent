import copy

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			return line

def find_not_repeating(buffer, count):
	"""
	Some tests:
	>>> find_not_repeating('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4)
	7
	>>> find_not_repeating('bvwbjplbgvbhsrlpgdmjqwftvncz', 4)
	5
	>>> find_not_repeating('nppdvjthqldpwncqszvftbrmjlhg', 4)
	6
	>>> find_not_repeating('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4)
	10
	>>> find_not_repeating('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4)
	11
	>>> find_not_repeating('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14)
	19
	>>> find_not_repeating('bvwbjplbgvbhsrlpgdmjqwftvncz', 14)
	23
	>>> find_not_repeating('nppdvjthqldpwncqszvftbrmjlhg', 14)
	23
	>>> find_not_repeating('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)
	29
	>>> find_not_repeating('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14)
	26
	"""
	window = [buffer[0]] * count
	position = 0
	for b in buffer:
		position += 1
		window.pop(0)
		window.append(b)
		if len(set(window)) == count:
			return position

def main(filename):
	buffer = read_input(filename)
	print(find_not_repeating(buffer, 4))
	print(find_not_repeating(buffer, 14))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
