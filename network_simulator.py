import networkx as nx
import matplotlib.pyplot as plt


N = 100
k = 1
# erdos renyi network
# G1 = nx.erdos_renyi_graph(N, k/N, directed=True)
# G1 = nx.gnp_random_graph(N, k/N) #Sensé être plus rapide pour k/N faible mais j'ai pas vu la diff
# barabasi network
# G2 = nx.barabasi_albert_graph(N, k)
# G3 = nx.gaussian_random_partition_graph(N,20,20,k/N,k/N)
# G4 = nx.watts_strogatz_graph(N, 10, 0.8)
G4 = nx.connected_watts_strogatz_graph(N, 10, 0.3, tries=30)
nx.write_gpickle(G4, 'network_simulation_{}.pkl'.format(N))


# p = 0.01 pour high local clustering but low avg path length
# https://chih-ling-hsu.github.io/2020/05/15/watts-strogatz


# G4 = nx.newman_watts_strogatz_graph(N, 10, 0.3)
# pos1 = nx.spring_layout(G1)
# nx.draw_networkx_nodes(G1, pos1, alpha = 0.6, node_size=[2*i for i in list(dict(G1.degree).values())])
# nx.draw_networkx_edges(G1, pos1, alpha=0.5)
# plt.title("Erdos-Renyi")
# plt.show()

# pos2 = nx.spring_layout(G2)
# nx.draw_networkx_nodes(G2, pos2, alpha = 0.6, node_size=[2*i for i in list(dict(G2.degree).values())])
# nx.draw_networkx_edges(G2, pos2, alpha=0.5)
# plt.title("Barabasi Albert")
# plt.show()

# pos3 = nx.spring_layout(G3)
# nx.draw_networkx_nodes(G3, pos3, alpha = 0.6, node_size=[2*i for i in list(dict(G3.degree).values())])
# nx.draw_networkx_edges(G3, pos3, alpha=0.5)
# plt.title("Gaussian random partition")
# plt.show()

pos4 = nx.spring_layout(G4)
nx.draw_networkx_nodes(G4, pos4, alpha = 0.6, node_size=[2*i for i in list(dict(G4.degree).values())])
nx.draw_networkx_edges(G4, pos4, alpha=0.2)
plt.title("watts_strogatz")
plt.show()