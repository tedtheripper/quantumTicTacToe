from graph import Vertex, Graph
g = Graph()
g.add_vertex(1)
g.add_vertex(2)
g.add_edge(1, 2)
g.add_vertex(3)
g.add_edge(2, 3)
g.add_edge(3, 1)
g.show_graph()

if g.is_cyclic():
    print("CYCEK!")
else:
    print("Chuj")