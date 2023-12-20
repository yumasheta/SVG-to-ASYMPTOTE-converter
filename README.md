# SVG to Asymptote Converter
This script takes an SVG file containing one or more Bézier curves and creates code to replicate the curves in [Asymptote](http://asymptote.ualberta.ca/). Specifically, the code contains declaration of `path` variables, which can then be drawn with the usual `draw` command.
## Usage
Calling
```bash
python run.py [-h] -f FILE [--debug]
```
from the terminal parses the SVG file `FILE` and outputs Asymptote code for all the contained Bézier curvers. The `--debug` flag is optional and creates dots at the positions of all control points.

## Supported features
- Cubic Bézier curves (open and closed)
