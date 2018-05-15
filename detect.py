import snap
import yaml
import csv
import numpy as np


def prepare_data(yaml_input, dict_node_file, graph_file):

    pairs = yaml.load(open(yaml_input,'r'))
    id = 1
    nodes = {}

    for pair in pairs:
        for friend in pair:
            if not friend in nodes:
                nodes[friend] = id
                id +=1
        
    save_dict_to_csv(dict_node_file,nodes)

    list_edge = []
    for pair in pairs:
        edge = [nodes[pair[0]], nodes[pair[1]]]
        list_edge.append(edge)
    
    with open(graph_file, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list_edge)



def save_dict_to_csv(dict_node_file,node_names):
    with open(dict_node_file, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in node_names.items():
            writer.writerow([key, value])

def load_nodes(dict_node_file):
    with open(dict_node_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        dict_ids = dict(reader)
    return dict_ids


def creat_graph(nodes_file, egdes_files):
    nodes = load_nodes(nodes_file)
    edges = np.genfromtxt(egdes_files,delimiter=',', dtype=int)
    
    graph = snap.TUNGraph.New()
    for key, node in nodes.items():
        node = int(node)
        graph.AddNode(node)
    for edge in edges:
        graph.AddEdge(edge[0], edge[1])
    
    print "Number node: ", graph.GetNodes() 
    print "Number edge:", graph.GetEdges()
    
    return graph

def comunityDetect(graph):

    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(graph, CmtyV)
    # modularity = snap.CommunityCNM(graph, CmtyV)
    
    list_comunity = []
    for Cmty in CmtyV:
        comunity = []
        for NI in Cmty:
            comunity.append(NI)
        
        list_comunity.append(comunity)
    
    return list_comunity, modularity


# prepare_data("friends_list.yaml", "output/dict_bigdata.csv", "output/edges_bigdata.csv")

graph = snap.LoadEdgeList(snap.PUNGraph, "edges.csv", 0, 1, ',')
# graph.Dump()

#Visualize graph:
snap.DrawGViz(graph, snap.gvlNeato, "output/graph_small.png", "graph visualize", True)

list_comunity , modularity = comunityDetect(graph)

print "list comunity: ", list_comunity
print "Modularity of the network: %f" % modularity

