import copy

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.strip()

def calculate_directory_size(name, path, transcript, digest):
	size = 0
	full_name = path + name + '/'
	print("entering directory {}".format(full_name))
	command = next(transcript)
	#print(command)
	assert command == '$ ls'
	for line in transcript:
		#print(line)
		tokens = line.split(' ')
		if tokens[0] == 'dir':
			pass
		elif tokens[0] == '$':
			if tokens[1] == 'cd':
				if tokens[2] == '..':
					break
				size += calculate_directory_size(tokens[2], full_name, transcript, digest)
			else:
				raise Exception('unknown command')
		else:
			size += int(tokens[0])

	assert full_name not in digest
	digest[full_name] = size
	return size

def traverse_directories(transcript):
	digest = {}
	command = next(transcript)
	assert command == '$ cd /'
	calculate_directory_size('', '', transcript, digest)
	return digest

def sum_under(digest, threshold):
	sum = 0
	for value in digest.values():
		if value < threshold:
			sum += value
	return sum

def size_to_delete(digest, target_space):
	to_be_freed = digest['/'] - target_space
	current_best = digest['/']
	for value in digest.values():
		if value > to_be_freed and value < current_best:
			current_best = value
	return current_best

def main(filename):
	transcript = read_input(filename)
	digest = traverse_directories(transcript)
	print(digest)
	print(sum_under(digest, 100000))
	print(size_to_delete(digest, 70000000 - 30000000))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
