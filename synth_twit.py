#!/usr/bin/env python3

# Synthesize a Twitter graph, and output its tweets to a .csv file.

import numpy as np
import pandas as pd
import igraph as ig
import datetime as dt
import string
import logging

# Candidate features:
#   Shortest path length
#   Number of shortest paths
#   Similarity of attributes
#      - among intermediates
#   Local transitivity
#   Degree of intermediates
#   Centralities

try:
    with open("/usr/share/dict/words") as w:
        words = w.read().replace("'","").split('\n')
        # (Just use 1/10th of the available words. Makes it run faster.)
        words = np.random.choice(words, int(len(words)/10), replace=False)
except:
    words = ("now is the time for all good men " + \
        "to come to the aid of their country").split(" ")

# Write some number of days worth of activity to the file f.
def record_n_days_worth_of_activity(g, num_days, num_node_activities_per_day,
    start_date, f):
    for day in range(num_days):
        start_date += dt.timedelta(days=1)
        logging.info("Recording activity for {}...".format(
            start_date.strftime("%b %d")))
        nodes = np.random.choice(range(g.vcount()),
            size=num_node_activities_per_day, replace=True)
        for node in nodes:
            record_activity_for(g, node, start_date, f)

# Write a line of text to the file f for a node of the graph g, containing a
# tweet that (possibly) mentions one or more of his followees.
def record_activity_for(g, node, date, f):
    followees = g.neighbors(node, mode="in")
    if len(followees) > 0:
        recipients = np.random.choice(followees,np.random.randint(
            0, len(followees)+1), replace=False)
        tweet = gen_tweet(g, recipients)
        logging.info("{} recipients, {} of which get tweeted to".format(
            len(followees), len(recipients)))
        logging.debug("{} mentions {}".format(node,
            " and ".join([str(r) for r in recipients])))
        print('{},{},"{}",{}'.format(
            date.strftime("%a %b %d %H:%M:%S +0000 %Y"),
            node+1000,tweet,'@'+g.vs[node]['name']), file=f)
    else:
        logging.debug("{} has no one to mention".format(node))

# Generate a random tweet, containing mentions of the recipients passed (if
# any).
def gen_tweet(g, recipients):
    mentions = [ '@'+g.vs[recipient]['name'] for recipient in recipients ]
    other_words = []
    while sum([ len(w) + 1 for w in mentions + other_words]) < 140:
        other_words += [np.random.choice(words,1)[0]]
    tweet_words = mentions + other_words[:-1]
    np.random.shuffle(tweet_words)
    return ' '.join(tweet_words)


# "Adder" functions return the probability of adding an edge between a node 
# and a potential neighbor, based on various graph properties.


# An adder function that uses only the length of the shortest path (if any)
# between the node and the potential neighbor. The mode argument controls
# whether the shortest path must be directed or not (and if so, which way).
def shortest_path_length_adder(g, node, potential_followee, mode="all"):
    SHORTEST_PATH_CALIBRATION = .3
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
    screenname_length, # In chars after the "@"
    num_days_before,   # The number of simulated days before the 'epoch.'
    num_days_after,    # The number of simulated days after the 'epoch.'
    num_node_activities_per_day,  # The number of events (tweets, essentially)
                                  # that will take place per day.
    adder,             # The adder function to determine probabilities.
    remover,           # The remover function to determine probabilities.
    output_filename="tweets.csv", 
    plot=True):

    saved_args = locals()

    with open(output_filename, "w") as f:

        # Output paper trail.
        print("# Synthetic Twitter data set", file=f)
        print("# Generated with synth_twit.py with following parameters:",
            file=f)
        print("# num_nodes: {}".format(num_nodes), file=f)
        for var,val in saved_args.items():
            print("# {}: {}".format(var,val), file=f)
        print("created_at,id,text,user_screen_name", file=f)

        # Create an ER random graph.
        logging.info("Creating graph...")
        pre_epoch_graph = ig.Graph.Erdos_Renyi(num_nodes, p, directed=True)
        pre_epoch_graph.es['color'] = 'black'
        pre_epoch_graph.vs['name'] = [ ''.join(np.random.choice(
                list(string.ascii_lowercase + string.digits),
                size=screenname_length))
            for _ in range(num_nodes) ]

        seven_neighbors = pre_epoch_graph.neighbors(7, mode="in")
        print("Right now, {} (7) is only receiving influence from: {}".format(
            pre_epoch_graph.vs[7]['name'], seven_neighbors))

        # 1. Simulate the time before the epoch. For each day, perform some
        # number of actions with a node (chosen with replacement).
        record_n_days_worth_of_activity(pre_epoch_graph, num_days_before,
            num_node_activities_per_day, dt.datetime.today(), f)

        # 2. Make mid-epoch changes. For each connection that exists in the
        # pre-epoch graph, sever it with some probability based on the
        # function passed. For each connection that doesn't exist in the
        # pre-epoch graph, add it with some probability based on the function
        # passed.
        post_epoch_graph = pre_epoch_graph.copy()
        for node in range(num_nodes):
            these_followees = set(post_epoch_graph.neighbors(node, mode="in"))
            these_non_followees = set(range(num_nodes)) - {node} - \
                these_followees
            for followee in these_followees:
                logging.debug("Considering severing {}<-{}".format(
                                                            node,followee))
            for non_followee in these_non_followees:
                logging.debug("Considering adding {}<-{}".format(
                                                        node,non_followee))
                if (np.random.uniform() < adder(
                                    post_epoch_graph,node,non_followee)):
                    if node == 7:
                        logging.error("@{} (7) now follows @{} ({})".format(
                            post_epoch_graph.vs[node]['name'],
                            post_epoch_graph.vs[non_followee]['name'],
                            non_followee))
                    post_epoch_graph.add_edge(non_followee, node,
                                                        color='red',width=2)
            
        # 3. Simulate the time after the epoch. For each day, perform some
        # number of actions with a node (chosen with replacement).
        record_n_days_worth_of_activity(post_epoch_graph, num_days_after,
            num_node_activities_per_day, dt.datetime.today() + 
                dt.timedelta(days=num_days_before), f)

        if plot:
            style = { 'vertex_color': 'lightblue' }
            layout = pre_epoch_graph.layout_kamada_kawai(seed=None)
            ig.plot(pre_epoch_graph, "before.pdf", layout=layout,
                vertex_label=range(pre_epoch_graph.vcount()), **style)
            ig.plot(post_epoch_graph, "after.pdf", layout=layout,
                vertex_label=range(post_epoch_graph.vcount()), **style)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.critical("Running...")
    synth_twit(num_nodes=20, p=.1,
        screenname_length=5,
        num_days_before=30,
        num_days_after=30,
        num_node_activities_per_day=30,
        adder=shortest_path_length_adder,
        remover=None)
