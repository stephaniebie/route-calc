from __future__ import annotations
from route_calc.location import Location


class Map:
    """
    An abstracted geographical map as an adjacency list.
    """

    def __init__(self, time_units: str = "minutes", verbose: bool = False):
        """
        Parameters
        ----------
        time_units: str
            The units to use for tracking the route durations
        verbose: bool
            Toggles verbosity of print statements
        """
        self.time_units = time_units
        self.verbose = verbose
        self._adjacency_list = {}

    def __repr__(self):
        return f"Map of {len(self._adjacency_list)} locations and {sum([len(r.values()) for r in self._adjacency_list.values()])} possible routes"

    def __eq__(self, other: Map):
        if isinstance(other, Map):
            return self._adjacency_list == other._adjacency_list
        raise TypeError(
            f"Cannot establish equality between Map and {type(other)} objects"
        )

    def add_route(self, start: Location, end: Location, duration: float = 0.0):
        """
        Add a route to the map.
        NOTE: Assumes duration is the same to and from the starting location.

        Parameters
        ----------
        start: Location
            Starting location for the route
        end: Location
            Ending location for the route
        duration: float
            Time it takes to traverse the route
        """
        # Adds starting location to adjacency list
        if start not in self._adjacency_list:
            if self.verbose:
                print(f"Starting location {start} not in map. Adding...")
            self._adjacency_list[start] = {}
        # Adds end location to adjacency list
        if end not in self._adjacency_list:
            if self.verbose:
                print(f"Ending location {end} not in map. Adding...")
            self._adjacency_list[end] = {}
        # Adds duration to adjacency list
        self._adjacency_list[start][end] = duration
        self._adjacency_list[end][start] = duration

    def calculate_duration(self, start: Location | str, end: Location | str) -> float:
        """
        Calculates the minimum duration required for a route using Dijkstra's algorithm.

        Parameters
        ----------
        start: Location | str
            Starting location
        end: Location | str
            Ending location

        Returns
        -------
        Minimum duration from start to end as a float
        """
        # Assert that these events are in the map first
        assert start in self._adjacency_list, f"{start.name} not in map"
        assert end in self._adjacency_list, f"{end.name} not in map"

        # Create a set of unvisited locations
        locations = list(self._adjacency_list)
        durations = {loc: (0 if loc == start else float("inf")) for loc in locations}
        parent = {loc: None for loc in locations}
        if self.verbose:
            print(
                f"Calculating durations from {start} to {end}.\nCurrent update:\n{durations}"
            )

        while locations:
            # Calculate the location with the minimum duration
            min_duration_location = min(locations, key=lambda l: durations[l])
            # Stop searching at end of the route
            if min_duration_location == end:
                break
            # Move on to other locations after calculating the duration
            locations.remove(min_duration_location)

            # Check neighboring locations for even shorter durations
            for location, duration in self._adjacency_list[
                min_duration_location
            ].items():
                duration += durations[min_duration_location]
                if duration < durations[location]:
                    durations[location] = duration
                    parent[location] = min_duration_location
                if self.verbose:
                    print(f"Current update:\n{durations}")
        return durations[end]
