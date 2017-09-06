from typing import List
from collections import namedtuple


Point = namedtuple('Point', 'x y')


def get_shortest_route(start: Point,
                       end: Point,
                       icebergs: List[List[Point]]) -> List[Point]:
    return [start, end]
