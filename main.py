import tsplib95 as tsplib
import sys

filename = sys.argv[1]
final_filename = 'Sample_Problem/' + filename
problem = tsplib.load(final_filename)
# testing
print("\nList Of all nodes\n")
print(list(problem.get_nodes()))

print("\nList Of all Edges\n")
print(list(problem.get_edges())[0])

# get all edges linked to node N
G = problem.get_graph()
print("\nList of all Neighbours to Node 0\n")
print("G[0]:\n", G[0])

print("\nList of all Neighbours to Node 0 Using For Loop\n")
for i in range(len(G[0])):
    print("neighbour: ", G[0][i], "\n")

print("\nEdge Between Node 0 and 1\n")
print("G[0][1]:\n", G[0][1])

print("\nWeight of Edge  Between Node 0 and 1\n")
print("G[0]:\n", G[0][1]['weight'])

infinity = 999999

# Instantiate the g_score array
g_score = []
for i in range(len(list(problem.get_nodes()))):
    g_score.append(infinity)
# print("\ng_score array:\n", g_score)

# instantiate the f_score array
f_score = []
for i in range(len(list(problem.get_nodes()))):
    f_score.append(infinity)
# print("\nf_score array:\n", f_score)

# instantiate the h_score array
h_score = []
for i in range(len(list(problem.get_nodes()))):
    h_score.append(infinity)
# print("\nf_score array:\n", f_score)

# instantiate the parent array
parent = []
for i in range(len(list(problem.get_nodes()))):
    parent.append(infinity)


# print("\ng_score array:\n", parent)


def get_edge_weight(from_node, to_node):
    return G[from_node][to_node]['weight']


def get_g_score(current):
    return g_score[current]


def set_g_score(current, parent, closed_list=None):
    if closed_list is None:
        g_score[current] = get_g_score(parent) + get_edge_weight(parent, current)
    else:
        total_path_distance = 0
        for index in range(len(closed_list) - 1):
            total_path_distance += get_edge_weight(closed_list[index], closed_list[index + 1])

        total_path_distance += get_edge_weight()



def get_h_score(current):
    return h_score[current]


def set_h_score(current, target):
    # h_score[current] = abs(current - target)
    h_score[current] = 1


def get_f_score(current):
    return f_score[current]


def set_f_score(current):
    f_score[current] = get_g_score(current) + get_h_score(current)
    print("xxx-----F-Score of Current---xxx:", current, ": ", f_score[current])


def get_node_with_lowest_f_score(open_list):
    lowest_f_score = infinity
    node_lowest_f_score = None
    print("\nInside func Open List[]:\n", open_list)
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
        # if index < 16
        total_path_distance += get_edge_weight(closed_list[index], closed_list[index + 1])
        print("\nindex:\n", index)

    return total_path_distance


def a_star(start):
    open_list = [start]
    f_score[start] = g_score[start] = h_score[start] = 0
    closed_list = []
    while len(open_list) > 0:
        print("\nIteration-------------------------------------------------------------:\n")
        print("\n F_Score[]:\n", f_score)
        current_node = get_node_with_lowest_f_score(open_list)
        print("\nCurrent Node:\n", current_node)
        closed_list.append(current_node)
        print("\nClosed List[](After append):\n", closed_list)
        open_list.remove(current_node)
        print("\nOpen List[](After removal):\n", open_list)
        for neighbour in range(len(G[current_node])):
            if not G[current_node][neighbour]['weight'] == 0:
                if neighbour_has_lower_g_value(neighbour, current_node) and is_in_closed_list(neighbour,
                                                                                              closed_list):
                    parent[neighbour] = current_node
                elif current_has_lower_g_value(neighbour, current_node) and is_in_open_list(neighbour, open_list):
                    parent[neighbour] = current_node
                elif not is_in_open_list(neighbour, open_list) and not is_in_closed_list(neighbour, closed_list):
                    if not is_in_closed_list(neighbour, closed_list):
                        open_list.append(neighbour)
                        set_g_score(neighbour, current_node)
                        set_h_score(neighbour, start)
                        set_f_score(neighbour)

    print("\n g_score: \n", g_score)
    print("\n Sum of Edge weights of path: \n", )

    return [get_total_path_distance(closed_list), closed_list]


def main():
    most_optimal_path = []
    for starting_node in range(len(list(problem.get_nodes()))):
        most_optimal_path.append(a_star(starting_node))

    for index in range(len(list(problem.get_nodes()))):
        print("\n Path ", index, ": ", most_optimal_path[index], '\n')

def aStarAlgo(start_node, stop_node):

        open_set = set(start_node)
        closed_set = set()
        g = {} #store distance from starting node
        parents = {}# parents contains an adjacency map of all nodes

        #ditance of starting node from itself is zero
        g[start_node] = 0
        #start_node is root node i.e it has no parent nodes
        #so start_node is set to its own parent node
        parents[start_node] = start_node


        while len(open_set) > 0:
            n = None

            #node with lowest f() is found
            for v in open_set:
                if n == None or g[v] + heuristic(v) < g[n] + heuristic(n):
                    n = v


            if n == stop_node or Graph_nodes[n] == None:
                pass
            else:
                for (m, weight) in get_neighbors(n):
                    #nodes 'm' not in first and last set are added to first
                    #n is set its parent
                    if m not in open_set and m not in closed_set:
                        open_set.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight


                    #for each node m,compare its distance from start i.e g(m) to the
                    #from start through n node
                    else:
                        if g[m] > g[n] + weight:
                            #update g(m)
                            g[m] = g[n] + weight
                            #change parent of m to n
                            parents[m] = n

                            #if m in closed set,remove and add to open
                            if m in closed_set:
                                closed_set.remove(m)
                                open_set.add(m)

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_node)

                path.reverse()

                print('Path found: {}'.format(path))
                return path


            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_set.remove(n)
            closed_set.add(n)

        print('Path does not exist!')
        return None

#define fuction to return neighbor and its distance
#from the passed node
def get_neighbors(v):
    if v in Graph_nodes:
        return Graph_nodes[v]
    else:
        return None
#for simplicity we ll consider heuristic distances given
#and this function returns heuristic distance for all nodes
def heuristic(n):
        H_dist = {
            'A': 11,
            'B': 6,
            'C': 99,
            'D': 1,
            'E': 7,
            'G': 0,

        }

        return H_dist[n]

#Describe your graph here
Graph_nodes = {
    'A': [('B', 2), ('E', 3)],
    'B': [('C', 1),('G', 9)],
    'C': None,
    'E': [('D', 6)],
    'D': [('G', 1)],

}
aStarAlgo('A', 'G')




























main()
