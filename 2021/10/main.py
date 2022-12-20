def read_input(filename):
	with open(filename, 'r') as f:
		for l in f:
			yield l

DELIM = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
}

CORRUP_SCORE = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137,
}

MISSING_SCORE = {
	')': 1,
	']': 2,
	'}': 3,
	'>': 4,
}

def check_corrupted(line):
	stack = []
	for c in line.strip():
		if c in DELIM:
			stack.append(c)
		elif c == DELIM[stack[-1]]:
			stack.pop()
		else:
			return c

def check_incomplete(line):
	stack = []
	for c in line.strip():
		if c in DELIM:
			stack.append(c)
		elif c == DELIM[stack[-1]]:
			stack.pop()
		else:
			return
	return stack

def missing_score(missing):
	score = 0
	while missing:
		m = missing.pop()
		score = score * 5 + MISSING_SCORE[DELIM[m]]
	return score

def main(filename):
	lines = read_input(filename)
	sum = 0
	missing_scores = []
	for line in lines:
		error = check_corrupted(line)
		if error:
			sum += CORRUP_SCORE[error]
		missing = check_incomplete(line)
		if missing:
			missing_scores.append(missing_score(missing))
	print(sum)
	print(sorted(missing_scores)[int(len(missing_scores)/2)])

import sys
main(sys.argv[1])
