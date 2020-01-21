from graph import Graph, BadArgumentError
import pytest


def test_inittialization():
    g = Graph()
    assert g.vertices is not None


def test_adding_vertex():
    g = Graph()
    g.add_vertex(1, 1)
    assert 1 in g.vertices.keys()
    with pytest.raises(BadArgumentError):
        g.add_vertex(-2, 50)


def test_removing_vertex():
    g = Graph()
    g.add_vertex(1, 1)
    test_adding_vertex()
    g.remove_vertex(1)
    assert 1 not in g.vertices.keys()
    with pytest.raises(BadArgumentError):
        g.remove_vertex(90)


def test_adding_edge():
    g = Graph()
    g.add_vertex(1, 1)
    g.add_vertex(2, 2)
    g.add_edge(1, 2)
    assert 1 in g.vertices[2].get_neighbours()
    assert 2 in g.vertices[1].get_neighbours()
    with pytest.raises(BadArgumentError):
        g.add_edge(1, 50)


def test_vertex_exists():
    g = Graph()
    g.add_vertex(1, 1)
    assert g.vertex_exist(1)
    assert not g.vertex_exist(50)


def test_get_neighbours():
    g = Graph()
    g.add_vertex(1, 1)
    g.add_vertex(2, 2)
    assert 2 not in g.get_neighbours(1)
    g.add_edge(1, 2)
    assert 2 in g.get_neighbours(1)
    with pytest.raises(BadArgumentError):
        g.get_neighbours(50)


def test_get_square_index():
    g = Graph()
    g.add_vertex(1, 1)
    assert g.get_square_index(1) == 1
    with pytest.raises(BadArgumentError):
        g.get_square_index(20)


def test_get_all_vertices_in_given_square():
    g = Graph()
    g.add_vertex(1, 1)
    g.add_vertex(2, 1)
    assert 1 in g.get_all_vertices_in_given_square(1)
    assert 2 not in g.get_all_vertices_in_given_square(2)
    with pytest.raises(BadArgumentError):
        g.get_all_vertices_in_given_square(50)


def test_is_cyclic():
    g = Graph()
    g.add_vertex(1, 1)
    g.add_vertex(2, 2)
    g.add_edge(1, 2)
    assert not g.is_cyclic()[0]
    g.add_vertex(3, 2)
    g.add_vertex(4, 1)
    g.add_edge(3, 4)
    g.add_edge(1, 4)
    g.add_edge(2, 3)
    assert g.is_cyclic()[0]
