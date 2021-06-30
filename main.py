import tsplib95 as tsplib
import sys
# import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

filename = sys.argv[1]
final_filename = 'Sample_Problem/' + filename
problem = tsplib.load(final_filename)
# testing

print(list(problem.get_nodes()))
print(list(problem.get_edges()))

G = nx.petersen_graph()
plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

plt.show()