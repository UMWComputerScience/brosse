
# Load the "aidsblog" graph into Python from the SAND book.

import igraph as ig
import pandas as pd


# Created in R via:
# > library(igraph)
# > library(sand)
# > write.table(get.edgelist(aidsblog),row.names=FALSE,sep=" ",quote=FALSE,
#   col.names=FALSE, file="elist_aidsblog.ncol")
g = ig.Graph.Read_Ncol("elist_aidsblog.ncol",weights="if_present",
    directed=True)


# Some plotting defaults, to give you the idea. When I run this, I get a file
# called "aplot.pdf" produced with the plot. Yours may auto-appear, not sure.
style = {'margin':70}
ig.plot(g,"aplot.pdf",
    vertex_label=g.vs['name'],
    vertex_size=18,
    vertex_label_dist=2,
    layout=g.layout("kk"),
    **style)

