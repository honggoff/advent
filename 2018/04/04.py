import re
from collections import namedtuple
from collections import Counter
from collections import defaultdict

Slice = namedtuple('Slice', ['guard_id', 'start', 'end'])


def read_input(filename):
	date_pattern = re.compile("\[\d+-\d+-\d+ 00:(\d\d)\]")
	guard_pattern = re.compile("Guard #(\d+) begins shift")
	start_pattern = re.compile("falls asleep")
	end_pattern = re.compile("wakes up")

	with open(filename, 'r') as f:
		start, end = None, None
		guard = None
		for l in f:
			m = guard_pattern.search(l)
			if m:
				if start is not None:
					raise Exception("newer woke up")
				guard = m.group(1)
			else:
				minute = date_pattern.match(l).group(1)
				if start_pattern.search(l):
					start = minute
				elif end_pattern.search(l):
					end = minute
					yield Slice(int(guard), int(start), int(end))
					start, end = None, None
				else:
					raise Exception("couldn't parse " + l)


def count_minutes(slices):
	counts = defaultdict(Counter)
	for slice in slices:
		counts[slice.guard_id].update(range(slice.start, slice.end))
	return counts


def strategy_one(counts):
	max_total = 0
	for id, counts in counts.items():
		total = sum(counts.values())
		if total > max_total:
			max_total = total
			max_guard_id = id
			max_value = max(counts.values())
			max_minute = next(m for m, v in counts.items() if v == max_value)
	return (max_guard_id, max_minute)


def strategy_two(counts):
	max_value = 0
	for id, counts in counts.items():
		value = max(counts.values())
		if value > max_value:
			max_value = value
			max_guard_id = id
			max_minute = next(m for m, v in counts.items() if v == max_value)
	return (max_guard_id, max_minute)

counts = count_minutes(read_input('test_input'))
guard, minute = strategy_one(counts)
print("S1 Guard {}, minute {} -> result {}".format(guard, minute, guard * minute))
guard, minute = strategy_two(counts)
print("S2 Guard {}, minute {} -> result {}".format(guard, minute, guard * minute))

counts = count_minutes(read_input('input.sorted'))
guard, minute = strategy_one(counts)
print("S1 Guard {}, minute {} -> result {}".format(guard, minute, guard * minute))
guard, minute = strategy_two(counts)
print("S2 Guard {}, minute {} -> result {}".format(guard, minute, guard * minute))
