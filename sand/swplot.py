
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
for x,y in list(top_chars_deg[:5]):
    print(y + " appeared in " + str(x) + " scenes.")

pairs = scenes.get_edgelist()
sub = scenes.subgraph([2,9])
scenes.vs['name']
ig.plot(sub, "sub.pdf", vertex_label=scenes.vs['name'])
scenes.es['weight'] = 1
sg = scenes.simplify(combine_edges=dict(weight=sum))
print(sg.es['weight'])