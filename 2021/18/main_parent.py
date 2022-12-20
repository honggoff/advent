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
		return "Pair({}, {}, {})".format(repr(self.left), repr(self.right), self.parent)

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
			if isinstance(self.left, Pair):
				to_add = self.left.explode(level + 1)
				if to_add.left:
					return to_add
				if to_add.right:
					return self.add_right_left(to_add)

			if isinstance(self.right, Pair):
				to_add = self.right.explode(level + 1)
				if to_add.left:
					return self.add_left_right(to_add)
				if to_add.right:
					return to_add
			return Pair(None)

		else:
			if isinstance(self.left, Pair):
				old = self.left
				self.left = 0
				return self.add_right_left(old)
			if isinstance(self.right, Pair):
				old = self.right
				self.right = 0
				return self.add_left_right(old)
			return Pair(None)

	def add_right_left(self, pair):
		if isinstance(self.right, Pair):
			self.right.add_left(pair.right)
		else:
			self.right += pair.right
		pair.right = 0
		return pair

	def add_left_right(self, pair):
		if isinstance(self.left, Pair):
			self.left.add_right(pair.left)
		else:
			self.left += pair.left
		pair.left = 0
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

def reduce(number):
	while True:
		result = number.explode()
		if result.parent:
			continue
		if not number.split():
			return number

def main(filename):
	pass

def test_string(s, reduced):
	print("testing", s)
	number = parse_string(s)
	#test_parse
	assert s == str(number)
	#test_reduce
	result = str(reduce(number))
	assert reduced == result, "{} == {}".format(reduced, result)

def add(pair1, pair2):
	if pair1:
		result = Pair(pair1, pair2)
		pair1.parent = result
		pair2.parent = result
		result.reduce()
		return result
	return pair2

def test_addition(lines, expected_result):
	result = None
	for line in lines.splitlines():
		result = add(result, parse_string(line.strip()))
	assert expected_result == str(result)

def test():
	# explode test cases
	test_string("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
	test_string("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
	test_string("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
	test_string("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
	test_string("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
	test_string("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

	test_addition("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""", "[[[[3,0],[5,3]],[4,4]],[5,5]]")
	#test_string("", "")

import sys
if len(sys.argv) > 1:
	main(sys.argv[1])
else:
	test()
