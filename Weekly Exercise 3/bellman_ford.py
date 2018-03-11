def bellman_ford(vertices, edges, start):
    '''
    Computes shortest paths to every reachable vertex from the vertex "start"
    in the given directed graph.

    vertices: the set of vertices in the graph.
    edges: maps pairs of vertices to values representing edge costs
       example - {('A', 'B'): -3} means the edge from vertex
                 'A' to vertex 'B' has cost -3
    start: the start vertex to search from

    Assumes the graph does not have negative cost cycles,
    that all edges have endpoints in "vertices", and that
    "start" is also in "vertices".

    returns dist, reached

    Here reached is the search tree to all reachable vertices along
    minimum-cost paths and dist[v] is the cost to v along
    this path. If v is not reachable, it should not be in the
    search tree nor an index in dist.

    >>> vertices = {1, 2, 3, 4, 5, 6}
    >>> edges = {(1,2):5, (2,5):-7, (3,2):2, (4,1):-2, (5,1):3, (5,3):6, (5,4):4, (6,3):2, (6,5):-10}
    >>> dist, reached = bellman_ford(vertices, edges, 1)
    >>> print(dist)
    {1: 0, 2: 5, 3: 4, 4: 2, 5: -2}
    >>> print(reached)
    {1: 1, 2: 1, 3: 5, 4: 5, 5: 2}
    '''

    reached = {start: start}

    dist = {}
    dist[start] = 0
    for v in vertices:
        if v == start:
            continue
        dist[v] = float('inf')

    for v in vertices:
        for e in edges:
            if dist[e[1]] > dist[e[0]] + edges[e]:
                dist[e[1]] = dist[e[0]] + edges[e]
                reached[e[1]] = e[0]
    # take out nonreacheable nodes. Hope this doesn't affect time
    dist = {k: v for k, v in dist.items() if v != float('inf')}
    return dist, reached


def find_potential(vertices, edges):
    """
    Finds a potential for the graph or determines the graph has
    a negative-cost cycle.

    vertices: the set of vertices in the graph.
    edges: maps pairs of vertices to values representing edge costs
    example - {('A', 'B'): -3}Uploading, please wait... means the edge from
            vertex 'A' to vertex 'B' has cost -3
    start: the start vertex to search from

    If the graph has a negative-cost cycle, this simply returns None.
    Otherwise, it returns a dictionary mapping each vertex to its value
    in a potential function.

    >>> vertices = {1, 2, 3, 4, 5, 6}
    >>> edges = {(1,2):5, (2,5):-7, (3,2):2, (4,1):-2, (5,1):3, (5,3):6, (5,4):4, (6,3):2, (6,5):-10}
    >>> dist, reached = bellman_ford(vertices, edges, 1)
    >>> print(dist)
    {1: 0, 2: 5, 3: 4, 4: 2, 5: -2}
    >>> print(reached)
    {1: 1, 2: 1, 3: 5, 4: 5, 5: 2}
    >>> print(find_potential(vertices, edges))
    {1: 8, 2: 3, 3: 4, 4: 6, 5: 10, 6: 0}
    >>> edges[(5, 4)] = 3   # creates a negative-cost cycle
    >>> print(find_potential(vertices, edges))
    None
    """
    poten = {}

    for v in vertices:
        poten[v] = 0

    for v in vertices:
        for e in edges:
            if poten[e[1]] > poten[e[0]] + edges[e]:
                poten[e[1]] = poten[e[0]] + edges[e]
    for e in edges:
        if poten[e[1]] > poten[e[0]] + edges[e]:
            return "None"

    # had the right values but they were negative
    for p in poten:
        poten[p] = abs(poten[p])
    return poten


if __name__ == "__main___":
    import doctest
    doctest.testmod()
