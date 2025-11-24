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
    test_map.add_route(start=A, end=B, duration=1)
    test_map.add_route(start=A, end=C, duration=1)
    test_map.add_route(start=C, end=B, duration=1)

    # No traffic
    no_traffic = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=1,
        risk=0,
        risk_count=3,
    )
    assert test_map == no_traffic

    # Has traffic but no extreme events
    with_traffic_no_blockages = simulate_traffic(
        map=test_map, min_delay=1, max_delay=3, risk=0
    )
    num_extreme_events = sum(
        [
            durr > 10
            for durr in sum(
                [
                    list(r.values())
                    for r in with_traffic_no_blockages._adjacency_list.values()
                ],
                [],
            )
        ]
    )
    assert test_map != with_traffic_no_blockages
    assert num_extreme_events == 0

    # Has traffic and extreme events
    with_traffic_and_blockages = simulate_traffic(
        map=test_map,
        min_delay=1,
        max_delay=3,
        risk=1,
        risk_count=3,
    )
    num_routes = len(
        sum(
            [
                list(r.values())
                for r in with_traffic_and_blockages._adjacency_list.values()
            ],
            [],
        )
    )
    num_extreme_events = sum(
        [
            durr > 10
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
    assert num_extreme_events == num_routes

    # Check that AssertionErrors are raised appropriately
    with pytest.raises(AssertionError) as exception:
        simulate_traffic(
            map=test_map,
            min_delay=1,
            max_delay=3,
            risk=-1,
            risk_count=3,
        )
    assert (
        "Invalid risk factor -1. Please use a number between 0 and 1, inclusive"
        == str(exception.value)
    )
