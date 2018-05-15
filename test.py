
import yaml
import snap
import csv
# pairs = yaml.load(open('friend_small.yaml', 'r'))

# print(len(pairs))



# UGraph = snap.GenRndGnm(snap.PUNGraph, 15,100 )
# CmtyV = snap.TCnComV()
# modularity = snap.CommunityGirvanNewman(UGraph, CmtyV)
# for Cmty in CmtyV:
#     print "Community: "
#     for NI in Cmty:
#         print NI
# print "The modularity of the network is %f" % modularity

# import snap

# Graph = snap.GenRndGnm(snap.PNGraph, 40, 100)
# snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph 1")

# UGraph = snap.GenRndGnm(snap.PUNGraph, 10, 40)
# snap.DrawGViz(UGraph, snap.gvlNeato, "11graph_undirected.png", "graph 2", True)

# NIdColorH = snap.TIntStrH()
# NIdColorH[0] = "green"
# NIdColorH[1] = "red"
# NIdColorH[2] = "purple"
# NIdColorH[3] = "blue"
# NIdColorH[4] = "yellow"
# Network = snap.GenRndGnm(snap.PNEANet, 5, 10)
# snap.DrawGViz(Network, snap.gvlSfdp, "network.png", "graph 3", True, NIdColorH)


def get_top_n(top_n):

    graph = snap.LoadEdgeList(snap.PUNGraph, "edges_bigdata.csv", 0, 1, ',')
    num_node = graph.GetNodes()
    num_remove = num_node - top_n

    # graph.Dump()
    PRankH = snap.TIntFltH()
    snap.GetPageRank(graph, PRankH)
    list_prank = []
    for item in PRankH:
        list_prank.append([item, PRankH[item]])
        # print item, PRankH[item]
    list_prank = sorted(list_prank, key=lambda x: x[1])
    remove_node = list_prank[: num_remove]

    with open("top_nodes.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(remove_node)

    for node in remove_node:
        graph.DelNode(node[0])
    snap.SaveEdgeList(graph, 'undirected_mygraph.txt')
    # graph.Dump()
get_top_n(100)
