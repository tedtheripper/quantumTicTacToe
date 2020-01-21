from src.vertex import Vertex


def test_adding_neighbour():
    v = Vertex(1, 1)
    v.add_neighbour(2)
    v.add_neighbour(3)
    assert len(v.get_neighbours()) == 2
    assert v.get_neighbours()[0] == 2
    assert v.get_neighbours()[1] == 3


def test_removing_neighbour():
    v = Vertex(1, 1)
    v.add_neighbour(2)
    v.add_neighbour(3)
    v.remove_neighbour(2)
    assert 2 not in v.get_neighbours()


def test_cleaning_neighbours():
    v = Vertex(1, 1)
    v.add_neighbour(2)
    v.add_neighbour(3)
    v.clean_neighbours()
    assert len(v.get_neighbours()) == 0


def test_color():
    v = Vertex(1, 1)
    v.set_color("Blue")
    assert v.get_color() == "Blue"


def test_index():
    v = Vertex(1, 1)
    assert v.get_index() == 1
    v.set_index(5)
    assert v.get_index() == 5


def test_mutability():
    v = Vertex(1, 1)
    assert not v.get_is_untouchable()
    v.set_is_untouchable()
    assert v.get_is_untouchable()
