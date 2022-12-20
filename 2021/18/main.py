from functools import reduce
from collections import defaultdict
import math

class Pair(object):
	def __init__(self, parent, left=None, right=None):
		self.left = left
		self.right = right
		self.parent = parent

	def __str__(self):
		return "[{},{}]".format(self.left, self.right)

	def __repr__(self):
		return "Pair({}, {}, {})".format(self.parent, repr(self.left), repr(self.right))

	def magnitude(self):
		if isinstance(self.left, Pair):
			left = self.left.magnitude()
		else:
			left = self.left
		if isinstance(self.right, Pair):
			right = self.right.magnitude()
		else:
			right = self.right
		return left * 3 + right * 2

	def split(self):
		if isinstance(self.left, Pair):
			if self.left.split():
				return True
		elif self.left >= 10:
			self.left = Pair(self, math.floor(self.left/2), math.ceil(self.left/2))
			return True
		if isinstance(self.right, Pair):
			if self.right.split():
				return True
		elif self.right >= 10:
			self.right = Pair(self, math.floor(self.right/2), math.ceil(self.right/2))
			return True
		return False

	def explode(self, level=1):
		#print("visit", self)
		if level < 4:
			to_add = Pair(None)
			if isinstance(self.left, Pair):
				to_add = self.left.explode(level + 1)
				if to_add.right:
					return self.add_right_left(to_add)

			if not to_add.parent and isinstance(self.right, Pair):
				to_add = self.right.explode(level + 1)
				if to_add.left:
					return self.add_left_right(to_add)
			return to_add

		else:
			if isinstance(self.left, Pair):
				old = self.left
				self.left = 0
				old = self.add_right_left(old)
				return old
			if isinstance(self.right, Pair):
				old = self.right
				self.right = 0
				#print("explode result", old)
				return self.add_left_right(old)
			return Pair(None)

	def add_right_left(self, pair):
		if isinstance(self.right, Pair):
			self.right.add_left(pair.right)
		else:
			self.right += pair.right
		pair.right = 0
		assert pair.parent is not None
		#print("add_right_left", pair)
		return pair

	def add_left_right(self, pair):
		if isinstance(self.left, Pair):
			self.left.add_right(pair.left)
		else:
			self.left += pair.left
		pair.left = 0
		assert pair.parent is not None
		return pair

	def add_left(self, value):
		if isinstance(self.left, Pair):
			self.left.add_left(value)
		else:
			self.left += value

	def add_right(self, value):
		if isinstance(self.right, Pair):
			self.right.add_right(value)
		else:
			self.right += value

	def reduce(self):
		while True:
			#print("reducing", self)
			result = self.explode()
			#print("after explode", self)

			if result.parent:
				continue
			if not self.split():
				return self

def parse_number(s, first, end):
	val = int(first)
	while True:
		c = next(s)
		if c in "0123456789":
			val = val * 10 + int(c)
		else:
			assert(c == end)
			return val

def parse_pair(s, parent=None):
	pair = Pair(parent)
	c = next(s)
	if c == '[':
		pair.left = parse_pair(s, pair)
		assert(next(s) == ',')
	else:
		pair.left = parse_number(s, c, ',')

	c = next(s)
	if c == '[':
		pair.right = parse_pair(s, pair)
		assert(next(s) == ']')
	else:
		pair.right = parse_number(s, c, ']')
	return pair

def parse_string(s):
	g = (c for c in s)
	assert(next(g) == '[')
	return parse_pair(g)

def main(filename):
	with open(filename, 'r') as f:
		result = add_numbers(f)
	print(result.magnitude())
	with open(filename, 'r') as f:
		print(biggest_magnitude(f))


def test_string(s, reduced):
	print("testing", s)
	number = parse_string(s)
	#test_parse
	assert s == str(number)
	#test_reduce
	number.reduce()
	assert reduced == str(number), "{} == {}".format(reduced, number)

def add(pair1, pair2):
	if pair1:
		result = Pair(None, pair1, pair2)
		pair1.parent = result
		pair2.parent = result
		result.reduce()
		return result
	return pair2

def add_numbers(number_strings):
	result = None
	for line in number_strings:
		#print("parsing", line)
		result = add(result, parse_string(line.strip()))
		#print("intermediate", result)
	return result

def biggest_magnitude(number_strings):
	s = [s for s in number_strings]
	return max(add(parse_string(s[i1]), parse_string(s[i2])).magnitude() for i1 in range(len(s)) for i2 in range(len(s)) if i1 != i2)

def test_addition(lines, expected_result):
	print("testing addition", repr(lines))
	result = add_numbers(lines.splitlines())
	assert expected_result == str(result), "{} == {}".format(expected_result, result)

def test_magnitude(s, expected_magnitude):
	print("testing magnitude", s)
	number = parse_string(s)
	assert expected_magnitude == number.magnitude()

def test():
	# explode test cases
	test_string("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
	test_string("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
	test_string("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
	test_string("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
	test_string("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
	test_string("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

	test_addition(
"""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""", "[[[[3,0],[5,3]],[4,4]],[5,5]]")
	test_addition(
"""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
""", "[[[[5,0],[7,4]],[5,5]],[6,6]]")
	test_addition(
"""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""", "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

	test_magnitude("[[1,2],[[3,4],5]]", 143)
	test_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384)
	test_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445)
	test_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791)
	test_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137)
	test_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)

	lines = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".splitlines()
	result = add_numbers(lines)
	assert result.magnitude() == 4140
	assert biggest_magnitude(lines) == 3993

import sys
if len(sys.argv) > 1:
	main(sys.argv[1])
else:
	test()
