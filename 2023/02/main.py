from pprint import pprint
from copy import copy

def read_input(filename):
	with open(filename, 'r') as f:
		games = {}
		for line in f:
			game, content = line.split(':')
			game_id = int(game.split()[1])
			sets = []
			for showing in content.split(';'):
				colorset = {}
				for color in showing.split(','):
					number, name = color.split()
					colorset[name] = int(number)
				sets.append(colorset)
			games[game_id] = sets
	return games


def is_possible(game):
	combination = {'red': 12, 'green': 13, 'blue': 14}
	for color, count in combination.items():
		for colorset in game:
			if color in colorset:
				if colorset[color] > count:
					return False
	return True


def combine_sets(a, b):
	result = copy(a)
	for color, count in b.items():
		if color in a:
			result[color] = max(count, a[color])
		else:
			result[color] = count
	return result


def minimal_set(game):
	result = {}
	for colorset in game:
		result = combine_sets(result, colorset)
	return result


def power(game):
	m =  minimal_set(game)
	return m['red'] * m['green'] * m['blue']


def main(filename):
	input = read_input(filename)
	# for game_id, game in input.items():
		# print(game_id, is_possible(game))
	# pprint(input)

	print(sum(game_id for game_id, game in input.items() if is_possible(game)))
	print(sum(power(game) for game in input.values()))

import sys
main(sys.argv[1])
