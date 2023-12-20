"""Provides the `CoordPair` type used to handle coordinate pair tuples.

`CoordPair` implements storing 2-tuples and addition of instances.
String representation of `CoordPair` flips the y coordinate.
"""

from __future__ import annotations
from typing import Generic, Iterable, TypeVar

CT = TypeVar("CT")


class CoordPair(Generic[CT]):
    """Implements coordinate pair supporting "+"."""

    def __init__(self, iter_pair: Iterable[CT]):
        """Converts iterable of len==2 to a CoordPair."""
        iterator = iter(iter_pair)
        x_coord = next(iterator)
        y_coord = next(iterator)
        try:
            next(iterator)
            raise LookupError("Iterable contains more than 2 elements")
        except StopIteration:
            self._coords = (x_coord, y_coord)

    def __getitem__(self, idx: int) -> CT:
        return self._coords[idx]

    def __add__(self, other: CoordPair):
        return type(self)((self[0]+other[0], self[1]+other[1]))

    def __str__(self):
        # the minus flips the y axis
        # s.t. svg (top to bottom) becomes asymptote (bottom to top)
        return str((self[0], -self[1]))
