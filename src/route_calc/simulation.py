from route_calc.map import Map
from random import normalvariate, random, shuffle


def simulate_traffic(
    map: Map,
    min_delay: float = 1.0,
    max_delay: float = 1.0,
    risk: float = 0.0,
    risk_count: int = 3,
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
    risk: float
        The chance that a route will experience an extreme event such as a severe delay (10+ times
        the duration) or road blockage. A blockage is defined to be a route of infinite duration.
        There is a 20% chance an extreme event will be a blockage. Must be between 0 and 1, inclusive.
    risk_count: int
        Number of events to apply the risk factor to

    Returns
    -------
    A new Map object with modified durations
    """
    # Assert risk to be bounded between 0 and 1, inclusive
    assert (
        risk <= 1 and risk >= 0
    ), f"Invalid risk factor {risk}. Please use a number between 0 and 1, inclusive"

    # Calculate mean and standard deviation for 99.7% containment
    mean = (min_delay + max_delay) / 2
    stdev = (max_delay - min_delay) / 6

    # Get the number of routes and affected routes (for discrete distribution)
    # NOTE: This calculation is only true because we're assuming duration is the same in both directions!!
    number_of_routes = int(
        sum([len(r.values()) for r in map._adjacency_list.values()]) / 2
    )

    # Generate a randomized set of multipliers
    multipliers = []
    for _ in range(number_of_routes):
        route_at_risk = False
        if risk_count > 0:
            # Determines the risk of the route having an extreme event
            route_at_risk = random() < risk
            risk_count -= 1

        # Route is at risk
        if route_at_risk:
            # Hard-coding a 20% chance the road will experience a blockage
            random_scalar = (
                float("inf") if random() < 0.2 else normalvariate(mean, stdev) + 10
            )
        # Route not at risk
        else:
            # Selected a random normally distributed value
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
                # Logging
                if map.verbose:
                    if multipliers[counter] == float("inf"):
                        print(f"Route [{start}] <-> [{end}] has a road blockage")
                    elif multipliers[counter] == 1:
                        print(f"Route [{start}] <-> [{end}] is not delayed")
                    else:
                        print(
                            f"Route [{start}] <-> [{end}] is delayed by a factor of {multipliers[counter]}"
                        )
                new_map.add_route(
                    start=start, end=end, duration=duration * multipliers[counter]
                )
                counter += 1
    return new_map
