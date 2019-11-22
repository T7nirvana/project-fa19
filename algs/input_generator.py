import string
import os
import random
la = string.ascii_lowercase
ua = string.ascii_uppercase
script_path = os.path.abspath(__file__)
script_dir = script_path[:script_path.rfind("algs")]
io_path = script_dir + "io/"

def random_name(n):
	"""
	n is number of name
	"""
	name_set = set(["Soda"])

	while True:
		rand_name_len = random.randint(3, 10) # 3 <= len <= 10
		name = ua[random.randint(0, 25)]
		for _ in range(rand_name_len):
			name  = name + la[random.randint(0, 25)]
		name_set.add(name)
		if len(name_set) == n:
			break
	name_list = list(name_set)
	return name_list

def random_home(name_list, home_num):
	home_idx_set = set()
	home_list = []
	while True:
		idx = random.randint(0, len(name_list)-1)
		if idx not in home_idx_set:
			home_idx_set.add(idx)
			home_list.append(name_list[idx])

		if len(home_list) == home_num:
			break
	return home_list


def adjacent_matrix(m,n):
	return "here is the matrix"


def random_input(m, n):
	"""
	m the number of locations, n the number of TA's home
	"""
	in_str = str(m) + '\n' + str(n) + '\n'
	locations = random_name(m)
	for loc in locations:
		in_str = in_str + str(loc) + ' '
	in_str = in_str + '\n'
	homes = random_home(locations, n)
	for home in homes:
		in_str = in_str + str(home) + ' '
	in_str = in_str + '\n' + 'Soda' + '\n'
	in_str = in_str + adjacent_matrix(m,n) + '\n'
	return in_str


def save_file(m, n):
	in_str = random_input(m, n)
	with open(io_path + "%s.in"%m, 'w+') as f:
		f.write(in_str)



if __name__ == '__main__':
	name_set = random_name(10)
	print(name_set)

	nlist = random_home(name_set, 3)
	print(nlist)

	print(random_input(10, 3))

	save_file(10, 3)

