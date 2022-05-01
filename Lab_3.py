import math
import networkx as nx
import matplotlib.pyplot as plt

maxsize = float('inf')


def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]


def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
    return min


def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        
        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]
    
    return second


def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res
    
    if level == N:
        
        if adj[curr_path[level - 1]][curr_path[0]] != 0:
            
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return
    
    for i in range(N):
        
        if (adj[curr_path[level - 1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]
            
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True
                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)
            
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp
            
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def TSP(adj):
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N
    
    for i in range(N):
        curr_bound += (firstMin(adj, i) +
                       secondMin(adj, i))
    
    curr_bound = math.ceil(curr_bound / 2)
    
    visited[0] = True
    curr_path[0] = 0
    
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


with open('l3-1.txt') as f:
    output = f.readlines()

matrix = []
for element in output:
    matrix.append([int(x) for x in element.split()])
adj = matrix

N = len(matrix)
final_path = [None] * (N + 1)

visited = [False] * N

final_res = maxsize

TSP(adj)

print("Minimum cost :", final_res)
print("List of vertexes : ", end=' ')
result = []
for i in range(N + 1):
    result.append(final_path[i])
print(result)

G = nx.Graph()
for vertex1, vertex_list1 in enumerate(matrix):
    for vertex2, weight in enumerate(vertex_list1):
        if int(weight) == 0:
            continue
        else:
            G.add_edge(vertex1, vertex2, weight=int(weight))
edges = list(G.edges)
result_edges = []
for i in range(len(result) - 1):
    if (result[i], result[i + 1]) in edges:
        result_edges.append((result[i], result[i + 1]))
    elif (result[i + 1], result[i]) in edges:
        result_edges.append((result[i + 1], result[i]))

for edge in edges:
    if edge in result_edges:
        nx.set_edge_attributes(G, {edge: {'color': 'g'}})
    else:
        nx.set_edge_attributes(G, {edge: {'color': 'b'}})
pos = nx.planar_layout(G)
colors = nx.get_edge_attributes(G, 'color').values()
nx.draw_networkx(G, pos, edge_color=colors, with_labels=True, width=2)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title(f'Visualisation of Hamilton сycle')
plt.text(-0.5, -0.5, f'Minimum cost is {final_res}', fontsize=12)

plt.show()
