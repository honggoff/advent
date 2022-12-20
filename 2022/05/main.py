import copy

def read_input(filename):
	with open(filename, 'r') as f:
		stacks = []
		for line in f:
			if line[1] == '1':
				break
			for i in range(int(len(line)/4)):
				e = line[1 + i * 4]
				if len(stacks) <= i:
					stacks.append([])
				if not e.isspace():
					stacks[i].append(e)
		for s in stacks:
			s.reverse()

		next(f)
		moves = []
		for line in f:
			tokens = line.split(' ')
			moves.append((int(tokens[1]), int(tokens[3]) - 1, int(tokens[5]) - 1))
		return stacks, moves

def process(stacks, moves):
	for n, f, t in moves:
		for i in range(n):
			e = stacks[f].pop()
			stacks[t].append(e)
	return stacks

def process_9001(stacks, moves):
	for n, f, t in moves:
		e = stacks[f][-n:]
		stacks[f] = stacks[f][:-n]
		stacks[t].extend(e)
	return stacks


def get_stack_top(stacks):
	code = ''
	for s in stacks:
		code += s[-1]
	return code

def main(filename):
	stacks, moves = read_input(filename)
	stack1 = process(copy.deepcopy(stacks), moves)
	stack2 = process_9001(copy.deepcopy(stacks), moves)
	print(get_stack_top(stack1))
	print(get_stack_top(stack2))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
