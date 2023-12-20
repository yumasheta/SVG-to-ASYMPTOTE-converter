"""CLI interface."""

from argparse import ArgumentParser, FileType

from svg_to_asy import BezierCubic


def parse_cli():
    """Parse cli args and print asymptote code."""
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", required=True, type=FileType("r"))
    parser.add_argument("--debug", action='store_true')
    args = parser.parse_args()

    path_strings = BezierCubic.load_svg(args.file)

    for i, possible_bezier in enumerate(path_strings, 1):
        print(BezierCubic.from_svg(possible_bezier, args.debug, f"path{i}"))


if __name__ == "__main__":
    parse_cli()
