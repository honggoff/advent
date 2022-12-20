from functools import reduce

def read_input(filename):
	with open(filename, 'r') as f:
		for l in f:
			return l

def to_binary(string):
	for i in range(int(len(string) / 2)):
		b = int(string[2*i: 2*i+2], 16)
		for bit in reversed(range(8)):
			yield (b >> bit) & 1

def parse_int(bits, length):
	sum = 0
	for pos in reversed(range(length)):
		if next(bits):
			sum += (1 << pos)
	return sum

def parse_header(bits):
	return parse_int(bits, 3), parse_int(bits, 3)

def parse_operator_arguments(bits, consumer):
	length = 1
	values = []
	if next(bits):
		length += 11
		number_sub_packets = parse_int(bits, 11)
		print(" with {} sub-packets".format(number_sub_packets))
		for i in range(number_sub_packets):
			sub_length, value = parse_packet(bits, consumer)
			length += sub_length
			values.append(value)
	else:
		length += 15
		number_bits = parse_int(bits, 15) + length
		print(" with {} bits of sub-packets".format(number_bits))
		while length < number_bits:
			sub_length, value = parse_packet(bits, consumer)
			length += sub_length
			values.append(value)
	return length, values

def parse_literal(bits):
	value = 0
	length = 0
	while True:
		cont = next(bits)
		value = (value << 4) | parse_int(bits, 4)
		length += 5
		if not cont:
			break
	print(" with value", value)
	return length, value

def perform_operator(bits, type, consumer):
	length, values = parse_operator_arguments(bits, consumer)
	if type == 0:
		value = sum(values)
	elif type == 1:
		value = reduce(lambda x, y: x*y, values)
	elif type == 2:
		value = min(values)
	elif type == 3:
		value = max(values)
	elif type == 5:
		value = 1 if values[0] > values[1] else 0
	elif type == 6:
		value = 1 if values[0] < values[1] else 0
	elif type == 7:
		value = 1 if values[0] == values[1] else 0
	return length, value

def parse_packet(bits, consumer):
	version, type = parse_header(bits)
	consumer.send((version, type))
	if type == 4:
		print("Literal version {}".format(type, version))
		length, value = parse_literal(bits)
	else:
		print("Operator of type {}, version {}".format(type, version))
		length, value = perform_operator(bits, type, consumer)
	return 6 + length, value

def sum_versions(bits):
	version_sum = 0
	def version_adder():
		nonlocal version_sum
		while True:
			version_sum += (yield)[0]

	adder = version_adder()
	next(adder)
	parse_packet(bits, adder)
	return version_sum

def calculate(bits):
	def dummy():
		while True:
			yield
	d = dummy()
	next(d)
	_, value = parse_packet(bits, d)
	return value

def main(filename):
	string = read_input(filename)
	sum = sum_versions(to_binary(string))
	print("Sum of input is", sum)
	result = calculate(to_binary(string))
	print("Result is", result)

def test():
	data = {
		"38006F45291200": 9,
		"EE00D40C823060": 14,
		"8A004A801A8002F478": 16,
		"620080001611562C8802118E34": 12,
		"C0015000016115A2E0802F182340": 23,
		"A0016C880162017C3686B18A3D4780": 31,
	}

	for s, expected in data.items():
		print("parsing", s)
		result = sum_versions(to_binary(s))
		print("expected sum {}, actual {}".format(expected, result))
		assert(expected == result)

	calc_data = {
		"C200B40A82": 3,
		"04005AC33890": 54,
		"880086C3E88112": 7,
		"CE00C43D881120": 9,
		"D8005AC2A8F0": 1,
		"F600BC2D8F": 0,
		"9C005AC2F8F0": 0,
		"9C0141080250320F1802104A08": 1,
	}

	for s, expected in calc_data.items():
		print("parsing", s)
		result = calculate(to_binary(s))
		print("expected result {}, actual {}".format(expected, result))
		assert(expected == result)

import sys
if len(sys.argv) > 1:
	main(sys.argv[1])
else:
	test()
