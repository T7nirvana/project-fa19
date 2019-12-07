import os
import random
import sys
import pandas as pd
from ACO import *

sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from sklearn.cluster import KMeans
from student_utils import *

"""
======================================================================
  Complete the following function.
======================================================================
"""
def generate_network(size,arange):
    res=[]
    for i in range(size):
        res.append(random.randint(0, arange-1))
    return res
def get_neighborhood(center, radix, domain):
    """Get the range gaussian of given radix around a center index."""

    # Impose an upper bound on the radix to prevent NaN and blocks
    if radix < 1:
        radix = 1

    # Compute the circular network distance to the center
    deltas = np.absolute(center - np.arange(domain))
    distances = np.minimum(deltas, domain - deltas)

    # Compute Gaussian distribution around the given center
    return np.exp(-(distances*distances) / (2*(radix*radix)))

# def som(locations,tsp_matrix,iterations=100000,learning_rates=0.8):
#     size=len(tsp_matrix)*8
#     network=generate_network(size,len(tsp_matrix))
#
#     for i in range(iterations)
#         location=locations.sample(1)['index'].values
#         winner_idx=tsp_matrix[location][network].argmin()
#
#         gaussian=get_neighborhood(winner_idx,size//10,len(network))

# def tsp(dropoff_set,tsp_matrix):
#     cycle=[]
#     cycle.append(0)
#     this_index=dropoff_set.index(0)
#     next=min(tsp_matrix[this_index]).argmin()
#     while len(cycle)<len(dropoff_set):
#         cycle.append(dropoff_set[next])
#         this_index=dropoff_set.index(next)
#         next=min(tsp_matrix[this_index].argmin())
#
#     cycle.append(0)
#     return cycle


def name2indice(list_of_location, list_of_name):
    return [list_of_location.index(name) for name in list_of_name]


def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    home_index = name2indice(list_of_locations, list_of_homes)
    startpoint=list_of_locations.index(starting_car_location)
    car_cycle = [startpoint]
    G, _ = adjacency_matrix_to_graph(adjacency_matrix)
    predecessors, shortest = nx.floyd_warshall_predecessor_and_distance(G, 'weight')
    shortest=dict(shortest)
    disFstart = np.array([shortest[startpoint][i] for i in range(len(list_of_locations))]).reshape(-1, 1)
    clusters = max(int(round(0.25 * len(home_index))),1)
    while True:
        km = KMeans(n_clusters=clusters, init='k-means++')  # !!!可以加一个参数kmeans的聚类个数
        disFstart_new = km.fit_transform(disFstart)
        labels = km.labels_
        # centers = km.cluster_centers_
        home_label_set = set()
        for home in range(len(home_index)):
            if labels[home] not in home_label_set:
                home_label_set.add(labels[home])

        route_set = {}.fromkeys(home_label_set)

        for loc in range(len(disFstart)):
            if labels[loc] in route_set:
                if (route_set[labels[loc]] is None) or (abs(disFstart_new[loc][labels[loc]]) < route_set[labels[loc]]):
                    route_set[labels[loc]] = loc

        dropoff_set = np.fromiter(route_set.values(),dtype=int) if (startpoint in route_set.values()) else np.append(np.fromiter(route_set.values(),dtype=int),startpoint)  # 必须包含起点
        tsp_matrix = np.array([[shortest[i][q] for q in dropoff_set] for i in dropoff_set])
        tsp_G, _ = adjacency_matrix_to_graph(tsp_matrix)
        # for u, v, weight in G.edges.data('weight'):
        #     ...
        #     if weight is not None:
        #         ...  # Do something useful with the edges
        #     ...
        #     pass

        # for u, v, weight in tsp_G.edges.data('weight'):
        #     if weight == 0:
        #         tsp_G.remove_edge(u, v)

        if nx.is_connected(tsp_G):
            break

   # dropoff_mapping = {}.fromkeys(dropoff_set, [])
    dropoff_mapping={k: [] for k in dropoff_set}
    if startpoint in home_index:
        dropoff_mapping[startpoint].append(startpoint)
        home_index.remove(startpoint)
    for home in range(len(home_index)):
        #dropoff_mapping[route_set[labels[home]]].append(home_index[home])
        clusters_id=labels[home]
        drop_index=route_set[clusters_id]
        dropoff_mapping[drop_index].append(home_index[home])

 #   no_edge_list=np.argmin(tsp_matrix, axis=0)
#    tsp_matrix[no_edge_list]=float('inf')
    # locations=pd.DataFrame(data={"index":range(len(dropoff_set))},index=dropoff_set)
    dropoff_order = TSP(len(dropoff_set),tsp_matrix)
    cluster_order=[]
    for i in dropoff_order:
        cluster_order.append(dropoff_set[i])

    dropoff_order=cluster_order[cluster_order.index(startpoint):]+cluster_order[0:cluster_order.index(startpoint)]
    dropoff_order.append(startpoint)
    cycle = get_edges_from_path(dropoff_order[:-1]) + [(dropoff_order[-2], dropoff_order[-1])]
    for (u, v) in cycle:
        car_cycle.extend(nx.reconstruct_path(u, v, predecessors)[1:])

    return car_cycle, dropoff_mapping


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""


def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)


def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(
        input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true',
                        help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.',
                        help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
