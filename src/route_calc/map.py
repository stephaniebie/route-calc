from __future__ import annotations
import heapq
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
        dist, prev = self._dijkstra(start=start, end=end)
        return dist

    def construct_path(self, start: Location | str, end: Location | str) -> list:
        """
        Reconstructs the path from start to end

        Parameters
        ----------
        start: Location | str
            Starting location
        end: Location | str
            Ending location

        Returns
        -------
        List of locations from start to end
        """
        dist, prev = self._dijkstra(start=start, end=end)
        path = []
        cur = [n for n in self._adjacency_list if n == end][0]
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        if path and path[0] == start:
            return path
        return []

    def _dijkstra(
        self, start: Location | str, end: Location | str
    ) -> tuple[float, dict]:
        """
        Implementation of Dijkstra's algorithm.

        Parameters
        ----------
        start: Location | str
            Starting location
        end: Location | str
            Ending location

        Returns
        -------
        Minimum duration from start to end as a float
        Previous node in shortest path as a dictionary
        """
        # Convert strings to Locations
        start_node = [n for n in self._adjacency_list if n == start][0]
        end_node = [n for n in self._adjacency_list if n == end][0]

        distances = {node: float("inf") for node in self._adjacency_list}
        distances[start_node] = 0
        prev = {node: None for node in self._adjacency_list}
        visited = set()
        counter = 0
        pq = [(0, counter, start_node)]

        while pq:
            curr_time, _, curr_node = heapq.heappop(pq)

            if curr_node in visited:
                continue
            visited.add(curr_node)

            if curr_node == end_node:
                return curr_time, prev
            for neighbor, weight in self._adjacency_list[curr_node].items():
                if neighbor in visited:
                    continue
                total_time = curr_time + weight
                if total_time < distances[neighbor]:
                    distances[neighbor] = total_time
                    prev[neighbor] = curr_node
                    counter += 1
                    heapq.heappush(pq, (total_time, counter, neighbor))
