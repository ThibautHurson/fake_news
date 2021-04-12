import networkx as nx
import matplotlib.pyplot as plt
import collections

fh = open("FB_network.txt", "rb")
G = nx.read_edgelist(fh)
print(nx.number_of_nodes(G))
fh.close()

print(G.nodes())
#nx.write_gpickle(G, 'fb_network.pkl')