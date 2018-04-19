import networkx as nx
import pygraphviz as pgv
from graph_search import Problem

G = nx.Graph()
G.add_nodes_from(["Arad",
                  "Bucarest",
                  "Craiova",
                  "Drobeta",
                  "Eforie",
                  "Fagaras",
                  "Giurgiu",
                  "Hirsova",
                  "Iasi",
                  "Lugoj",
                  "Mehadia",
                  "Neamt",
                  "Oradea",
                  "Pitesti",
                  "Rimnicu Vilcea",
                  "Sibiu",
                  "Timisoara",
                  "Urziceni",
                  "Vaslui",
                  "Zerind"])

G.add_edges_from([
    ("Arad", "Timisoara", {"distance": 118}),
    ("Arad", "Zerind", {"distance": 75}),
    ("Arad", "Sibiu", {"distance": 140}),
    ("Lugoj", "Timisoara", {"distance": 111}),
    ("Lugoj", "Mehadia", {"distance": 70}),
    ("Mehadia", "Drobeta", {"distance": 75}),
    ("Drobeta", "Craiova", {"distance": 120}),
    ("Rimnicu Vilcea", "Craiova", {"distance": 146}),
    ("Pitesti", "Craiova", {"distance": 138}),
    ("Zerind", "Oradea", {"distance": 71}),
    ("Oradea", "Sibiu", {"distance": 151}),
    ("Sibiu", "Fagaras", {"distance": 99}),
    ("Sibiu", "Rimnicu Vilcea", {"distance": 80}),
    ("Rimnicu Vilcea", "Pitesti", {"distance": 97}),
    ("Pitesti", "Bucarest", {"distance": 101}),
    ("Bucarest", "Giurgiu", {"distance": 90}),
    ("Bucarest", "Urziceni", {"distance": 85}),
    ("Urziceni", "Hirsova", {"distance": 98}),
    ("Hirsova", "Eforie", {"distance": 86}),
    ("Urziceni", "Vaslui", {"distance": 142}),
    ("Vaslui", "Iasi", {"distance": 92}),
    ("Neamt", "Iasi", {"distance": 87}),
    ("Bucarest", "Fagaras", {"distance": 211})])

heuristic_dlr_to_bucarest = {
    "Arad": 366,
    "Bucarest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

romeniaProblem = Problem('Arad',['Bucarest'], G, heuristic_dlr_to_bucarest)

romeniaProblem.solve_with_a_star()

# for u,v,d in G.edges(data=True):
#     d['label'] = d.get('distance','')

# A=nx.nx_agraph.to_agraph(G)
# A.layout()
# A.draw('romenia.png')