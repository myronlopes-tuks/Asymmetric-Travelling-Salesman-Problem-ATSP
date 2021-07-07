import tsplib95 as tsplib
import sys
import numpy as np

filename = sys.argv[1]
final_filename = 'Sample_Problem/' + filename
problem = tsplib.load(final_filename)
# get all edges linked to node N
G = problem.get_graph()

infinity = 999999

# Instantiate the g_score array
g_score = []
for i in range(len(list(problem.get_nodes()))):
    g_score.append(infinity)

# instantiate the f_score array
f_score = []
for i in range(len(list(problem.get_nodes()))):
    f_score.append(infinity)

# instantiate the h_score array
h_score = []
for i in range(len(list(problem.get_nodes()))):
    h_score.append(infinity)

# instantiate the parent array
parent = []
for i in range(len(list(problem.get_nodes()))):
    parent.append(infinity)


def get_edge_weight(from_node, to_node):
    return G[from_node][to_node]['weight']


def get_g_score(current):
    return g_score[current]


def set_g_score(current, parent, closed_list=None):
    g_score[current] = get_edge_weight(parent, current)


def get_h_score(current):
    return h_score[current]


def set_h_score(current, target):
    h_score[current] = abs(current - target)


def get_f_score(current):
    return f_score[current]


def set_f_score(current):
    f_score[current] = 0
    f_score[current] = get_g_score(current) + get_h_score(current)


def get_node_with_lowest_f_score(open_list):
    lowest_f_score = infinity
    node_lowest_f_score = None
    for node in open_list:
        if get_f_score(node) < lowest_f_score:
            lowest_f_score = get_f_score(node)
            node_lowest_f_score = node

    return node_lowest_f_score


def is_in_closed_list(neighbour, closed_list):
    return neighbour in closed_list


def neighbour_has_lower_g_value(neighbour, current_node):
    return g_score[neighbour] <= g_score[current_node]


def current_has_lower_g_value(neighbour, current_node):
    return g_score[current_node] <= g_score[neighbour]


def is_in_open_list(neighbour, open_list):
    return neighbour in open_list


def get_total_path_distance(closed_list):
    total_path_distance = 0
    for index in range(len(closed_list) - 1):
        edge_weight = get_edge_weight(closed_list[index], closed_list[index + 1])
        total_path_distance += edge_weight

    return total_path_distance


def a_star(start):
    open_list = [start]
    f_score[start] = g_score[start] = h_score[start] = 0
    closed_list = []
    while len(open_list) > 0:
        current_node = get_node_with_lowest_f_score(open_list)
        closed_list.append(current_node)
        open_list.remove(current_node)
        for neighbour in range(len(G[current_node])):
            if not neighbour == current_node:
                if neighbour_has_lower_g_value(neighbour, current_node) and is_in_closed_list(neighbour,
                                                                                              closed_list):
                    set_f_score(neighbour)
                elif current_has_lower_g_value(neighbour, current_node) and is_in_open_list(neighbour, open_list):
                    set_g_score(neighbour, current_node, closed_list)
                    set_f_score(neighbour)
                    parent[neighbour] = current_node
                elif not is_in_open_list(neighbour, open_list) and not is_in_closed_list(neighbour, closed_list):
                    if not is_in_closed_list(neighbour, closed_list):
                        open_list.append(neighbour)
                        set_g_score(neighbour, start)
                        set_h_score(neighbour, start)
                        set_f_score(neighbour)

    closed_list.append(start)
    return [get_total_path_distance(closed_list), closed_list]


def get_adjacency_matrix():
    with open(final_filename) as f:
        instance_lines = f.readlines()

    print("\n Dimension: \n", problem.dimension)
    num_list = []
    i = 0
    for line in instance_lines:
        line = line.rstrip("\n")
        if "EOF" in line.split(" "):
            break
        if i > 6:
            [num_list.append(int(num)) for num in line.split(" ") if num.isnumeric()]
        i += 1

    print("HEREEEEEEEE", num_list)

    values = np.array(num_list)
    print("\n Values: \n", values)

    values = np.reshape(values, (problem.dimension, problem.dimension))

    return values


def main():
    most_optimal_path = []
    for starting_node in range(len(list(problem.get_nodes()))):
        most_optimal_path.append(a_star(starting_node))

    index_most_optimal = 0
    for index in range(len(list(problem.get_nodes()))):
        if most_optimal_path[index_most_optimal][0] <= most_optimal_path[index][0]:
            pass
        else:
            index_most_optimal = index

    print("Total cost of path: ", most_optimal_path[index_most_optimal][0])
    print("\nShortest path found: ", most_optimal_path[index_most_optimal][1])


main()
