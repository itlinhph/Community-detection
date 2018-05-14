
import yaml
import snap

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

NIdColorH = snap.TIntStrH()
NIdColorH[0] = "green"
NIdColorH[1] = "red"
NIdColorH[2] = "purple"
NIdColorH[3] = "blue"
NIdColorH[4] = "yellow"
Network = snap.GenRndGnm(snap.PNEANet, 5, 10)
snap.DrawGViz(Network, snap.gvlSfdp, "network.png", "graph 3", True, NIdColorH)