import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self, num_of_nodes):
        self.m_v = num_of_nodes
        self.m_edges = []
        self.m_component = {}
    
    def add_edge(self, u, v, weight):
        self.m_edges.append([u, v, weight])
    
    def find_component(self, u):
        if self.m_component[u] == u:
            return u
        return self.find_component(self.m_component[u])
    
    def set_component(self, u):
        if self.m_component[u] == u:
            return
        else:
            for k in self.m_component.keys():
                self.m_component[k] = self.find_component(k)
    
    def union(self, component_size, u, v):
        if component_size[u] <= component_size[v]:
            self.m_component[u] = v
            component_size[v] += component_size[u]
            self.set_component(u)
        
        elif component_size[u] >= component_size[v]:
            self.m_component[v] = self.find_component(u)
            component_size[u] += component_size[v]
            self.set_component(v)
        
        print(self.m_component)
    
    def boruvka_minimum(self):
        res_dict = {}
        component_size = []
        mst_weight = 0
        
        minimum_weight_edge = [-1] * self.m_v
        
        for node in range(self.m_v):
            self.m_component.update({node: node})
            component_size.append(1)
        
        num_of_components = self.m_v
        
        print("---------Forming MST(minimum)------------")
        while num_of_components > 1:
            for i in range(len(self.m_edges)):
                
                u = self.m_edges[i][0]
                v = self.m_edges[i][1]
                w = self.m_edges[i][2]
                
                u_component = self.m_component[u]
                v_component = self.m_component[v]
                
                if u_component != v_component:
                    if minimum_weight_edge[u_component] == -1 or \
                            minimum_weight_edge[u_component][2] > w:
                        minimum_weight_edge[u_component] = [u, v, w]
                    if minimum_weight_edge[v_component] == -1 or \
                            minimum_weight_edge[v_component][2] > w:
                        minimum_weight_edge[v_component] = [u, v, w]
            
            for node in range(self.m_v):
                if minimum_weight_edge[node] != -1:
                    u = minimum_weight_edge[node][0]
                    v = minimum_weight_edge[node][1]
                    w = minimum_weight_edge[node][2]
                    
                    u_component = self.m_component[u]
                    v_component = self.m_component[v]
                    
                    if u_component != v_component:
                        mst_weight += w
                        self.union(component_size, u_component, v_component)
                        res_dict[u, v] = w
                        print("Added edge [" + str(u) + " - "
                              + str(v) + "]\n"
                              + "Added weight: " + str(w) + "\n")
                        num_of_components -= 1
            
            minimum_weight_edge = [-1] * self.m_v
        print("----------------------------------")
        print("The total weight of the minimal spanning tree is: " + str(mst_weight))
        print(f"Res dict is {res_dict}")
        return res_dict, mst_weight
    
    def boruvka_maximum(self):
        res_dict = {}
        component_size = []
        mst_weight = 0
        
        maximum_weight_edge = [1] * self.m_v
        
        for node in range(self.m_v):
            self.m_component.update({node: node})
            component_size.append(1)
        
        num_of_components = self.m_v
        
        print("---------Forming MST(maximum)------------")
        while num_of_components > 1:
            for i in range(len(self.m_edges)):
                
                u = self.m_edges[i][0]
                v = self.m_edges[i][1]
                w = self.m_edges[i][2]
                
                u_component = self.m_component[u]
                v_component = self.m_component[v]
                
                if u_component != v_component:
                    if maximum_weight_edge[u_component] == 1 or \
                            maximum_weight_edge[u_component][2] < w:
                        maximum_weight_edge[u_component] = [u, v, w]
                    if maximum_weight_edge[v_component] == 1 or \
                            maximum_weight_edge[v_component][2] < w:
                        maximum_weight_edge[v_component] = [u, v, w]
            
            for node in range(self.m_v):
                if maximum_weight_edge[node] != 1:
                    u = maximum_weight_edge[node][0]
                    v = maximum_weight_edge[node][1]
                    w = maximum_weight_edge[node][2]
                    
                    u_component = self.m_component[u]
                    v_component = self.m_component[v]
                    
                    if u_component != v_component:
                        mst_weight += w
                        self.union(component_size, u_component, v_component)
                        res_dict[u, v] = w
                        print("Added edge [" + str(u) + " - "
                              + str(v) + "]\n"
                              + "Added weight: " + str(w) + "\n")
                        num_of_components -= 1
            
            maximum_weight_edge = [1] * self.m_v
        print("----------------------------------")
        print("The total weight of the maxinum spanning tree is: " + str(mst_weight))
        print(f"Res dict is {res_dict}")
        return res_dict, mst_weight
    
    def draw_graph(self, res_dict, mst_weight, option):
        print(f'm_edges is {self.m_edges}')
        
        G = nx.Graph()
        for record in self.m_edges:
            G.add_edge(record[0], record[1], weight=record[2])
        
        edges = list(G.edges)
        
        for edge in edges:
            if edge in res_dict.keys() or (edge[1], edge[0]) in res_dict.keys():
                if option == 'maximum':
                    nx.set_edge_attributes(G, {edge: {'color': 'r'}})
                else:
                    nx.set_edge_attributes(G, {edge: {'color': 'g'}})
            else:
                nx.set_edge_attributes(G, {edge: {'color': 'b'}})
        pos = nx.circular_layout(G)
        colors = nx.get_edge_attributes(G, 'color').values()
        nx.draw_networkx(G, pos, edge_color=colors, with_labels=True, width=2)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        plt.title(f'Visualisation of {option} spanning tree')
        if option == 'maximum':
            l1 = plt.plot(1, 1, color='red')
        else:
            l1 = plt.plot(1, 1, color='green')
        l2 = plt.plot(1, 1, color='blue')
        plt.legend([l1, l2], labels=['MST', 'Graph edges'])
        plt.text(-1.1, -1.1, f'Total weight is {mst_weight}', fontsize=12)
        plt.savefig(f"{option}.png", format="PNG")
        plt.show()


with open('l1_2.txt') as f:
    output = f.readlines()

matrix = []
for element in output:
    matrix.append(element.split())
print(matrix)
g = Graph(8)
for vertex1, vertex_list1 in enumerate(matrix):
    for vertex2, weight in enumerate(vertex_list1):
        if int(weight) == 0:
            continue
        else:
            g.add_edge(vertex1, vertex2, int(weight))

res1, mst_weight1 = g.boruvka_minimum()
g.draw_graph(res1, mst_weight1, 'minimum')

res2, mst_weight2 = g.boruvka_maximum()
g.draw_graph(res2, mst_weight2, 'maximum')
