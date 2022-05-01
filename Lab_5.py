from pprint import pprint

import networkx as nx


def read_matrix(file):
    with open(file) as f:
        output = f.readlines()
    matrix = []
    for element in output:
        matrix.append(element.split())
    return matrix


def get_number_of_edges(degree_list):
    res = []
    for i in degree_list:
        res.append(i[1])
    return sorted(res)


def check_isomophism(G1, G2):
    if len(G1.edges) == len(G2.edges) and len(G1.nodes) == len(G2.nodes):
        if get_number_of_edges(G1.degree) == get_number_of_edges(G2.degree):
            pass
            return 'Graphs are isomorphic'
        return 'Graphs aren\'t isomorphic'
    return 'Graphs aren\'t isomorphic'


def main():
    matrix1 = read_matrix('l1_1.txt')
    matrix2 = read_matrix('l1_2.txt')
    print('Graph1 is:')
    pprint(matrix1)
    print('Graph2 is:')
    pprint(matrix2)
    G1 = nx.Graph()
    for vertex1, vertex_list1 in enumerate(matrix1):
        for vertex2, weight in enumerate(vertex_list1):
            if int(weight) == 0:
                continue
            else:
                G1.add_edge(vertex1, vertex2, weight=int(weight))
    
    G2 = nx.Graph()
    for vertex1, vertex_list1 in enumerate(matrix2):
        for vertex2, weight in enumerate(vertex_list1):
            if int(weight) == 0:
                continue
            else:
                G2.add_edge(vertex1, vertex2, weight=int(weight))
    
    print(G1.degree)
    print(G2.degree)
    print(f'Result of built-in function "is_isomprophic": {nx.is_isomorphic(G1, G2)}')
    print(f'Result of my function is: {check_isomophism(G1, G2)}')


main()
