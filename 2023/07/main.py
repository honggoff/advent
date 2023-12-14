from pprint import pprint
from collections import Counter
from functools import cmp_to_key


FIVE_OF_A_KIND = 1
FOUR_OF_A_KIND = 2
FULL_HOUSE = 3
THREE_OF_A_KIND = 4
TWO_PAIR = 5
ONE_PAIR = 6
HIGH_CARD = 7

SUB = {
'A': 13,
'K': 12,
'Q': 11,
'J': 10,
'T': 9,
'9': 8,
'8': 7,
'7': 6,
'6': 5,
'5': 4,
'4': 3,
'3': 2,
'2': 1,
}

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			hand, bet = line.split()
			yield [SUB[h] for h in hand], int(bet)


def type(hand):
	c = Counter(hand)
	if len(c) == 5:
		return HIGH_CARD
	if len(c) == 4:
		return ONE_PAIR
	if len(c) == 3:
		_, _, a = sorted(c.values())
		if a == 3:
			return THREE_OF_A_KIND
		return TWO_PAIR
	if len(c) == 2:
		_, a = sorted(c.values())
		if a == 4:
			return FOUR_OF_A_KIND
		return FULL_HOUSE
	return FIVE_OF_A_KIND


def compare_by_card(hand1, hand2):
	if hand1 < hand2:
		return -1
	if hand1 == hand2:
		return 0
	return 1


def compare(entry1, entry2):
	hand1, _ = entry1
	hand2, _ = entry2
	t1 = type(hand1)
	t2 = type(hand2)
	if t1 < t2:
		return 1
	if t1 > t2:
		return -1
	return compare_by_card(hand1, hand2)


def score(data):
	ranked = sorted((data), key=cmp_to_key(compare))
	return sum(bet * n for (_, bet), n in zip(ranked, range(1, len(ranked)+1)))


def main(filename):
	data = list(read_input(filename))
	print(sorted((data), key=cmp_to_key(compare)))
	print(score(data))


import sys
main(sys.argv[1])
