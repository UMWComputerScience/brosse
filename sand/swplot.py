
# Star Wars data sets.

import igraph as ig
import pandas as pd
import numpy as np
from pprint import pprint


characters = pd.read_csv("characters.csv")
colors = {
    'human':'blue',
    'alien':'green',
    'wookie':'brown',
    'droid':'yellow',
    '':'black',
    'IV':'orange',
    'V':'lightblue',
    'VI':'pink'
}
scenes = ig.Graph.Formula(":".join(characters.char))
scenes.vs['color'] = [ colors[species] for species in characters.species ]

scenes_df = pd.read_csv("scenes.csv")
for row in scenes_df.itertuples(index=False):
    scenes.add_edge(row.char1, row.char2, color=colors[row.ep])

style = {'margin':40}
ig.plot(scenes,"scenes.pdf",
    vertex_label=scenes.vs['name'],
    vertex_color=scenes.vs['color'],
    vertex_size=18,
    vertex_label_dist=2,
    layout=scenes.layout("kk"),
    **style)
#%%
#Episode I
top_chars = []
topchars_deg = []
for name in characters['char']:
    topchars_deg.append(scenes.vs.find(name).degree())
    top_chars.append(scenes.vs.find(name)['name'])
top_chars_deg = zip(topchars_deg, top_chars)

top_chars_deg = sorted(top_chars_deg, reverse=True)
for x, y in list(top_chars_deg[:5]):
    print(y + " appeared in " + str(x) + " scenes.")
print("-------------------------------------")
pairs = scenes.get_edgelist()
#sub = scenes.subgraph([2,9])
#ig.plot(sub, "sub.pdf", vertex_label=scenes.vs['name'])
scenes.es['weight'] = 1
sg = scenes.simplify(combine_edges=dict(weight=sum))

ig.plot(sg,"scenes_simple.pdf",
    vertex_label=scenes.vs['name'],
    vertex_color=scenes.vs['color'],
    vertex_size=18,
    vertex_label_dist=2,
    layout=scenes.layout("kk"),
    **style)

#print(sg.es['weight'])
weights = sg.es['weight']
indmax = weights.index(max(weights))
bigedge = sg.es[indmax]
bryce = zip(weights, range(len(weights)))
bryce = sorted(bryce, reverse=True)
for x,y in bryce[0:5]:
    print(sg.vs[sg.es[y].source]['name'] + " & " + sg.vs[sg.es[y].target]['name'] + " appeared in " + str(sg.vs[sg.es[y].target].degree()) + " scenes together.")
#alien = sg.vs.select(color='green')
#human = sg.vs.select(color='blue')
#humanalien = sg.es.select(_between=(alien, alien))

topchars_deg = []
top_chars_deg = []
top_chars = []
for name in characters['char']:
    topchars_deg.append(sg.vs.find(name).degree())
    top_chars.append(sg.vs.find(name)['name'])
top_chars_deg = zip(topchars_deg, top_chars)

top_chars_deg = sorted(top_chars_deg, reverse=True)
for x, y in list(top_chars_deg[:5]):
    print(y + " appeared with " + str(x) + " characters.")
print("-------------------------------------")
#%%
#Episode II
#Union deletes vertex attributes
jedi_scenes = scenes.induced_subgraph(["Vader", "Luke", "Yoda", "Emperor", "Obiwan"])
#goodguy_scenes = scenes.induced_subgraph(["Leia", "Luke", "Han", "Obiwan", "Yoda", "Lando"])
#wierd_alien_scenes = scenes.induced_subgraph(["Greedo","Chewie","Walrusman","Jabba","Ackbar","NienNunb"])
#jedi_plus_goodguy_scenes = jedi_scenes.union([goodguy_scenes])
#ig.plot(jedi_scenes, "jedi_plus_goodguy_scenes.pdf", vertex_label=jedi_scenes.vs['name'])
#%%
#Episode III
#3.1
cliqcount = []
group = []
clicks = scenes.cliques()
for i in range(len(clicks)):
    cliqcount.append(len(clicks[i]))
    group.append(clicks[i])
cliqdf = pd.DataFrame({"size":cliqcount, "nodes":group})
bigscene = scenes.vs[cliqdf.iloc[-1]['nodes']]['name']
for name in bigscene:
    print(name + ",", end=" ")
print("were all in one scenes together! That's " + str(cliqdf.iloc[-1]['size']) + " actors.")
print("---------------------------")
#3.2
names = list(characters['char'])
transitivity = list(scenes.transitivity_local_undirected(vertices=names))
ziptrans = zip(transitivity, names)
ziptrans = sorted(ziptrans, reverse=True)
for x,y in list(ziptrans):
    print(str(y) + " " + str(x))
print("Seems to be a correlation with amount of scenes with different characters")
#3.3
artic = scenes.cut_vertices()
print("Vader and Han connect the main component to Jared and Greedo respectvely")
#%%
jedi_decomp = jedi_scenes.decompose()
scenes_decomp = scenes.decompose()
for i in jedi_decomp:
    print(i)
print("\n" )
for j in scenes_decomp:
    print(j)
print("Scenes diameter", scenes.diameter())
print("Jedi diameter", jedi_scenes.diameter())
print('Closeness')
closeness = scenes.closeness()
zipclose = zip(closeness, names)
zipclose = sorted(zipclose, reverse=True)
for x,y in list(zipclose[:5]):
    print(str(y) + " " + str(x))
print('Betweenness')
betweenness = scenes.betweenness()
zipbetween = zip(betweenness, names)
zipbetween = sorted(zipbetween, reverse=True)
for x,y in list(zipbetween[:5]):
    print(str(y) + " " + str(x))
print('Eigenvector Centrality')
eigenvector_central = scenes.eigenvector_centrality()
zipeigen = zip(eigenvector_central, names)
zipeigen = sorted(zipeigen, reverse=True)
for x,y in list(zipeigen[:5]):
    print(str(y) + " " + str(x))
    
communities = scenes.community_fastgreedy()
ig.plot(communities, "com.pdf")
    
    
    
    
    
    
    
    
    
    