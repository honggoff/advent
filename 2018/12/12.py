import re

class Ruleset:
	def __init__(self):
		self._rules = set()

	def add_rule(self, rule):
		m = re.match("(.....) => (.)", rule)
		pattern = tuple(p == '#' for p in m.group(1))
		value = m.group(2) == '#'
		if value:
			self._rules.add(pattern)

	def match(self, pattern):
		return pattern in self._rules


class Pots:
	PADSIZE = 100
	def __init__(self, values, rules):
		self._values = [p == '#' for p in values]
		self._next_generation = [False] * len(self._values)
		self._rules = rules
		self._offset = 0

	def _pad(self):
		if any(self._values[0:3]):
			self._values = [False] * self.PADSIZE + self._values
			self._offset -= self.PADSIZE
		if any(self._values[-3:]):
			self._values = self._values + [False] * self.PADSIZE
		if len(self._values) != len(self._next_generation):
			self._next_generation = [False] * len(self._values)
			print("padded")

	def generation(self):
		self._pad()
		for i in range(2, len(self._values) - 2):
			pattern = tuple(self._values[i-2:i+3])
			self._next_generation[i] = self._rules.match(pattern)
		self._values, self._next_generation = self._next_generation, self._values
		#print("".join('#' if p else '.' for p in self._values))


	def count_alive_numbers(self):
		return sum(v for v, s in zip(range(self._offset, len(self._values)), self._values) if s)


def read_input(filename):
	with open(filename, 'r') as f:
		pot_string = next(f).split(" ")[2].strip()
		rules = Ruleset()
		assert(next(f).strip() == '')
		for l in f:
			rules.add_rule(l.strip())
		pots = Pots(pot_string, rules)
		return pots

def generate(filename, generations):
	pots = read_input(filename)
	percent = generations / 100
	next_percent = percent
	for g in range(generations):
		pots.generation()
		if g > next_percent:
			print("{}%".format(g / generations * 100))
			next_percent += percent

	print(pots.count_alive_numbers())

generate('test_input', 20)
generate('input', 20)
generate('input', 50000000000)
import cProfile
cProfile.run('generate("input", 50000000000)')
