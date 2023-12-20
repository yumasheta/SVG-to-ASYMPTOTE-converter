#! /usr/bin/env python3

from __future__ import annotations
from typing import Sequence
from xml.dom import minidom

from coordinate_type import CoordPair


class Asymptote:

    @classmethod
    def load_svg(cls, svg_filename: str):
        """Extract a list of all 'path' tags from the file svg_filename."""

        with minidom.parse(svg_filename) as doc:
            path_strings = [path.getAttribute('d')
                            for path in doc.getElementsByTagName('path')]

        return path_strings

    @classmethod
    def points_to_dots(cls, points: Sequence[CoordPair]):
        """Generate a dot asy command for each `CoordPair` in points."""
        return "\n".join(f"dot({p});" for p in points)


class BezierCubic(Asymptote):
    """Generate asy command for cubic bezier curves."""

    stride = 3

    @classmethod
    def _build_cubic_control_points(cls, start: str, points: Sequence[str]):
        start = CoordPair(map(float, start.split(",")))
        controls = [start]

        for p1, p2, p3 in zip(
            points[0:-cls.stride+1:cls.stride],
            points[1:-cls.stride+2:cls.stride],
            points[2::cls.stride]
        ):
            pre = controls[-1]
            controls += [
                CoordPair(map(float, p1.split(",")))+pre,
                CoordPair(map(float, p2.split(",")))+pre,
                CoordPair(map(float, p3.split(",")))+pre,
            ]

        return controls

    @classmethod
    def _cubic_to_asy_command(cls, controls: Sequence[CoordPair], pathname: str):
        # the asy command string
        asy = f"path {pathname} = "
        # exclude the last elem in controls
        for p, c1, c2 in zip(
            controls[0:-cls.stride:cls.stride],
            controls[1:-cls.stride+1:cls.stride],
            controls[2:-cls.stride+2:cls.stride],
        ):
            asy += f"{p}..controls {c1} and {c2}.."

        asy += str(controls[-1])
        return asy

    @classmethod
    def from_svg(cls, svg_string: str, debug=False, pathname="path1"):
        """Convert the svg string command for cubic spline to asy.

        svg_string: svg cubic spline command
        debug: if True, generate `dot();` asy commands for each node and control point
        pathname: name of the path variable in asy command
        """

        points = svg_string.split(" ")

        if points[-1] in ["z", "Z"]:
            # the path is cyclic
            asy_end = "..cycle;"
            points = points[:-1]
        else:
            asy_end = ";"

        control_points = cls._parse_cubic_svg(points)
        asy = cls._cubic_to_asy_command(control_points, pathname) + asy_end

        if debug is True:
            asy_debug = cls.points_to_dots(control_points)
            return asy + "\n" + asy_debug

        return asy

    @classmethod
    def _parse_cubic_svg(cls, points):
        match points:
            case ["M", start, "C", *points]:
                # we are in absolute coordinates
                raise NotImplementedError
            case ["m", start, "c", *points]:
                # we are in relative coords
                control_points = cls._build_cubic_control_points(start, points)
            case _:
                raise Exception("The path is not a cubic spline!")

        return control_points
