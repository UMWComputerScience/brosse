
# Load the "Karate" graph into Python from the R igraph package.
#Hello World
import igraph as ig
import pandas as pd
import numpy as np
import math

# Created in R via:
# library(igraph)
# library(igraphdata)
# library(stringr)
# data(karate)
# V(karate)$name <- str_replace(V(karate)$name," ","")
# V(karate)$name <- str_replace(V(karate)$name,"Actor","")
# el <- get.edgelist(karate)
# el <- cbind(el, E(karate)$weight)
# write.table(el,row.names=FALSE,sep=" ",quote=FALSE,col.names=FALSE,
#   file="elist_karate.ncol")
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
#%%
dubs = []
for i in g.vs.degree():
    i = 5*(math.sqrt(i))
    dubs.append(i)
style = {'margin':70}
g.vs['shape'] = 'circle'
g.vs.find('MrHi')['shape'] = 'rectangle'
g.vs.find('JohnA')['shape'] = 'rectangle'

vertex_sizes = [math.sqrt(30*deg) for deg in g.vs.degree()]
vertex_sizes[g.vs.find('JohnA').index] = 50
vertex_sizes[g.vs.find('MrHi').index] = 50
g.vs['size'] = vertex_sizes
offsets = [ 0 for thing in g.vs() ]
for x in g.vs.select(size_le=19):
    offsets[x.index] = 3

ig.plot(g,"aplot.pdf",
    vertex_label=g.vs['name'],
    vertex_size= vertex_sizes,
    vertex_label_dist=offsets,
    layout=g.layout("kk"),
    **style)

