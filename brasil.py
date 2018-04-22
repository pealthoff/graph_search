import csv
import networkx as nx
import heapq as hp
from heapq_max import *
from math import radians, cos, sin, asin, sqrt
from graph_search import Problem
from max_heap import MaxHeap

def getDistanceFromLatLng(lat1, lng1, lat2, lng2):
    r=6371 # radius of the earth in km
    lat1=radians(lat1)
    lat2=radians(lat2)
    lat_dif=lat2-lat1
    lng_dif=radians(lng2-lng1)
    a=sin(lat_dif/2.0)**2+cos(lat1)*cos(lat2)*sin(lng_dif/2.0)**2
    d=2*r*asin(sqrt(a))
    return d

def generate_brasil_with_h_csv():
    with open('data/br-km.csv') as br_km:
        br_km_reader = csv.reader(br_km, delimiter=',', quotechar='|')
        br_km_cities = next(br_km_reader)

    print(br_km_cities)
    brasil_with_h = open('brasil_with_h.csv', 'w')
    writer = csv.writer(brasil_with_h, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    with open('data/brasil.csv', 'r') as brasil:
        visited = []
        brasil_reader = csv.reader(brasil, delimiter=',', quotechar='|')
        row = next(brasil_reader)
        for row in brasil_reader:
            if row[1] in visited:
                print("Cidade Repetida")
                print(row[1])
            if row[1] in br_km_cities and row[1] not in visited:
                name = row[1]
                visited.append(name)
                uf = row[3]
                lat = row[5]
                lon = row[6]
                writer.writerow([name, uf, lat, lon])

    brasil_with_h.close()


# generate_brasil_with_h_csv()
def generate_graph(max_dist, max_edges):
    G = nx.Graph()
    with open('data/br-km.csv') as br_km:
        br_km_reader = csv.reader(br_km, delimiter=',', quotechar='|')
        br_km_cities = next(br_km_reader)
        br_km_cities.pop(0)
        G.add_nodes_from(br_km_cities)
        edges = []
        for city in br_km_reader:
            city_edges = []
            for i in range(1,len(city)-1):
                try:
                    num_dist = float(city[i])
                    if(num_dist < max_dist):
                        if(len(city_edges)>=max_edges):
                            heappushpop_max(city_edges, (num_dist, br_km_cities[i-1]))
                        else:
                            heappush_max(city_edges, (num_dist, br_km_cities[i]))
                except ValueError:
                    pass
            for edge in city_edges:
                edges.append((city[0], edge[1], {"distance": edge[0]}))
        G.add_edges_from(edges)
    return G

def generate_graph_lat_lon(max_dist, max_edges):
    G = nx.Graph()
    with open('data/br-km.csv') as br_km:
        br_km_reader = csv.reader(br_km, delimiter=',', quotechar='|')
        br_km_cities = next(br_km_reader)
        br_km_cities.pop(0)
        G.add_nodes_from(br_km_cities)
        edges = []
        for city in br_km_reader:
            city_edges = []
            for i in range(1,len(city)-1):
                try:
                    num_dist = float(city[i])
                    if(num_dist < max_dist):
                        if(len(city_edges)>=max_edges):
                            heappushpop_max(city_edges, (num_dist, br_km_cities[i-1]))
                        else:
                            heappush_max(city_edges, (num_dist, br_km_cities[i]))
                except ValueError:
                    pass
            for edge in city_edges:
                edges.append((city[0], edge[1], {"distance": edge[0]}))
        # G.add_edges_from(edges)
    return G

G = generate_graph(1000, 100)
print(G)
def generate_heuristic_dlr_to(city, graph):
    heuristic_dlr = {}
    city_lat = 0
    city_lon = 0
    with open('data/brasil_with_h.csv') as brwh:
        reader = csv.reader(brwh, delimiter=',', quotechar='|')
        for row in reader:
            if(row[0] == city):
                city_lat = float(row[2])
                city_lon = float(row[3])

    with open('data/brasil_with_h.csv') as brwh:
        reader = csv.reader(brwh, delimiter=',', quotechar='|')
        for row in reader:
            heuristic_dlr[row[0]] = getDistanceFromLatLng(city_lat, city_lon, float(row[2]), float(row[3]))
    for city in graph:
        if city not in heuristic_dlr:
            heuristic_dlr[city] = 10000
    return heuristic_dlr


def draw_graph(G):
    import math
    import warnings
    warnings.simplefilter('ignore', RuntimeWarning)
    for u,v,d in G.edges(data=True):
        d['label'] = d.get('distance','')
    A=nx.nx_agraph.to_agraph(G)
    A.node_attr['shape']='circle'
    A.node_attr['fixedsize']='true'
    A.node_attr['fontsize']='8'
    A.node_attr['style']='filled'
    A.graph_attr['outputorder']='edgesfirst'
    # # A.graph_attr['label']="miles_dat"
    # A.graph_attr['ratio']='1.0'
    A.edge_attr['color']='#1100FF'
    A.edge_attr['style']='setlinewidth(2)'
    with open('data/brasil_with_h.csv') as br_km:
        br_reader = csv.reader(br_km, delimiter=',', quotechar='|')
        for city in br_reader:
            # print(city)
            n=A.get_node(city[0])
            x = city[2]
            y = city[3]
            pop=100
            # assign positions, scale to be something reasonable in points
            n.attr['pos']="%f,%f)"%((float(x)),(float(y)))
            print(n.attr['pos'])
            # assign node size, in sqrt of 1,000,000's of people
            # d=math.sqrt(float(pop)/1000000.0)
            # n.attr['height']="%s"%(d/2)
            # n.attr['width']="%s"%(d/2)
            # assign node color
            # n.attr['fillcolor']="#0000%2x"%(int(d*256))
            # empty labels
            # n.attr['label']=' '

    A.layout()
    A.draw('brasil100.png',prog='fdp')

# draw_graph(G)
start = 'Rio de Janeiro'
objective = 'Ourinhos'

heuristic = generate_heuristic_dlr_to(objective, G)
rio_to_ourinhos = Problem(start, [objective], G, heuristic)
rio_to_ourinhos.solve_with_a_star()
rio_to_ourinhos.solve_with_sma_star(90)