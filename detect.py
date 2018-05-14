import snap
import yaml
import csv
import numpy as np


def prepare_data():

    pairs = yaml.load(open('friend_small.yaml','r'))
    id = 1
    friends = {}

    for pair in pairs:
        for friend in pair:
            if not friend in friends:
                friends[friend] = id
                id +=1
        
    save_id_to_csv(friends)

    list_edge = []
    for pair in pairs:
        edge = [friends[pair[0]], friends[pair[1]]]
        list_edge.append(edge)
    # print "num edges:", len(list_edge)
    
    with open("edges.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_edge)



def save_id_to_csv(dic_ids):
    with open('dict_ids.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dic_ids.items():
            writer.writerow([key, value])

def load_friends():
    with open('dict_ids.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file)
        dict_ids = dict(reader)
    return dict_ids


def creat_graph(egdes):
    graph = snap.TUNGraph.New()

    nodes = load_friends()
    for key, node in nodes.items():
        node = int(node)
        graph.AddNode(node)
    for edge in egdes:
        graph.AddEdge(edge[0], edge[1])

    return graph


# prepare_data()
# friends = load_friends()
# print "num nodes:" , len(friends)

edges = np.genfromtxt('edges.csv',delimiter=',', dtype=int)
print edges.shape
graph = creat_graph(edges)
print graph.GetNodes()
print graph.GetEdges()
snap.DrawGViz(graph, snap.gvlNeato, "graph_undirected.png", "graph 2", True)

CmtyV = snap.TCnComV()
modularity = snap.CommunityGirvanNewman(graph, CmtyV)
for Cmty in CmtyV:
    print "Community: "
    for NI in Cmty:
        print NI
print "The modularity of the network is %f" % modularity

