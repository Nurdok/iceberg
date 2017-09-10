"""Navigate a ship in the Northern Ocean with icebergs.

Usage:
    iceberg <input-file> <output-file>

"""


from networkx import Graph, shortest_path
from typing import List, Tuple, TextIO
from itertools import combinations
from sympy.geometry import Point2D, Polygon, Segment2D
from pathlib import Path
from docopt import docopt


def get_shortest_route(start: Point2D,
                       end: Point2D,
                       icebergs: List[Polygon]) -> List[Point2D]:
    """Calculate the best safe route from `start` to `end`.

    A safe route is one where you don't hit any icebergs.

    """
    # Create a graph where nodes are all the given points - source,
    # destination, and all points on all the icebergs.
    graph = Graph()
    graph.add_node(start)
    graph.add_node(end)
    for iceberg in icebergs:
        graph.add_nodes_from(iceberg.vertices)

    # For every two nodes on the graph (which are points on the map), we check
    # if the segment / route between them is blocked. If not, we add a graph
    # edge between them with the distance as weight.
    for u, v in combinations(graph.nodes(), r=2):
        segment = Segment2D(u, v)
        for iceberg in icebergs:
            # If we try to travel between adjacent points on an iceberg,
            # there can't be a collision.
            if segment in iceberg.sides:
                continue

            # Since icebergs are convex, any segment between two non-adjacent
            # points on the iceberg are blocked by the iceberg itself.
            if u in iceberg.vertices and v in iceberg.vertices:
                break

            # The intersection is a list of points and segments.
            intersection = segment.intersection(iceberg)
            if not intersection:
                continue

            # If the intersection is the source or the destination point,
            # then it's okay. It's also fine if we walk alongside the iceberg.
            if len(intersection) == 1 and (intersection[0] in (u, v) or
                                           intersection[0] in iceberg.sides):
                continue

            # In any other case, there's a bad collision.
            break
        else:
            graph.add_edge(u, v, {'distance': u.distance(v)})

    # Now that we have the graph with proper distances, we can use a shortest
    # path algorithm (e.g., Dijkstra) to find the shortest path.
    return shortest_path(graph, source=start, target=end, weight='distance')


def read_parameters(stream: TextIO) -> Tuple[Point2D, Point2D, List[Polygon]]:
    """Read lines from an input stream and return the problem parameters.

    The input should be in the following format:

    1. Integer with number of icebergs
    2. A set of 2D polygons representing icebergs boundaries, represented as
       a set of ordered coordinates. One line for an iceberg,
       the format: x1,y1 x2,y2 x3,y3.
    3. Position of Start point A in the format x,y.
    4. Position of End point B in the format x,y.

    """
    def readline():
        return stream.readline().strip()

    def point_from_str(point_str):
        x, y = point_str.split(',')
        return Point2D(int(x), int(y))

    iceberg_num = int(readline())
    icebergs: List[Polygon] = []
    for _ in range(iceberg_num):
        iceberg = Polygon(*[point_from_str(point_str)
                            for point_str in readline().split()])
        icebergs.append(iceberg)

    start = point_from_str(readline())
    end = point_from_str(readline())
    return start, end, icebergs


def write_solution(stream: TextIO, route: List[Point2D]) -> None:
    """Write the resulting route into the output stream.

    The output should be in the following format:

    1. An ordered list of co­ordinates which combine the selected path from
       A to B not crossing any iceberg. Including A and B.

    """
    stream.write(' '.join(f'{point.x},{point.y}' for point in route))


def solve_file(input_path: Path, output_path: Path) -> None:
    """Solve the shortest route problem from the input file.

    The solution is written to the output file.

    """
    with input_path.open('rt') as input_file:
        problem_parameters = read_parameters(input_file)  # type: ignore

    solution = get_shortest_route(*problem_parameters)

    with output_path.open('wt') as output_file:
        write_solution(output_file, solution)  # type: ignore


def _draw_graph(graph):
    """Draw a graph and save it to a file, for visualization and debugging."""
    import matplotlib.pyplot as plt
    import networkx as nx
    pos = {point: (point.x, point.y) for point in graph.nodes()}
    node_labels = {point: f'({point.x}, {point.y})' for point in graph.nodes()}
    edge_labels = {edge[:2]: edge[2]['distance']
                   for edge in graph.edges(data=True)}
    nx.draw_networkx(graph,
                     pos=pos,
                     labels=node_labels,
                     hold=True)
    print(edge_labels)
    nx.draw_networkx_edge_labels(graph,
                                 pos=pos,
                                 edge_labels=edge_labels,
                                 rotate=False)
    plt.savefig(r'graph.png')
    print(graph.edges())


def main():
    """Run the CLI."""
    args = docopt(__doc__)
    solve_file(Path(args['<input-file>']), Path(args['<output-file>']))


if __name__ == '__main__':
    main()
