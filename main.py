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
    # if closed_list is None:
    #     g_score[current] = get_g_score(parent) + get_edge_weight(parent, current)
    # else:
    #     total_path_distance = 0
    #     for index in range(len(closed_list) - 1):
    #         total_path_distance += get_edge_weight(closed_list[index], closed_list[index + 1])
    #
    #     total_path_distance += get_edge_weight(parent, current)
    #     g_score[current] = total_path_distance
    g_score[current] = get_edge_weight(parent, current)


def get_h_score(current):
    return h_score[current]


def set_h_score(current, target):
    # h_score[current] = abs(current - target)
    h_score[current] = 0
    # print("G[0]:\n", G[0][1]['weight'])
    # running_total = 0
    # for index in range(len(G[current])):
    #     if not index == current:
    #         running_total += G[current][index]['weight']
    #
    # h_score[current] = running_total
    # h_score[current] = get_edge_weight(target, current)
    # sum = 0
    # for i in range(len(list(problem.get_nodes()))):
    #     if not i == current:
    #         sum += get_edge_weight(current, i)
    #
    # # print(sum)
    #
    # h_score[current] = sum


def get_f_score(current):
    return f_score[current]


def set_f_score(current):
    f_score[current] = 0
    f_score[current] = get_g_score(current) + get_h_score(current)
    # print("xxx-----F-Score of Current---xxx:", current, ": ", f_score[current])


def get_node_with_lowest_f_score(open_list):
    lowest_f_score = infinity
    node_lowest_f_score = None
    # print("\nInside func Open List[]:\n", open_list)
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
        # print("\ntotal path distance: \n", total_path_distance, "+ ", edge_weight)
        total_path_distance += edge_weight

    return total_path_distance


def a_star(start):
    open_list = [start]
    f_score[start] = g_score[start] = h_score[start] = 0
    closed_list = []
    while len(open_list) > 0:
        # print("\nIteration-------------------------------------------------------------:\n")
        # print("\n F_Score[]:\n", f_score)
        current_node = get_node_with_lowest_f_score(open_list)
        # print("\nCurrent Node:\n", current_node)
        closed_list.append(current_node)
        # print("\nClosed List[](After append):\n", closed_list)
        open_list.remove(current_node)
        # print("\nOpen List[](After removal):\n", open_list)
        # print("\nF[]: ", f_score)
        # print("\nG[]: ", g_score)
        # print("\nh[]: ", h_score)
        for neighbour in range(len(G[current_node])):
            if not neighbour == current_node:
                if neighbour_has_lower_g_value(neighbour, current_node) and is_in_closed_list(neighbour,
                                                                                              closed_list):
                    # set_g_score(neighbour, current_node)
                    set_g_score(neighbour, current_node, closed_list)
                    set_f_score(neighbour)
                    # parent[neighbour] = current_node
                elif current_has_lower_g_value(neighbour, current_node) and is_in_open_list(neighbour, open_list):
                    set_g_score(neighbour, current_node, closed_list)
                    # set_g_score(neighbour, current_node)
                    set_f_score(neighbour)
                    parent[neighbour] = current_node
                elif not is_in_open_list(neighbour, open_list) and not is_in_closed_list(neighbour, closed_list):
                    if not is_in_closed_list(neighbour, closed_list):
                        open_list.append(neighbour)
                        set_g_score(neighbour, start)
                        # set_g_score(neighbour, current_node, closed_list)
                        set_h_score(neighbour, start)
                        set_f_score(neighbour)

    # print("\n g_score: \n", g_score)
    # print("\n Parent[]: \n", parent)
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
    # most_optimal_path.append(a_star(0))

    index_most_optimal = 0
    shortest_path_found = []
    for index in range(len(list(problem.get_nodes()))):
        if most_optimal_path[index_most_optimal][0] <= most_optimal_path[index][0]:
            pass
        else:
            index_most_optimal = index

    print("\n Path ", index_most_optimal, ": ", most_optimal_path[index_most_optimal], '\n')
    # print("\n Path ", 0, ": ", most_optimal_path[0], '\n')


main()
