from graph import Graph,  Vertex

g = Graph()
g.add_vertex(1)
g.add_vertex(2)
g.add_vertex(3)
g.add_vertex(4)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(1, 3)
g.remove_vertex(1)
g.show_graph()
if g.is_cyclic()[0]:
    print("graf jest cykliczny")
    print(g.is_cyclic()[1])
else:
    print("graf nie jest cykliczny")