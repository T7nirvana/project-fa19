import networkx as nx
import numpy as np

# new utils 
import matplotlib.pyplot as plt;
import matplotlib;
def show(G):
    plt.figure()
    nx.draw_random(G)
    plt.show()

def graph_to_matrix(G):
    node_num = len(G)
    mat = ['x' for _ in range(node_num*node_num)]
    for u,v,weight in G.edges.data('weight'):
        # print(u)
        # print(v)
        # print(str(weight))
        mat[u*node_num + v] = str(weight)
        mat[v*node_num + u] = str(weight)
        
    mat_str=""
    for i in range(node_num):
        for j in range(node_num):
            mat_str = mat_str + mat[i*node_num + j] + ' '
        mat_str = mat_str + '\n'
    return mat_str

# def random_metric_graph(n, pos = None):
#     G = nx.Graph()
#     G.add_nodes_from(range(n))
#     # print(len(G))
#     if pos is None:
#         pos = {v: [random.random()*1000 for _ in range(2)] for v in range(n)}

#     print(pos)
#     nx.set_node_attributes(G, pos, 'pos')

#     return G

    # node_weights = [adjacency_matrix[i][i] for i in range(len(adjacency_matrix))]
    # adjacency_matrix_formatted = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]

    # for i in range(len(adjacency_matrix_formatted)):
    #     adjacency_matrix_formatted[i][i] = 0

    # G = nx.convert_matrix.from_numpy_matrix(np.matrix(adjacency_matrix_formatted))

    # message = ''

    # for node, datadict in G.nodes.items():
    #     if node_weights[node] != 'x':
    #         message += 'The location {} has a road to itself. This is not allowed.\n'.format(node)
    #     datadict['weight'] = node_weights[node]

    # return G, message
# official utils

def decimal_digits_check(number):
    number = str(number)
    parts = number.split('.')
    if len(parts) == 1:
        return True
    else:
        return len(parts[1]) <= 5


def data_parser(input_data):
    number_of_locations = int(input_data[0][0])
    number_of_houses = int(input_data[1][0])
    list_of_locations = input_data[2]
    list_of_houses = input_data[3]
    starting_location = input_data[4][0]

    adjacency_matrix = [[entry if entry == 'x' else float(entry) for entry in row] for row in input_data[5:]]
    return number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix


def adjacency_matrix_to_graph(adjacency_matrix):
    node_weights = [adjacency_matrix[i][i] for i in range(len(adjacency_matrix))]
    adjacency_matrix_formatted = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]

    for i in range(len(adjacency_matrix_formatted)):
        adjacency_matrix_formatted[i][i] = 0

    G = nx.convert_matrix.from_numpy_matrix(np.matrix(adjacency_matrix_formatted))

    message = ''

    for node, datadict in G.nodes.items():
        if node_weights[node] != 'x':
            message += 'The location {} has a road to itself. This is not allowed.\n'.format(node)
        datadict['weight'] = node_weights[node]

    return G, message


def is_metric(G):
    shortest = dict(nx.floyd_warshall(G))
    for u, v, datadict in G.edges(data=True):
        if abs(shortest[u][v] - datadict['weight']) >= 0.00001:
            # print("w%s"%datadict['weight'])
            # print("s%s"%shortest[u][v])
            return False
            # print(u)
            # print(v)
    return True


def adjacency_matrix_to_edge_list(adjacency_matrix):
    edge_list = []
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[0])):
            if adjacency_matrix[i][j] == 1:
                edge_list.append((i, j))
    return edge_list


def is_valid_walk(G, closed_walk):
    '''
    each edges taken actually can be found in the graph
    Notice, A->A is not valid tho
    '''
    return all([(closed_walk[i], closed_walk[i+1]) in G.edges for i in range(len(closed_walk) - 1)])


def get_edges_from_path(path):
    return [(path[i], path[i+1]) for i in range(len(path) - 1)]

"""
G is the adjacency matrix.
car_cycle is the cycle of the car in terms of indices.
dropoff_mapping is a dictionary of dropoff location to list of TAs that got off at said droppoff location
in terms of indices.
"""
def cost_of_solution(G, car_cycle, dropoff_mapping):
    cost = 0
    message = ''
    dropoffs = dropoff_mapping.keys()
    if not is_valid_walk(G, car_cycle):
        message += 'This is not a valid walk for the given graph.\n'
        cost = 'infinite'

    if not car_cycle[0] == car_cycle[-1]:
        message += 'The start and end vertices are not the same.\n'
        cost = 'infinite'
    if cost != 'infinite':
        if len(car_cycle) == 1:
            car_cycle = []
        else:
            car_cycle = get_edges_from_path(car_cycle[:-1]) + [(car_cycle[-2], car_cycle[-1])]
        driving_cost = sum([G.edges[e]['weight'] for e in car_cycle]) * 2 / 3
        walking_cost = 0
        shortest = dict(nx.floyd_warshall(G))

        for drop_location in dropoffs:
            for house in dropoff_mapping[drop_location]:
                walking_cost += shortest[drop_location][house]

        message += f'The driving cost of your solution is {driving_cost}.\n'
        message += f'The walking cost of your solution is {walking_cost}.\n'
        cost = driving_cost + walking_cost

    message += f'The total cost of your solution is {cost}.\n'
    return cost, message


def convert_locations_to_indices(list_to_convert, list_of_locations):
    return [list_of_locations.index(name) if name in list_of_locations else None for name in list_to_convert]
