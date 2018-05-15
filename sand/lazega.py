
# Load the "Lazega" graph into Python from the SAND book.

import igraph as ig
import pandas as pd


# Created in R via:
# > library(igraph)
# > library(sand)
# > write.table(get.edgelist(lazega),row.names=FALSE,sep=" ",quote=FALSE,
#   col.names=FALSE, file="elist_lazega.ncol")
g = ig.Graph.Read_Ncol("elist_lazega.ncol",weights="if_present",
    directed=False)

# Created in R via:
#   attrs <- list.vertex.attributes(lazega)
#   cols <- vector("list", length(attrs))
#   for (i in 1:length(cols)) {
#       cols[[i]] <- get.vertex.attribute(lazega,attrs[i])
#   }
#   v.attr.lazega <- data.frame(cols)
#   names(v.attr.lazega) <- list.vertex.attributes(lazega)
# > write.csv(v.attr.lazega,row.names=FALSE,file="v_attr_lazega.csv")
# (Note: in order to work, this very much depends on the vertices appearing
#   in the .ncol file in the same order as they appear in the .csv file!)
v_attr_df = pd.read_csv("v_attr_lazega.csv")
for col in v_attr_df.columns[1:]:
    g.vs[col] = v_attr_df[col]


# Some plotting defaults, to give you the idea. When I run this, I get a file
# called "aplot.pdf" produced with the plot. Yours may auto-appear, not sure.
style = {'margin':70}
ig.plot(g,"aplot.pdf",
    vertex_label=g.vs['name'],
    vertex_size=18,
    vertex_label_dist=2,
    layout=g.layout("kk"),
    **style)

