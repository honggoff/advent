from pprint import pprint
import string
from collections import defaultdict

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			card, content = line.split(':')
			card_id = int(card.split()[1])
			winning_str, present_str = content.split('|')
			winning = set(int(n) for n in winning_str.split())
			present = set(int(n) for n in present_str.split())
			yield (card_id, winning, present)


def matching(card):
	card_id, winning, present = card
	count = sum(1 for number in present if number in winning)
	return count


def worth(card):
	count = matching(card)
	return 2 ** (count - 1) if count > 0 else 0


def play_cards(cards):
	number_cards = {}
	for c, _, _ in cards:
		number_cards[c] = 1
	for card in cards:
		c = card[0]
		number = number_cards[c]
		count = matching(card)
		for i in range(c+1, c + count + 1):
			number_cards[i] += number
	return number_cards


def main(filename):
	cards = list(read_input(filename))
	pprint([(worth(card), card) for card in cards])
	print(sum(worth(card) for card in cards))
	print(sum(count for count in play_cards(cards).values()))


import sys
main(sys.argv[1])
