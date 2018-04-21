import csv
import networkx as nx
import heapq as hp
from heapq_max import *
from math import radians, cos, sin, asin, sqrt
from graph_search import Problem

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
    with open('br-km.csv') as br_km:
        br_km_reader = csv.reader(br_km, delimiter=',', quotechar='|')
        br_km_cities = next(br_km_reader)

    print(br_km_cities)
    brasil_with_h = open('brasil_with_h.csv', 'w')
    writer = csv.writer(brasil_with_h, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    with open('brasil.csv', 'r') as brasil:
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
    with open('br-km.csv') as br_km:
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
                        # city_edges.append((city[0], br_km_cities[i], {"distance": num_dist}))
                        else:
                            heappush_max(city_edges, (num_dist, br_km_cities[i]))
                except ValueError:
                    pass
            for edge in city_edges:
                edges.append((city[0], edge[1], {"distance": edge[0]}))
        G.add_edges_from(edges)
    return G

G = generate_graph(1000, 5)

def generate_heuristic_dlr_to(city, graph):
    heuristic_dlr = {}
    city_lat = 0
    city_lon = 0
    with open('brasil_with_h.csv') as brwh:
        reader = csv.reader(brwh, delimiter=',', quotechar='|')
        for row in reader:
            if(row[0] == city):
                city_lat = float(row[2])
                city_lon = float(row[3])

    with open('brasil_with_h.csv') as brwh:
        reader = csv.reader(brwh, delimiter=',', quotechar='|')
        for row in reader:
            heuristic_dlr[row[0]] = getDistanceFromLatLng(city_lat, city_lon, float(row[2]), float(row[3]))
    for city in graph:
        if city not in heuristic_dlr:
            heuristic_dlr[city] = 10000
    return heuristic_dlr



# for u,v,d in G.edges(data=True):
#     d['label'] = d.get('distance','')
# A=nx.nx_agraph.to_agraph(G)
# A.layout()
# A.draw('brasil1000.png')
start = 'Rio de Janeiro'
objective = 'Ourinhos'

heuristic = generate_heuristic_dlr_to(objective, G)
rio_to_ourinhos = Problem(start, [objective], G, heuristic)
rio_to_ourinhos.solve_with_a_star()
rio_to_ourinhos.solve_with_sma_star(100)