import functools
import collections

class Monkey:
	def __init__(self, items, operation, test, true_monkey, false_monkey):
		self.items = items
		self.operation = operation
		self.test = test
		self.true_monkey = true_monkey
		self.false_monkey = false_monkey
		self.inspections = 0

	def __str__(self):
		return 'Monkey({})'.format(self.items)

	def __repr__(self):
		fields = ('items', 'operation', 'test', 'true_monkey', 'false_monkey')
		return 'Monkey(' + ', '.join([str(self.__getattribute__(a)) for a in fields]) + ")"

	@classmethod
	def parse(cls, inp):
		item_string = next(inp).strip()
		items = [int(x) for x in item_string.split(':')[1].split(',')]

		operation_string = next(inp).strip()
		operation = operation_string.split('=')[1]

		test_string = next(inp).strip()
		test = int(test_string.split('by')[1])

		true_monkey_string = next(inp).strip()
		true_monkey = int(true_monkey_string.split('monkey')[1])

		false_monkey_string = next(inp).strip()
		false_monkey = int(false_monkey_string.split('monkey')[1])

		return cls(items, operation, test, true_monkey, false_monkey)


def read_input(filename):
	monkeys = []
	with open(filename, 'r') as f:
		for line in f:
			#print("parsing {}".format(line))
			monkeys.append(Monkey.parse(f))
			next(f)
	return monkeys


def inspect_and_throw(item, monkey, monkeys):
	item = eval(monkey.operation, {'old': item})
	item = int(item % 9699690)
	if item % monkey.test == 0:
		monkeys[monkey.true_monkey].items.append(item)
	else:
		monkeys[monkey.false_monkey].items.append(item)
	monkey.inspections += 1


def perform_turn(monkey, monkeys):
	while monkey.items:
		item = monkey.items.pop(0)
		inspect_and_throw(item, monkey, monkeys)


def perform_round(monkeys):
	for monkey in monkeys:
		perform_turn(monkey, monkeys)
		#print(list(str(m) for m in monkeys))


def calculate_monkey_business(monkeys):
	inspections = sorted((m .inspections for m in monkeys), reverse=True)
	return inspections[0] * inspections[1]


def main(filename):
	monkeys = read_input(filename)
	print(list(repr(m) for m in monkeys))
	for i in range(10000):
		perform_round(monkeys)
		print(calculate_monkey_business(monkeys))


if __name__ == "__main__":
	import sys
	main(sys.argv[1])
