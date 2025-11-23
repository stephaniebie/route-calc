import pytest
from route_calc.location import Location


def test_init():
    test_location = Location(
        name="Location Name",
        latitude=0,
        longitude=0,
    )
    assert test_location.name == "Location Name"
    assert test_location.latitude == 0
    assert test_location.longitude == 0


def test_eq():
    original_location = Location(
        name="Location Name",
        latitude=0,
        longitude=0,
    )
    same_location = Location(
        name="Location Name",
        latitude=0,
        longitude=0,
    )
    different_location = Location(
        name="Another Name",
        latitude=10,
        longitude=10,
    )
    different_location_same_name = Location(
        name="Location Name",
        latitude=10,
        longitude=10,
    )
    same_location_different_name = Location(
        name="Another Name",
        latitude=0,
        longitude=0,
    )

    assert original_location == same_location
    assert original_location == "Location Name"
    assert original_location != different_location
    assert original_location != different_location_same_name
    assert original_location != same_location_different_name

    # Check that TypeErrors are raised appropriately
    with pytest.raises(TypeError) as exception:
        original_location == 0
    assert f"Cannot establish equality between Location and {int} objects" == str(
        exception.value
    )
