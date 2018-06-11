import igraph as ig
import pandas as pd

df = pd.read_csv("Data/june_mentions.csv")

graph = ig.Graph()  # directed graph (for now)

vertex_set = set()
for i, row in df.iterrows():
    vertex_set.add(row.creator)
    vertex_set.add(row.mentioned)

for v in vertex_set:
    graph.add_vertex(name=v)

for row in df.itertuples(index=False):
    graph.add_edge(row.mentioned, row.creator)  # arrows goes from mentioned to creator

graph = graph.simplify(combine_edges=dict(weight=sum))

originator = []
friend = []
shortest_path_lengths = []
orig_spl = []
friend_spl = []
orig_transitivities = []
friend_transitivites = []
orig_degree = []
orig_indeg = []
orig_outdeg = []
friend_degree = []
friend_indeg = []
friend_outdeg = []
for vs in graph.vs:
    name = vs.attributes()['name']
    neighbors = set()
    neighbor_objects = vs.neighbors()
    for neighbor in neighbor_objects:
        neighbors.add(neighbor.attributes()['name'])
    print(name, neighbors)
    for ovs in graph.vs:
        oname = ovs.attributes()['name']
        if vs != ovs and oname not in neighbors:
            originator.append(name)
            friend.append(oname)

            # undirected measures
            shortest_path_lengths.append(len(vs.get_shortest_paths(ovs)[0]))
            transitivites = graph.transitivity_local_undirected(vertices=[vs, ovs])
            orig_transitivities.append(transitivites[0])
            friend_transitivites.append(transitivites[1])

            # directed measures
            # orig_spl.append(vs.get_shortest_paths(ovs)[0])
            # friend_spl.append(ovs.get_shortest_paths(vs)[0])
            # orig_degree.append(vs.degree())
            # orig_indeg.append(vs.indegree())
            # orig_degree.append(vs.outdegree())
            # friend_degree.append(ovs.degree())
            # friend_indeg.append(ovs.indegree())
            # friend_outdeg.append(ovs.outdegree())


graph = ig.Graph(directed=True)  # directed graph (for now)

vertex_set = set()
for i, row in df.iterrows():
    vertex_set.add(row.creator)
    vertex_set.add(row.mentioned)

for v in vertex_set:
    graph.add_vertex(name=v)

for row in df.itertuples(index=False):
    graph.add_edge(row.mentioned, row.creator)  # arrows goes from mentioned to creator

graph = graph.simplify(combine_edges=dict(weight=sum))
for vs in graph.vs:
    name = vs.attributes()['name']
    neighbors = set()
    neighbor_objects = vs.neighbors()
    for neighbor in neighbor_objects:
        neighbors.add(neighbor.attributes()['name'])
    print(name, neighbors)
    for ovs in graph.vs:
        oname = ovs.attributes()['name']
        if vs != ovs and oname not in neighbors:
            # originator.append(name)
            # friend.append(oname)
            #
            # # undirected measures
            # shortest_path_lengths.append(len(vs.get_shortest_paths(ovs)[0]))
            # transitivites = graph.transitivity_local_undirected(vertices=[vs, ovs])
            # orig_transitivities.append(transitivites[0])
            # friend_transitivites.append(transitivites[1])

            # directed measures
            orig_spl.append(len(vs.get_shortest_paths(ovs)[0]))
            friend_spl.append(len(ovs.get_shortest_paths(vs)[0]))
            orig_degree.append(vs.degree())
            orig_indeg.append(vs.indegree())
            orig_outdeg.append(vs.outdegree())
            friend_degree.append(ovs.degree())
            friend_indeg.append(ovs.indegree())
            friend_outdeg.append(ovs.outdegree())

july_df = pd.read_csv('Data/july_mentions.csv')
july_graph = ig.Graph(directed=True)
vertex_set = set()
for i, row in july_df.iterrows():
    vertex_set.add(row.creator)
    vertex_set.add(row.mentioned)
for v in vertex_set:
    july_graph.add_vertex(name=v)
for row in july_df.itertuples(index=False):
    july_graph.add_edge(row.mentioned, row.creator)  # arrows goes from mentioned to creator

connected = []
in_connected = []
out_connected = []
for o, f in zip(originator, friend):
    neighbor_objects = july_graph.vs.find(o).neighbors(mode='ALL')
    in_neighbor_objects = july_graph.vs.find(o).neighbors(mode='IN')
    out_neighbor_objects = july_graph.vs.find(o).neighbors(mode='OUT')
    neighbors = set()
    in_neighbors = set()
    out_neighbors = set()
    for neighbor in neighbor_objects:
        neighbors.add(neighbor.attributes()['name'])
    for neighbor in in_neighbor_objects:
        in_neighbors.add(neighbor.attributes()['name'])
    for neighbor in out_neighbor_objects:
        out_neighbors.add(neighbor.attributes()['name'])
    connected.append(f in neighbors)
    in_connected.append(f in in_neighbors)
    out_connected.append(f in out_neighbors)

data = pd.DataFrame({'original': originator, 'potential_friend': friend, 'shortest_path_len': shortest_path_lengths,
                     'orig_spl': orig_spl, 'friend_spl': friend_spl, 'orig_transitivity': orig_transitivities,
                     'friend_transitivity': friend_transitivites, 'orig_degree': orig_degree,
                     'orig_indegree': orig_indeg, 'orig_outdegree': orig_outdeg, 'friend_degree': friend_degree,
                     'friend_indegree': friend_indeg, 'friend_outdegree': friend_outdeg, 'connected': connected,
                     'in_connected': in_connected, 'out_connected': out_connected})
data.to_csv('Data/graph_info_v2.csv', index=False)

