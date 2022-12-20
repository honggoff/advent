from collections import deque

def read_input(filename):
	with open(filename, 'r') as f:
		return deque(int(e) for e in next(f).split(' '))


def sum_attributes(input):
	number_children = input.popleft()
	number_attributes = input.popleft()
	subtotal = 0
	for _ in range(number_children):
		subtotal += sum_attributes(input)
	for _ in range(number_attributes):
		subtotal += input.popleft()
	return subtotal


def select_attributes(input):
	number_children = input.popleft()
	number_attributes = input.popleft()
	subtotal = 0
	if not number_children:
		for a in range(number_attributes):
			subtotal += input.popleft()
	else:
		subnodes = []
		for _ in range(number_children):
			subnodes.append(select_attributes(input))
		for _ in range(number_attributes):
			a = input.popleft() - 1
			if a < number_children:
				subtotal += subnodes[a]
	return subtotal

print(sum_attributes(read_input('test_input')))
print(sum_attributes(read_input('input')))

print(select_attributes(read_input('test_input')))
print(select_attributes(read_input('input')))
