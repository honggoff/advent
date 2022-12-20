
# 0 1 2 3 4 5 6
# 1 2 3 4 5 6 7

test_input = "dabAcCaCBAcCcaDA"

def react(polymer):
	polymer = list(polymer)
	removed = True
	while removed:
		removed = False
		for i in range(len(polymer) - 2, -1, -1):
			if i > len(polymer) - 2:
				continue
			a = polymer[i]
			b = polymer[i+1]
			if (a != b) and (a.lower() == b.lower()):
				del polymer[i:i+2]
				removed = True
	return polymer


def optimize(polymer):
	units = set(polymer.lower())
	min_score = len(polymer)
	for unit in units:
		filtered = [e for e in polymer if e.lower() != unit]
		score = len(react(filtered))
		if score < min_score:
			min_score = score
	return min_score


def read_input(filename):
	with open(filename, 'r') as f:
		return next(f).strip()

reacted = react(test_input)
print("reduced {}, optimized {}".format(len(reacted), optimize(test_input)))
input = read_input('input')
reacted = react(input)
print("reduced {}, optimized {}".format(len(reacted), optimize(input)))
