"""Test for the iceberg module."""


from iceberg import get_shortest_route


def test_no_icebergs():
    """Test that with no icebergs, a direct route is taken."""
    start = (4, 4)
    end = (12, 80)
    icebergs = ()
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        (4, 4),
        (12, 80),
    ]


def test_irrelevant_icebergs():
    """Test that if the direct route is not interrupted, it is used."""
    start = (4, 4)
    end = (12, 80)
    icebergs = (
        ((0, 0), (1, 1), (0, 2)),
        ((11, 20), (15, 50), (15, 20)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        (4, 4),
        (12, 80),
    ]


def test_shortest_route():
    """Test that the correct path is taken."""
    start = (4, 4)
    end = (12, 80)
    icebergs = (
        ((4, 7), (4, 8), (100, 8), (100, 7)),
    )
    assert get_shortest_route(start=start, end=end, icebergs=icebergs) == [
        (4, 4),
        (4, 8),
        (12, 80),
    ]

