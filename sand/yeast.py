
# Load the "yeast" graph into Python from the R igraph package.

import igraph as ig
import pandas as pd


# Created in R via:
# library(igraph)
# data(yeast)
# write.table(get.edgelist(yeast),row.names=FALSE,sep=" ",quote=FALSE,
#   col.names=FALSE,file="elist_yeast.ncol")
g = ig.Graph.Read_Ncol("elist_yeast.ncol",weights="if_present",
    directed=False)

# Created in R via:
#   attrs <- list.vertex.attributes(yeast)
#   cols <- vector("list", length(attrs))
#   for (i in 1:length(cols)) {
#       cols[[i]] <- get.vertex.attribute(yeast,attrs[i])
#   }
#   v.attr.yeast <- data.frame(cols)
#   names(v.attr.yeast) <- list.vertex.attributes(yeast)
#   write.csv(v.attr.yeast,row.names=FALSE,file="v_attr_yeast.csv")
v_attr_df = pd.read_csv("v_attr_yeast.csv")
for col in v_attr_df.columns[1:]:
    g.vs[col] = v_attr_df[col]

# Created in R via:
#   attrs <- list.edge.attributes(yeast)
#   cols <- vector("list", length(attrs))
#   for (i in 1:length(cols)) {
#       cols[[i]] <- get.edge.attribute(yeast,attrs[i])
#   }
#   e.attr.yeast <- data.frame(cols)
#   names(e.attr.yeast) <- list.edge.attributes(yeast)
#   write.csv(e.attr.yeast,row.names=FALSE,file="e_attr_yeast.csv")
e_attr_df = pd.read_csv("e_attr_yeast.csv")
for col in e_attr_df.columns:
    g.es[col] = e_attr_df[col]
