
# Load the "macaque" graph into Python from the R igraph package.

import igraph as ig
import pandas as pd
import numpy as np
import math

# Created in R via:
# library(igraph)
# library(igraphdata)
# data(macaque)
# write.table(get.edgelist(macaque),row.names=FALSE,sep=" ",quote=FALSE,
#   col.names=FALSE,file="elist_macaque.ncol")
g = ig.Graph.Read_Ncol("elist_macaque.ncol",weights="if_present",
    directed=True)

# Created in R via:
#   attrs <- list.vertex.attributes(macaque)
#   cols <- vector("list", length(attrs))
#   for (i in 1:length(cols)) {
#       cols[[i]] <- get.vertex.attribute(macaque,attrs[i])
#   }
#   v.attr.macaque <- data.frame(cols)
#   names(v.attr.macaque) <- list.vertex.attributes(macaque)
#   write.csv(v.attr.macaque,row.names=TRUE,file="v_attr_macaque.csv")
# (Note: in order to work, this very much depends on the vertices appearing
#   in the .ncol file in the same order as they appear in the .csv file!)
v_attr_df = pd.read_csv("v_attr_macaque.csv")
for col in v_attr_df.columns:
    g.vs[col] = v_attr_df[col]

style = {'margin':70}
ig.plot(g,"aplot.pdf",
    vertex_size=30,
    vertex_color='orange',
    vertex_label=g.vs['name'],
    vertex_shape=g.vs['shape'],
    layout=g.layout("kk"),
    **style)

