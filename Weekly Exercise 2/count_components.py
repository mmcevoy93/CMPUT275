''''

    test cases:
    >>> from graph import Graph
    >>> from count_components import count_components
    >>> g = Graph()
    >>> vertices = {1, 2, 3, 4, 5, 6}
    >>> edges = [(1, 2), (3, 4), (3, 5), (4, 5)]
    >>> for v in vertices: g.add_vertex(v)
    >>> for e in edges: g.add_edge( (e[0], e[1]) )
    >>> for e in edges: g.add_edge( (e[1], e[0]) )
    >>> count_components(g)
    3
    >>> g.add_edge( (1, 4) )
    >>> g.add_edge( (4, 1) )
    >>> count_components(g)
    2

'''
from graph import Graph
from breadth_first_search import breadth_first_search
from breadth_first_search import get_path

g1 = Graph({"A", "B", "C", "D"}, [("A", "B"), ("B", "D"),
                                  ("C", "B"), ("C", "D")])
print(breadth_first_search(g1, "A"))
vertices_check = g1.get_vertices()
print(vertices_check)

'''
if __name__ == "__main__":
  import doctest
  doctest.testmod()
'''
