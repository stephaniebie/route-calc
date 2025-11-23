from __future__ import annotations


class Location:
    def __init__(
        self, name: str, latitude: float | None = None, longitude: float | None = None
    ):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.name

    def __eq__(self, other: Location | str):
        # If other is a Location object, require all attributes to match
        if isinstance(other, Location):
            return vars(self) == vars(other)
        # If other is just a string, match it to the name
        elif isinstance(other, str):
            return self.name == other
        raise TypeError(
            f"Cannot establish equality between Location and {type(other)} objects"
        )

    def __hash__(self):
        return hash(self.name)
