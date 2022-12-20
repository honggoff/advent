from functools import reduce
from collections import defaultdict
import math

def find_all_x_velocities(xrange):
	for vxs in range(1, xrange[1]+1):
		vx = vxs
		x = vx
		t = 1
		while x <= xrange[1] and vx > 0:
			if x >= xrange[0]:
				#print(x, vxs, vx, t, xrange[0])
				yield (vxs, t)
			vx -= 1
			x += vx
			t += 1

def find_all_y_velocities(yrange):

	for vys in range(yrange[1], -yrange[1]):
		vy = vys
		y = vy
		t = 1
		while y >= yrange[1]:
			if (y <= yrange[0]):
				yield (vys, t)
			vy -= 1
			y += vy
			t += 1

def find_all_velocities(xrange, yrange):
	yvelocities = defaultdict(list)
	for vy, t in find_all_y_velocities(yrange):
		print("y", vy, t)
		yvelocities[t].append(vy)
	tmax = max(yvelocities.keys())
	for vx, t in find_all_x_velocities(xrange):
		print("x", vx, t)
		for vy in yvelocities[t]:
			yield (vx, vy)
		if t == vx:
			for nt in range(t+1, tmax+1):
				for vy in yvelocities[nt]:
					yield (vx, vy)

def main():
	t = [x for x in find_all_velocities((20, 30), (-5, -10))]
	print(t)
	print(len(set(t)))

	t = find_all_velocities((155,215), (-72, -132))
	print(t)
	print(len(set(t)))

main()
