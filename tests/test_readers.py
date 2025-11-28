import pytest
from route_calc.map import Map
from route_calc.location import Location
from route_calc.readers import read_locations, read_routes


def test_read_locations():
    expected_locations = [
        Location(
            name="Fenway Park",
            latitude=42.346268,
            longitude=-71.095764,
        ),
        Location(
            name="Boston Public Garden",
            latitude=42.3541614,
            longitude=-71.0704078,
        ),
        Location(
            name="Old North Church",
            latitude=42.3663277,
            longitude=-71.0544555,
        ),
        Location(
            name="Faneuil Hall",
            latitude=42.360031,
            longitude=-71.054749,
        ),
        Location(
            name="Boston Common",
            latitude=42.355083,
            longitude=-71.06588,
        ),
        Location(
            name="Museum of Fine Arts Boston",
            latitude=42.339359,
            longitude=-71.094292,
        ),
        Location(
            name="Symphony Hall",
            latitude=42.342025,
            longitude=-71.085784,
        ),
        Location(
            name="Bunker Hill Monument",
            latitude=42.376296,
            longitude=-71.060348,
        ),
        Location(
            name="Massachusetts State House",
            latitude=42.3587415,
            longitude=-71.0638745,
        ),
        Location(
            name="Boston Tea Party Ships & Museum",
            latitude=42.352231,
            longitude=-71.051626,
        ),
    ]
    assert read_locations("data/locations.csv") == expected_locations


def test_read_routes(tmp_path):
    temp_file = tmp_path / "test_readers.csv"
    temp_file.write_text(
        "\n".join(
            [
                "start,end,duration",
                "A,B,5",
                "A,C,10.5",
                "C,B,50",
            ]
        )
    )

    expected_map = Map()
    A = Location(name="A", latitude=None, longitude=None)
    B = Location(name="B", latitude=None, longitude=None)
    C = Location(name="C", latitude=None, longitude=None)
    expected_map.add_route(start=A, end=B, duration=5)
    expected_map.add_route(start=A, end=C, duration=10.5)
    expected_map.add_route(start=C, end=B, duration=50)

    assert read_routes(temp_file) == expected_map
