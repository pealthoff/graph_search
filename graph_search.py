import heapq as hp
import networkx as nx
import pygraphviz as pgv
import math
from min_heap import MinHeap

MAX_ATTEMPTS = 100000

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
        openList = MinHeap([])
        entryFinder = {}
        initial_cost = self.heuristic[self.startingNode]
        openList.insert(initial_cost, [self.startingNode, []])
        entryFinder[self.startingNode] = 0
        closedList = []
        memory_spend=0

        for i in range(1, MAX_ATTEMPTS):
            if openList.heap_size is 0:
                raise Exception("Not found a solution")
            else:
                if openList.heap_size > memory_spend:
                    memory_spend = openList.heap_size
                p = openList.extract_min()
                cost_until_now = p[0]
                actual_city = p[1][0]
                if actual_city in entryFinder:
                    entryFinder.pop(actual_city)
                if actual_city in self.objectives:
                    finalPath = p[1][1]
                    finalPath.append(actual_city)
                    print(memory_spend)
                    print(finalPath)
                    print(cost_until_now)
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
                            openList.insert(cost, [adj_city, newPath])
                            entryFinder[adj_city] = cost
                        else:
                            if cost < entryFinder[adj_city]:
                                path = p[1][1]
                                newPath = list(path)
                                newPath.append(actual_city)
                                for i in range(1,openList.heap_size):
                                    if openList.heap[i][1][0] == adj_city:
                                        openList.heap[i][1][1] = newPath
                                        openList.decrease_priority(i, cost)
                                        entryFinder[adj_city] = cost
                                        break;
        raise Exception("Max attempts reached")

    def solve_with_sma_star(self, memory_max):
        path=[]
        openList = MinHeap([])
        entryFinder = {}
        initial_cost = self.heuristic[self.startingNode]
        openList.insert(initial_cost, [self.startingNode, [], initial_cost])
        entryFinder[self.startingNode] = 0
        closedList = []
        memory_spend = 0

        for i in range(1, MAX_ATTEMPTS):
            if openList.heap_size is 0:
                raise Exception("Not found a solution")
            else:
                if openList.heap_size > memory_spend:
                    memory_spend = openList.heap_size
                p = openList.extract_min()
                cost_until_now = p[1][2]
                actual_city = p[1][0]
                if actual_city in entryFinder:
                    entryFinder.pop(actual_city)
                if actual_city in self.objectives:
                    finalPath = p[1][1]
                    finalPath.append(actual_city)
                    print(memory_spend)
                    print(finalPath)
                    print(cost_until_now)
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
                            if openList.heap_size >= memory_max:
                                (max, maxEl) = openList.extract_max()
                                maxParent = openList.parent(max)
                                if openList.heap[maxParent][1][0] in closedList:
                                    closedList.remove(openList.heap[maxParent][1][0])
                                openList.heap[maxParent][0] = maxEl[0]
                                openList.heapify(maxParent)
                                # del entryFinder[maxEl[1][0]]
                            openList.insert(cost, [adj_city, newPath, cost])
                            entryFinder[adj_city] = cost
                        else:
                            if cost < entryFinder[adj_city]:
                                path = p[1][1]
                                newPath = list(path)
                                newPath.append(actual_city)
                                if openList.heap_size >= memory_max:
                                    (max, maxEl) = openList.extract_max()
                                    maxParent = openList.parent(max)
                                    if openList.heap[maxParent][1][0] in closedList:
                                        closedList.remove(openList.heap[maxParent][1][0])
                                    if openList.heap[max][1][0] in closedList:
                                        closedList.remove(openList.heap[max][1][0])
                                    openList.heap[maxParent][0] = maxEl[0]
                                    openList.heapify(maxParent)
                                openList.insert(cost, [adj_city, newPath, cost])
                                entryFinder[adj_city] = cost
                                for i in range(1,openList.heap_size):
                                    if openList.heap[i][1][0] == adj_city:
                                        openList.heap[i][1][1] = newPath
                                        openList.heap[i][1][2] = cost
                                        openList.decrease_priority(i, cost)
                                        entryFinder[adj_city] = cost
                                        break;
        raise Exception("Max attempts reached")