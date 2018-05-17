import snap
import yaml
import csv
import numpy as np

# convert yaml input file into dictionary node file and graph edge file.
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
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(list_edge)

# save dictionary to csv
def save_dict_to_csv(dict_node_file,node_names):
    with open(dict_node_file, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for key, value in node_names.items():
            writer.writerow([key, value])

# load dictionary file to dict object.
def load_nodes(dict_node_file):
    with open(dict_node_file, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        dict_ids = dict(reader)
    return dict_ids

# Creat graph from node, edge file.
def creat_graph(nodes_file, edges_files):
    nodes = load_nodes(nodes_file)
    edges = np.genfromtxt(edges_files,delimiter=',', dtype=int)
    
    graph = snap.TUNGraph.New()
    for key, node in nodes.items():
        node = int(node)
        graph.AddNode(node)
    for edge in edges:
        graph.AddEdge(edge[0], edge[1])
    
    print "Number node: ", graph.GetNodes() 
    print "Number edge:", graph.GetEdges()
    
    return graph

# Comunity detect from graph use: Girvan Newman or CNM
# Return list_comunity and modularity
def comunityDetect(graph):

    CmtyV = snap.TCnComV()
    # modularity = snap.CommunityGirvanNewman(graph, CmtyV)
    modularity = snap.CommunityCNM(graph, CmtyV)
    
    list_comunity = []
    for Cmty in CmtyV:
        comunity = []
        for NI in Cmty:
            comunity.append(NI)
        
        list_comunity.append(comunity)
    
    return list_comunity, modularity

# Visualize graph, make color all comunity
def visualize_graph(file_egdes, file_img, list_comunity):

    graph = snap.LoadEdgeList(snap.PUNGraph, file_egdes, 0, 1, '\t')
    NIdColorH = snap.TIntStrH()
    colors = ["red", "yellow", "brown", "blue", "green", "pink", "indigo", "antiquewhite","chocolate", "purple", "sienna4", "powderblue", "violet" ]
    num_color = len(colors)
    for i, comunity in enumerate(list_comunity):
        if len(comunity) ==1:
            NIdColorH[comunity[0]]= "white" 
        else:
            index = i%num_color
            for node in comunity:
                NIdColorH[node] = colors[index]

    snap.DrawGViz(graph, snap.gvlNeato, file_img, "graph visualize", True, NIdColorH)


def extract_top_nodes(edges_big_file, edges_extracted_file, top_n):

    graph = snap.LoadEdgeList(snap.PUNGraph, edges_big_file , 0, 1, '\t')
    total_node = graph.GetNodes()
    num_remove = total_node - top_n

    # Get page rank to extract top n:
    PRankH = snap.TIntFltH()
    snap.GetPageRank(graph, PRankH)
    list_prank = []
    for item in PRankH:
        list_prank.append([item, PRankH[item]])
    
    list_prank = sorted(list_prank, key=lambda x: x[1]) # Sort by page rank
    remove_node = list_prank[: num_remove]

    for node in remove_node:
        graph.DelNode(node[0])
    snap.SaveEdgeList(graph, edges_extracted_file)


# prepare_data("bigdata/friends_list.yaml", "bigdata/dict_bigdata.csv", "bigdata/edges_bigdata.csv")

edges_file = "edges_1000.csv"
num_nodes = 1000
graph_name = "graph-1000nodes.png"


extract_top_nodes("bigdata/edges_bigdata.csv", edges_file, num_nodes)
graph = snap.LoadEdgeList(snap.PUNGraph, edges_file, 0, 1, '\t')
# graph.Dump()  #show graph information

list_comunity , modularity = comunityDetect(graph)

print "list comunity: ", list_comunity
print "len list comunity: ", len(list_comunity)
print "Modularity of the network: %f" % modularity

visualize_graph(edges_file, graph_name, list_comunity)
