#!/usr/bin/env python3

# Synthesize a Twitter graph, and output its tweets to a .csv file.

import numpy as np
import pandas as pd
import igraph as ig

# Candidate features:
#   Shortest path length
#   Number of shortest paths
#   Similarity of attributes
#      - among intermediates
#   Local transitivity
#   Degree of intermediates
#   Centralities


# Write some number of days worth of activity to the file f.
def record_n_days_worth_of_activity(g,num_days,num_node_activities_per_day,f):
    for day in range(num_days):
        nodes = np.random.choice(range(g.vcount()),
            size=num_node_activities_per_day, replace=True)
        for node in nodes:
            record_activity_for(g, node, f)

# Write a line of text to the file f for a node of the graph g, containing a
# tweet that (possibly) mentions one or more of his followees.
def record_activity_for(g, node, f):
    followees = g.neighbors(node, mode="out")
    if len(followees) > 0:
        recipient = np.random.choice(followees,1)[0]
        print("{} mentions {}".format(node,recipient))
    else:
        print("{} has no one to mention".format(node))


# "Adder" functions return the probability of adding an edge between a node 
# and a potential neighbor, based on various graph properties.


# An adder function that uses only the length of the shortest path (if any)
# between the node and the potential neighbor. The mode argument controls
# whether the shortest path must be directed or not (and if so, which way).
def shortest_path_length_adder(g, node, potential_followee, mode="out"):
    SHORTEST_PATH_CALIBRATION = .1
    sp = g.get_shortest_paths(node, potential_followee, mode=mode)[0]
    if len(sp) == 0:
        # Not connected at all. Return 0 (no chance of adding).
        return 0
    return 1/len(sp) * SHORTEST_PATH_CALIBRATION


# Main function. Synthesize a Twitter graph, and output its tweets to the
# filename passed, overwriting if it exists.
def synth_twit(
    num_nodes,         # The Erdos-Reyni n
    p,                 # The Erdos-Reyni p
    num_days_before,   # The number of simulated days before the 'epoch.'
    num_days_after,    # The number of simulated days after the 'epoch.'
    num_node_activities_per_day,  # The number of events (tweets, essentially)
                                  # that will take place per day.
    adder,             # The adder function to determine probabilities.
    remover,           # The remover function to determine probabilities.
    output_filename="tweets.csv", 
    plot=True):

    with open(output_filename, "w") as f:

        # Create an ER random graph.
        pre_epoch_graph = ig.Graph.Erdos_Renyi(num_nodes, p, directed=True)
        pre_epoch_graph.es['color'] = 'black'



        # 1. Simulate the time before the epoch. For each day, perform some
        # number of actions with a node (chosen with replacement).
        record_n_days_worth_of_activity(pre_epoch_graph, num_days_before,
            num_node_activities_per_day, f)

        # 2. Make mid-epoch changes. For each connection that exists in the
        # pre-epoch graph, sever it with some probability based on the
        # function passed. For each connection that doesn't exist in the
        # pre-epoch graph, add it with some probability based on the function
        # passed.
        post_epoch_graph = pre_epoch_graph.copy()
        for node in range(num_nodes):
            these_followees = set(pre_epoch_graph.neighbors(node, mode="out"))
            these_non_followees = set(range(num_nodes)) - {node} - \
                these_followees
            for followee in these_followees:
                print("Considering severing {}->{}".format(node,followee))
            for non_followee in these_non_followees:
                print("Considering adding {}->{}".format(node,non_followee))
                if (np.random.uniform() < adder(
                                    post_epoch_graph,node,non_followee)):
                    post_epoch_graph.add_edge(node, non_followee, 
                                                        color='red',width=2)
            
        # 3. Simulate the time after the epoch. For each day, perform some
        # number of actions with a node (chosen with replacement).
        record_n_days_worth_of_activity(post_epoch_graph, num_days_after,
            num_node_activities_per_day, f)

        if plot:
            style = { 'vertex_color': 'lightblue' }
            layout = pre_epoch_graph.layout_kamada_kawai(seed=None)
            ig.plot(pre_epoch_graph, "before.pdf", layout=layout,
                vertex_label=range(pre_epoch_graph.vcount()), **style)
            ig.plot(post_epoch_graph, "after.pdf", layout=layout,
                vertex_label=range(post_epoch_graph.vcount()), **style)


if __name__ == "__main__":
    print("Running...")
    synth_twit(num_nodes=20, p=.1,
        num_days_before=5,
        num_days_after=5,
        num_node_activities_per_day=2,
        adder=shortest_path_length_adder,
        remover=None)
        
