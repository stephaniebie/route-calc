from csv import DictReader
from route_calc.map import Map
from route_calc.location import Location


def read_locations(path: str) -> list:
    """
    Read a CSV into a list of Location objects.
    NOTE: Makes assumptions about the CSV header titles

    Parameters
    ----------
    path: str
        Path to the CSV file
    """
    with open(path, "r") as f:
        return [
            Location(
                name=row["name"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )
            for row in DictReader(f)
        ]


def read_routes(
    path: str,
    locations: list | None = None,
    time_units: str = "minutes",
    verbose: bool = False,
) -> Map:
    """
    Read a CSV into a Map object.
    NOTE: Makes assumptions about the CSV header titles and data types

    Parameters
    ----------
    path: str
        Path to the CSV file
    locations: list | None
        List of Location objects with additional information populated
    time_units: str
        The units to use for tracking the route durations
    verbose: bool
        Toggles verbosity of print statements

    Returns
    -------
    Map object
    """
    points_of_interest = Map(time_units=time_units, verbose=verbose)
    with open(path, "r") as f:
        for row in DictReader(f):
            # Configure start and end locations
            try:
                start_location = locations[locations.index(row["start"])]
            except:
                start_location = Location(name=row["start"])
            try:
                end_location = locations[locations.index(row["end"])]
            except:
                end_location = Location(name=row["end"])

            # Add route to map
            points_of_interest.add_route(
                start=start_location,
                end=end_location,
                duration=float(row["duration"]),
            )
    return points_of_interest
