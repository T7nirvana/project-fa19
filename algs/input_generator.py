import string
import random
la = string.ascii_lowercase
ua = string.ascii_uppercase

def random_name(n):
	"""
	n is number of name
	"""
	name_set = set(["Soda"])
	while True:
		rand_name_len = random.randint(0, 10)
		name = ua[random.randint(0, 25)]
		for i in range(rand_name_len):
			name  = name + la[random.randint(0, 25)]
		name_set.add(name)
		if len(name_set) == n:
			break

	return list(name_set)

def random_home(name_list, home_num):
	home_idx_set = set()
	home_list = []
	while True:
		idx = random.randint(0, len(name_list)-1)
		if idx not in home_idx_set and name_list[idx] is not "Soda":
			home_idx_set.add(idx)
			home_list.append(name_list[idx])

		if len(home_list) == home_num:
			break
	return home_list





if __name__ == '__main__':
	name_set = random_name(10)
	print(name_set)

	nlist = random_home(name_set, 3)
	print(nlist)
