import pytest
from route_calc.map import Map
from route_calc.location import Location


def test_init():
    # Initialize Map object
    test_map = Map()

    # Check defaults
    assert test_map.time_units == "minutes"
    assert test_map.verbose is False
    assert test_map._adjacency_list == {}

    # Initialize Map object
    test_map = Map(time_units="seconds", verbose=True)

    # Check defaults
    assert test_map.time_units == "seconds"
    assert test_map.verbose is True
    assert test_map._adjacency_list == {}


def test_eq():
    original_map = Map()
    another_map = Map()

    A = Location(name="A", latitude=None, longitude=None)
    B = Location(name="B", latitude=None, longitude=None)
    C = Location(name="C", latitude=None, longitude=None)

    original_map.add_route(start=A, end=B, duration=5)
    original_map.add_route(start=A, end=C, duration=10.5)
    original_map.add_route(start=C, end=B, duration=50)

    assert original_map != another_map
    another_map.add_route(start=C, end=B, duration=50)
    assert original_map != another_map
    another_map.add_route(start=A, end=C, duration=10.5)
    assert original_map != another_map
    another_map.add_route(start=A, end=B, duration=5)
    assert original_map == another_map

    # Check that TypeErrors are raised appropriately
    with pytest.raises(TypeError) as exception:
        original_map == 0
    assert f"Cannot establish equality between Map and {int} objects" == str(
        exception.value
    )


def test_add_route():
    # Initialize Map object
    test_map = Map()

    # Create some Location objects
    loc1 = Location(
        name="Location 1",
        latitude=1,
        longitude=1,
    )
    loc2 = Location(
        name="Location 2",
        latitude=2,
        longitude=2,
    )
    loc3 = Location(
        name="Location 3",
        latitude=3,
        longitude=3,
    )
    test_map.add_route(start=loc1, end=loc2, duration=5)
    test_map.add_route(start=loc1, end=loc3, duration=10.5)
    test_map.add_route(start=loc3, end=loc2, duration=50)

    assert test_map._adjacency_list == {
        loc1: {
            loc2: 5,
            loc3: 10.5,
        },
        loc2: {
            loc1: 5,
            loc3: 50,
        },
        loc3: {
            loc1: 10.5,
            loc2: 50,
        },
    }


def test_calculate_duration():
    # Initialize Map object
    test_map = Map()

    # Create some Location objects
    loc0 = Location(
        name="0",
        latitude=0,
        longitude=0,
    )
    loc1 = Location(
        name="1",
        latitude=1,
        longitude=1,
    )
    loc2 = Location(
        name="2",
        latitude=2,
        longitude=2,
    )
    loc3 = Location(
        name="3",
        latitude=3,
        longitude=3,
    )
    loc4 = Location(
        name="4",
        latitude=4,
        longitude=4,
    )
    test_map.add_route(start=loc0, end=loc1, duration=4)
    test_map.add_route(start=loc0, end=loc2, duration=8)
    test_map.add_route(start=loc1, end=loc2, duration=3)
    test_map.add_route(start=loc1, end=loc4, duration=6)
    test_map.add_route(start=loc2, end=loc3, duration=2)
    test_map.add_route(start=loc3, end=loc4, duration=10)

    # Different types are valid
    assert test_map.calculate_duration(loc0, loc2) == 7
    assert test_map.calculate_duration("0", "2") == 7

    # Check shortest path is calculated correctly
    assert test_map.calculate_duration("0", "1") == 4
    assert test_map.calculate_duration("0", "2") == 7
    assert test_map.calculate_duration("0", "3") == 9
    assert test_map.calculate_duration("0", "4") == 10


def test_construct_path():
    # Initialize Map object
    test_map = Map()

    # Create some Location objects
    loc0 = Location(
        name="0",
        latitude=0,
        longitude=0,
    )
    loc1 = Location(
        name="1",
        latitude=1,
        longitude=1,
    )
    loc2 = Location(
        name="2",
        latitude=2,
        longitude=2,
    )
    loc3 = Location(
        name="3",
        latitude=3,
        longitude=3,
    )
    loc4 = Location(
        name="4",
        latitude=4,
        longitude=4,
    )
    test_map.add_route(start=loc0, end=loc1, duration=4)
    test_map.add_route(start=loc0, end=loc2, duration=8)
    test_map.add_route(start=loc1, end=loc2, duration=3)
    test_map.add_route(start=loc1, end=loc4, duration=6)
    test_map.add_route(start=loc2, end=loc3, duration=2)
    test_map.add_route(start=loc3, end=loc4, duration=10)

    # Check shortest path is calculated correctly
    assert test_map.construct_path(loc0, loc1) == [loc0, loc1]
    assert test_map.construct_path(loc0, loc2) == [loc0, loc1, loc2]
    assert test_map.construct_path(loc0, loc3) == [loc0, loc1, loc2, loc3]
    assert test_map.construct_path(loc0, loc4) == [loc0, loc1, loc4]
