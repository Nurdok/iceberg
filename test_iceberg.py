"""Test for the iceberg module."""


from iceberg import (
    get_shortest_route,
    Point2D,
    Polygon,
    read_parameters,
    write_solution,
)

from io import StringIO
import textwrap


def test_no_icebergs():
    """Test that with no icebergs, a direct route is taken."""
    start = Point2D(4, 4)
    end = Point2D(12, 80)
    icebergs = ()
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        Point2D(4, 4),
        Point2D(12, 80),
    ]


def test_irrelevant_icebergs():
    """Test that if the direct route is not interrupted, it is used."""
    start = Point2D(4, 4)
    end = Point2D(12, 80)
    icebergs = (
        Polygon(Point2D(0, 0), Point2D(1, 1), Point2D(0, 2)),
        Polygon(Point2D(11, 20), Point2D(15, 50), Point2D(15, 20)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        Point2D(4, 4),
        Point2D(12, 80),
    ]


def test_route_on_iceberg_side():
    """Test when the shortest route goes alongside an iceberg."""
    start = Point2D(4, 4)
    end = Point2D(12, 80)

    icebergs = (
        Polygon(Point2D(4, 7), Point2D(4, 8), Point2D(100, 8),
                Point2D(100, 7)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        Point2D(4, 4),
        Point2D(4, 8),
        Point2D(12, 80),
    ]


def test_route_on_iceberg_point():
    """Test when the shortest route touches one point of an iceberg."""
    start = Point2D(0, 0)
    end = Point2D(5, 5)

    icebergs = (
        Polygon(Point2D(1, 2), Point2D(1, 3), Point2D(5, 2)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        Point2D(0, 0),
        Point2D(1, 3),
        Point2D(5, 5),
    ]


def test_complex_route():
    start = Point2D(5, 0)
    end = Point2D(5, 5)

    icebergs = (
        Polygon(Point2D(4, 1), Point2D(8, 1), Point2D(8, 2), Point2D(4, 2)),
        Polygon(Point2D(6, 3), Point2D(6, 4), Point2D(2, 4), Point2D(2, 3)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        Point2D(5, 0),
        Point2D(4, 1),
        Point2D(4, 2),
        Point2D(6, 3),
        Point2D(6, 4),
        Point2D(5, 5),
    ]


def test_input_parsing():
    input_stream = StringIO(textwrap.dedent("""\
        2
        1,2 1,3 5,2
        10,20 10,30 50,20
        0,0
        100,100
    """))

    start = Point2D(0, 0)
    end = Point2D(100, 100)
    icebergs = [
        Polygon(Point2D(1, 2), Point2D(1, 3), Point2D(5, 2)),
        Polygon(Point2D(10, 20), Point2D(10, 30), Point2D(50, 20)),
    ]

    assert read_parameters(input_stream) == (start, end, icebergs)


def test_output_writing():
    output_stream = StringIO()
    route = (Point2D(1, 2), Point2D(1, 3), Point2D(5, 2))
    write_solution(output_stream, route)

    assert output_stream.getvalue() == '1,2 1,3 5,2'
