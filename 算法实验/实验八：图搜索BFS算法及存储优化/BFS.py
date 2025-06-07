import time
# Adjacent list representation of a graph
class ADJList:
    def __init__(self):
    # initialize an empty dictionary; the key is the vertex and the value is the list of adjacent vertices
        self.graph = {}
    
    def addEdge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    
    def BFS(self, s, print_vertices = True):
        # from the source s
        visited = {vertex:False for vertex in self.graph.keys()}
        # use a queue to store the vertices to traverse in the breadth-first manner
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            s = queue.pop(0)
            if print_vertices:
                print(s, end = " ")
            for i in self.graph[s]:
                try:
                    if visited[i] == False:
                        queue.append(i)
                        visited[i] = True
                except:
                    pass

# Adjacency Matrix representation of a graph
class ADJMatrix:
    def __init__(self, n):
    # the input is the number of vertices in the graph
        self.graph = [[0 for i in range(n)] for j in range(n)]
        self.vertices_to_integer = {}
        self.integer_to_vertices = {}
    
    def addEdge(self, u, v):
        self.graph[u][v] = 1
    
    def BFS(self, s):
        visited = [False] * len(self.graph)
        queue = []
        queue.append(s)
        visited[s] = True
        while queue:
            s = queue.pop(0)
            print(self.integer_to_vertices[s], end = " ")
            for i in range(len(self.graph[s])):
                if self.graph[s][i] == 1 and visited[i] == False:
                    queue.append(i)
                    visited[i] = True

with open('data.txt', 'r') as f:
    vertices = f.readline().strip().split(',')
    vertices_to_integer = {vertices:i for i, vertices in enumerate(vertices)}
    integer_to_vertices = {i:vertices for i, vertices in enumerate(vertices)}
    edges = f.readlines()
    # Because the graph is edge-intense, we use the adjacency list representation
    graph_ADJMatrix = ADJMatrix(len(vertices))
    graph_ADJMatrix.vertices_to_integer = vertices_to_integer
    graph_ADJMatrix.integer_to_vertices = integer_to_vertices
    for edge in edges:
        u, v = edge.strip().split('-')
        graph_ADJMatrix.addEdge(vertices_to_integer[u], vertices_to_integer[v])

graph_ADJMatrix.BFS(vertices_to_integer['A'])

# twitter_small, Nodes 81306, Edges 1768149, edge density 0.000043
with open('twitter_small.txt', 'r') as f:
    edges = f.readlines()
    graph_twitter_small = ADJList()
    for edge in edges:
        u, v = edge.strip().split()
        graph_twitter_small.addEdge(int(u), int(v))

time_start = time.time()
graph_twitter_small.BFS(list(graph_twitter_small.graph.keys())[0], print_vertices = False)
time_end = time.time()
print("\nTime used for BFS on twitter_small: ", time_end - time_start)
