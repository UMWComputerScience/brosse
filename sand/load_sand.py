
# Load graphs used in Kolaczyk/Csardi ("SAND") book.

import igraph as ig
import pandas as pd
from pathlib import Path

def load_graph(name, directed=False, plot=False):

    g = ig.Graph.Read_Ncol("elist_"+name+".ncol",weights="if_present",
        directed=directed)

    v_attr_df = pd.read_csv("v_attr_"+name+".csv")
    for col in v_attr_df.columns[1:]:
        g.vs[col] = v_attr_df[col]

    if Path("e_attr_"+name+".csv").exists():
        e_attr_df = pd.read_csv("e_attr_"+name+".csv")
        for col in e_attr_df.columns:
            g.es[col] = e_attr_df[col]

    globals()[name] = g
    style = {'margin':70}

    if plot:
        plot_graph(name)
    

def plot_graph(name):
    g = globals()[name]
    style = {'margin':70}
    ig.plot(globals()[name],name+".pdf",
        vertex_label=g.vs['name'],
        vertex_size=18,
        vertex_label_dist=2,
        layout=g.layout("kk"),
        **style)

if __name__ == "__main__":
    load_graph("yeast")
    load_graph("lazega", plot=True)
    load_graph("karate", plot=True)
