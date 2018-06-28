import csv
import networkx as nx
import numpy as np

# TODO
# Figure out LRIP
# Figure out how to compute a singular value for Katz using networkx
# Consider adding directional characteristics

fields = ['user1', 'user2', 'common_neighbors', 'adamic_adar', 'lrip', 'katz_unweighted', 'katz_weighted', 'connected']

pre_file = open("Data/june_mentions.csv", 'r', encoding='utf-8')
post_file = open("Data/july_mentions.csv", 'r', encoding='utf-8')
write_file = open("Data/features.csv", 'w', encoding='utf-8', newline='')
pre_reader = csv.reader(pre_file)
post_reader = csv.reader(post_file)
writer = csv.writer(write_file)
writer.writerow(fields)

# Structure: {u1: {u2: {'weight': 2}, u3: {'weight': 4}}, ...}
d = {}
el = []

# Pre-Epoch
next(pre_reader)
for row in pre_reader:
    if row[2] not in d.keys():
        d[row[2]] = {row[4]: {'weight': 1}}
    else:
        if row[4] not in d[row[2]].keys():
            d[row[2]][row[4]] = {'weight': 1}
        else:
            d[row[2]][row[4]]['weight'] = d[row[2]][row[4]]['weight'] + 1

# Post-Epoch
next(post_reader)
for row in post_reader:
    el.append((row[2], row[4]))

G = nx.Graph(d)
post_G = nx.Graph(el)

pre_file.close()
post_file.close()

alpha = 1 / np.real(max(nx.adjacency_spectrum(G)))  # can be messed around with
beta = 0.5  # can be messed around with

nodes = list(G.nodes())
adari = nx.adamic_adar_index(G)
cats = nx.katz_centrality(G, beta=beta)
fat_cats = nx.katz_centrality_numpy(G, alpha=alpha, beta=beta,
                                    weight='weight')
neo = nx.to_numpy_matrix(G)

adars = {}
for i in adari:
    tu = (i[0], i[1])
    adars[tu] = i[2]

# NEEDS WORK
u, s, v = np.linalg.svd(neo)
arr = np.zeros((len(u), len(v)))
for i in range(4):
    arr += s[i] * np.outer(u.T[i], v[i])

print(arr)

ones = []
twos = []
both = []
# Undirected measures
CN = []
AA = []
LRIP = []  # rank = 4 for synthetic, will mess with on actual
KatzU = []  # Beta = .5 for synthetic, will mess with on actual
KatzW = []  # Beta = .5 for synthetic, will mess with on actual
for node in nodes:
    neighbors = G[node]
    for other in nodes:
        if other != node and other not in neighbors:
            ones.append(node)
            twos.append(other)
            both.append((node, other))
            CN.append(sum(1 for x in nx.common_neighbors(G, node, other)))
            if (node, other) in adars:
                AA.append(adars[(node, other)])
            else:
                AA.append(adars[(other, node)])

connected = []
for o, t in both:
    connected.append(t in post_G[o])

for i in range(len(ones)):
    writer.writerow(ones[i], twos[i], CN[i], AA[i], LRIP[i], KatzU[i], KatzW[i], connected[i])

write_file.close()
