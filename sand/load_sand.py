
# Load graphs used in Kolaczyk/Csardi ("SAND") book.

import igraph as ig
import pandas as pd
from pathlib import Path

def load_graph(name, directed=False, plot=False, plot_params={}):

    g = ig.Graph.Read_Ncol("elist_"+name+".ncol",weights="if_present",
        directed=directed)

    if Path("v_attr_"+name+".csv").exists():
        v_attr_df = pd.read_csv("v_attr_"+name+".csv")
        for col in v_attr_df.columns[1:]:
            g.vs[col] = v_attr_df[col]

    if Path("e_attr_"+name+".csv").exists():
        e_attr_df = pd.read_csv("e_attr_"+name+".csv")
        for col in e_attr_df.columns:
            g.es[col] = e_attr_df[col]

    globals()[name] = g

    if plot:
        plot_graph(name, plot_params)

    return g
    

def plot_graph(name, plot_params):
    g = globals()[name]
    style = {'margin':70, 'vertex_label_dist':2, 'vertex_size':18}
    for key,val in plot_params.items():
        if val in g.vs.attribute_names():
            style[key] = g.vs[val]
        else:
            style[key] = val
    ig.plot(globals()[name],name+".pdf",
        vertex_label=g.vs['name'],
        layout=g.layout("kk"),
        **style)

if __name__ == "__main__":
    load_graph("yeast")
    load_graph("lazega", plot=True)
    load_graph("karate", plot=True)
    load_graph("aidsblog", directed=True, plot=True)
    load_graph("macaque", directed=True, plot=True, plot_params=
        {'vertex_color':'orange',
         'vertex_shape':'shape',
         'vertex_label_dist':0,
         'vertex_size':30,
         })
