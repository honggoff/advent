import re
from collections import defaultdict
from collections import namedtuple
from collections import OrderedDict

TASK_DURATION_CONSTANT = 0

class Step:
	def __init__(self, name):
		self.name = name
		self.before = []
		self.after = []
		self.duration = ord(self.name) - 64 + TASK_DURATION_CONSTANT

	def __str__(self):
		return "Step({}, before={}, after={})".format(self.name, [b.name for b in self.before], [a.name for a in self.after])

	def start(self, time):
		self.start = time

	def done(self, time):
		return self.start + self.duration <= time


class Steps(defaultdict):
	def __missing__(self, key):
		item = Step(key)
		self.__setitem__(key, item)
		return item


def read_input(filename):
	steps = Steps()
	with open(filename, 'r') as f:
		for l in f:
			m = re.match('Step (.) must be finished before step (.) can begin.', l)
			a, b = m.groups()
			steps[a].after.append(steps[b])
			steps[b].before.append(steps[a])
	start = {}
	for n, s in steps.items():
		if not s.before:
			start[s.name] = s
	return start


def pop_next_step(steps):
	next_name = sorted(steps.keys())[0]
	next_step = steps[next_name]
	del steps[next_name]
	return next_step


def immediate_execution(start):
	runnable = start
	order = []
	ran = set()
	while runnable:
		s = pop_next_step(runnable)
		ran.add(s.name)
		#print("running ", s)
		order.append(s)
		for a in s.after:
			#print("considering ", a.name)
			if all(b.name in ran for b in a.before):
				#print("taken")
				runnable[a.name] = a
	return order


def timed_execution(start, workers):
	idle_workers = workers
	runnable = start
	done = set()
	running = {}
	time = 0
	while runnable or (idle_workers < workers):
		for s in list(running.values()):
			if s.done(time):
				idle_workers += 1
				done.add(s.name)
				del running[s.name]
				for a in s.after:
					if all(b.name in done for b in a.before):
						runnable[a.name] = a
		while idle_workers and runnable:
			s = pop_next_step(runnable)
			s.start(time)
			idle_workers -= 1
			running[s.name] = s
		time += 1
		#print("second {} in work {} done {}".format(time, running.keys(), done))
	return time - 1


def print_order(order):
	print(''.join(s.name for s in order))


print_order(immediate_execution(read_input('test_input')))
print_order(immediate_execution(read_input('input')))

print("test execution takes {}s".format(timed_execution(read_input('test_input'), 2)))
TASK_DURATION_CONSTANT = 60
print("real execution takes {}s".format(timed_execution(read_input('input'), 5)))
