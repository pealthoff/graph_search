import heapq as hp
import networkx as nx
import pygraphviz as pgv

MAX_ATTEMPTS = 100

class Problem:
    def __init__(self, start, objectives, graph, heuristic):
        self.objectives = objectives
        self.graph = graph
        self.startingNode = start
        self.heuristic = heuristic

    def __str__(self):
        return "Graph: {g} \n Starting node: {sn} \n Objectives {ob}".format(g=self.graph, sn=self.startingNode, ob=self.objectives)

    def solve_with_a_star(self):
        path=[]
        openList = []
        entryFinder = {}
        hp.heappush(openList, (self.heuristic[self.startingNode], [self.startingNode, []]))
        entryFinder[self.startingNode] = 0
        closedList = []

        for i in range(1, MAX_ATTEMPTS):
            if len(openList) is 0:
                raise Exception("Not found a solution")
            else:
                p = hp.heappop(openList)
                cost_until_now = p[0]
                actual_city = p[1][0]
                entryFinder.pop(actual_city)
                if actual_city in self.objectives:
                    finalPath = p[1][1]
                    finalPath.append(actual_city)
                    print(finalPath)
                    return
                adj_cities = self.graph[actual_city]
                closedList.append(actual_city)
                for adj_city in adj_cities:
                    if adj_city not in closedList:
                        gx = (cost_until_now - self.heuristic[actual_city]) + adj_cities[adj_city]['distance']
                        cost = gx + self.heuristic[adj_city]
                        if adj_city not in entryFinder:
                            path = p[1][1]
                            newPath = list(path)
                            newPath.append(actual_city)
                            hp.heappush(openList, (cost, [adj_city, newPath]))
                            entryFinder[adj_city] = cost
                        else:
                            if cost < entryFinder[adj_city]:
                                path = p[1][1]
                                newPath = list(path)
                                newPath.append(actual_city)
                                hp.heappush(openList, (cost, [adj_city, newPath]))
                                #the best here is to remove the higher cost
                                #but the heapq impl don't make this easy
                                #in future replace heapq by a min_heap impl