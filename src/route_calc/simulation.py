from random import normalvariate, shuffle
from route_calc.map import Map


def simulate_traffic(
    map: Map,
    min_delay: float = 1.0,
    max_delay: float = 1.0,
    distribution: float = 1.0,
    blockages: int = 0,
) -> Map:
    """
    Simulate traffic for each route in the map, normally distributed.
    NOTE: Assumes traffic is the same in both directions!

    Parameters
    ----------
    min_delay: float
        The minimum number by which to scale the amount of random traffic throughout the map routes
    max_delay: float
        The maximum number by which to scale the amount of random traffic throughout the map routes
    distribution: float
        Determines the amount by which to distribute the delay through out the map. Must be within range [0, 1]:
            0 = no routes are delayed
            1 = all routes are delayed
    blockages: int
        Adds a number of route blockages to the map. A blockage is defined to be a route of infinite duration

    Returns
    -------
    A new Map object with modified durations
    """
    # Assert distribution be bounded between 0 and 1, inclusive
    assert (
        distribution <= 1 and distribution >= 0
    ), f"Invalid distribution {distribution}. Please use a number between 0 and 1, inclusive"

    # Calculate mean and standard deviation for 99.7% containment
    mean = (min_delay + max_delay) / 2
    stdev = (max_delay - min_delay) / 6

    # Get the number of routes and affected routes (for discrete distribution)
    # NOTE: Calculation only true because we're assuming duration is the same in both directions!!
    number_of_routes = int(
        sum([len(r.values()) for r in map._adjacency_list.values()]) / 2
    )
    affected_routes = int(number_of_routes * distribution)

    # Assert that you cannot have more blockages than affected routes
    assert (
        blockages <= affected_routes
    ), f"Cannot have more blockages than allowed by the distribution. Maximum allowed blockages: {affected_routes}"

    # Non-affected routes experience no delays
    multipliers = [1] * (number_of_routes - affected_routes) + [
        float("inf")
    ] * blockages

    # Generate a randomized set of multipliers
    for _ in range(affected_routes - blockages):
        random_scalar = normalvariate(mean, stdev)
        # Ensure multiplier lies within the expected range [min_delay, max_delay]
        if random_scalar > max_delay:
            random_scalar = max_delay
        if random_scalar < min_delay:
            random_scalar = min_delay
        multipliers.append(random_scalar)
    shuffle(multipliers)

    # Create a new map with traffic
    counter = 0
    new_map = Map(time_units=map.time_units, verbose=map.verbose)
    for start, duration_mapping in map._adjacency_list.items():
        for end, duration in duration_mapping.items():
            if (
                start not in new_map._adjacency_list
                or end not in new_map._adjacency_list[start]
            ):
                new_map.add_route(
                    start=start, end=end, duration=duration * multipliers[counter]
                )
                counter += 1
    return new_map
