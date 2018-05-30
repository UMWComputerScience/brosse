
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
alien = sg.vs.select(color='green')
human = sg.vs.select(color='blue')
humanalien = sg.es.select(_between=(alien, alien))

#%%
#Episode III
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

#%%

# 1.3
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

# II


























#ig.plot(jedi_scenes, "jedi_scenes.pdf", vertex_label=jedi_scenes.vs['name'], vertex_label_dist=-2)