import pytest
from route_calc.map import Map
from route_calc.location import Location
from route_calc.simulation import simulate_traffic


def test_simulate_traffic():
    # Create an example map
    test_map = Map()
    A = Location(name="A", latitude=None, longitude=None)
    B = Location(name="B", latitude=None, longitude=None)
    C = Location(name="C", latitude=None, longitude=None)
    test_map.add_route(start=A, end=B, duration=5)
    test_map.add_route(start=A, end=C, duration=10.5)
    test_map.add_route(start=C, end=B, duration=50)

    # No traffic
    no_traffic = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=1,
        distribution=1,
        blockages=0,
    )
    assert test_map == no_traffic

    # No traffic
    no_traffic = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=100,
        distribution=0,
        blockages=0,
    )
    assert test_map == no_traffic

    # Has traffic but no blockages
    with_traffic_no_blockages = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=100,
        distribution=0.5,
        blockages=0,
    )
    assert test_map != with_traffic_no_blockages
    assert float("inf") not in sum(
        [list(r.values()) for r in with_traffic_no_blockages._adjacency_list.values()],
        [],
    )

    # Has traffic and route blockages
    with_traffic_and_blockages = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=100,
        distribution=0.5,
        blockages=1,
    )
    num_blockages = sum(
        [
            durr == float("inf")
            for durr in sum(
                [
                    list(r.values())
                    for r in with_traffic_and_blockages._adjacency_list.values()
                ],
                [],
            )
        ]
    )
    assert test_map != with_traffic_and_blockages
    assert num_blockages == 2

    # Check that AssertionErrors are raised appropriately
    with pytest.raises(AssertionError) as exception:
        simulate_traffic(
            map=test_map,
            min_delay=1,
            max_delay=100,
            distribution=-1,
            blockages=0,
        )
    assert (
        "Invalid distribution -1. Please use a number between 0 and 1, inclusive"
        == str(exception.value)
    )
    with pytest.raises(AssertionError) as exception:
        simulate_traffic(
            map=test_map,
            min_delay=1,
            max_delay=100,
            distribution=0,
            blockages=10,
        )
    assert (
        "Cannot have more blockages than allowed by the distribution. Maximum allowed blockages: 0"
        == str(exception.value)
    )
