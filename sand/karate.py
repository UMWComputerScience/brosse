
# Load the "Karate" graph into Python from the R igraph package.

import igraph as ig
import pandas as pd


# Created in R via:
# library(igraphdata)
# library(stringr)
# data(karate)
# V(karate)$name <- str_replace(V(karate)$name," ","")
# V(karate)$name <- str_replace(V(karate)$name,"Actor","")
# write.table(get.edgelist(karate),row.names=FALSE,sep=" ",quote=FALSE,
#   col.names=FALSE,file="elist_karate.ncol")
g = ig.Graph.Read_Ncol("elist_karate.ncol",weights="if_present",
    directed=False)

# Created in R via:
#   V(karate)$color <- ifelse(V(karate)$color == 1, "red","blue")
#   attrs <- list.vertex.attributes(karate)
#   cols <- vector("list", length(attrs))
#   for (i in 1:length(cols)) {
#       cols[[i]] <- get.vertex.attribute(karate,attrs[i])
#   }
#   v.attr.karate <- data.frame(cols)
#   names(v.attr.karate) <- list.vertex.attributes(karate)
#   write.csv(v.attr.karate,row.names=FALSE,file="v_attr_karate.csv")
# (Note: in order to work, this very much depends on the vertices appearing
#   in the .ncol file in the same order as they appear in the .csv file!)
v_attr_df = pd.read_csv("v_attr_karate.csv")
for col in v_attr_df.columns[1:]:
    g.vs[col] = v_attr_df[col]


style = {'margin':70}
ig.plot(g,"aplot.pdf",
    vertex_label=g.vs['name'],
    vertex_size=18,
    vertex_label_dist=2,
    layout=g.layout("kk"),
    **style)

