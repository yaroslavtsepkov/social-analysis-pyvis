import networkx as nx
import pandas as pd
from pyvis import network


def main():

    minmaxscaler = lambda series, coeff : coeff * (series - series.min()) / (series.max() - series.min())
    nodes = pd.read_csv("source_code/dataset/stack_network_nodes.csv", dtype={"name":str, "group":int, "nodesize":float})
    nodes.columns = ["label", "group", "nodesize"]
    nodes.nodesize = minmaxscaler(nodes.nodesize, 50)
    edges = pd.read_csv("source_code/dataset/stack_network_links.csv", dtype={"sourse":str, "target":str, "value":float})
    edges.columns = ["source", "target", "weight"]
    G = nx.MultiDiGraph()
    for idx, row in nodes.iterrows():
        title = "".join((edges[edges["source"] == row.label]["target"].map(lambda x: x+"<br>")).tolist())
        G.add_node(row.label, labels=row.label, size=row.nodesize, title=title, group=row.group)
    for idx, row in edges.iterrows():
        G.add_edge(row.source, row.target, weight=row.weight)

    IG = network.Network("750px", "1000px", directed=True, bgcolor='#222222', font_color='white')
    IG.from_nx(G)
    
    IG.show_buttons(filter_=['node','physics'])
    IG.show("example/stackoverflow.html")
    

if __name__ == '__main__':
    main()
