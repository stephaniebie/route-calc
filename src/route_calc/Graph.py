import heapq
import random

class Graph:
    def __init__(self, scenario="Base"):
        self.adjacency_list = {}
        self.scenario = scenario
        
    def add_edge(self, u, v, weight=1, risk=False):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        if self.scenario == "Rush Hour":
            rval = random.gauss(2, 0.5)
            rval = max(1, rval) # ensure min is 1 
            rval = min(3, rval) # ensure max is 3
            weight = int(weight * rval)
        if risk and random.random() < 0.2:
            print("Accident on edge", u, v)
            weight *= 15
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))
    
    def load_edges_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            next(file)  
            for line in file:
                u, v, weight = line.strip().split(',')
                self.add_edge(u, v, int(weight))
    
    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.adjacency_list}
        distances[start] = 0
        prev = {node: None for node in self.adjacency_list}
        visited = set()
        pq = [(0, start)]
        
        while pq:
            curr_time, curr_node = heapq.heappop(pq)
            
            if curr_node in visited:
                continue
            visited.add(curr_node)
            
            if curr_node == end:
                return self.reconstruct_path(start, end, prev), curr_time
            
            for neighbor, weight in self.adjacency_list[curr_node]:
                if neighbor in visited:
                    continue
                total_time = curr_time + weight
                if total_time < distances[neighbor]:
                    distances[neighbor] = total_time
                    prev[neighbor] = curr_node
                    heapq.heappush(pq, (total_time, neighbor))
        
                    
    def reconstruct_path(self, start, end, prev):
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
        return path
            
    
    def __repr__(self):
        return f"Graph with {len(self.adjacency_list)} nodes\n Adjacency List: {self.adjacency_list}"
    
    def __str__(self):
        return self.__repr__()
    