import string
import random
la = string.ascii_lowercase
ua = string.ascii_uppercase

def random_name(n):
	"""
	n is number of name
	"""
	name_set = {"Soda"}
	while True:
		rand_name_len = random.randint(0, 10)
		name = ua[random.randint(0, 25)]
		for i in range(rand_name_len):
			name  = name + la[random.randint(0, 25)]
		name_set.add(name)
		if len(name_set) == n:
			break

	return name_set




if __name__ == '__main__':
	name_set = random_name(10)
	for name in name_set:
		print(name)