
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
