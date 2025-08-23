#!/usr/bin/env python3
#
#  tree.py
"""
Drawing tree features on the map.

If radius of trunk or crown are specified they are displayed with simple
circles.
"""
#
#  Copyright © 2021 Sergey Vartanov <me@enzet.ru>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
import numpy as np
from colour import Color  # type: ignore[import-untyped]
from svgwrite import Drawing  # type: ignore[import-untyped]

# this package
from map_machine.geometry.flinger import Flinger
from map_machine.osm.osm_reader import Tagged
from map_machine.scheme import Scheme

__all__ = ["Tree"]


class Tree(Tagged):
	"""Tree on the map."""

	def __init__(self, tags: dict[str, str], coordinates: np.ndarray, point: np.ndarray) -> None:
		super().__init__(tags)
		self.coordinates: np.ndarray = coordinates
		self.point: np.ndarray = point

	def draw(self, svg: Drawing, flinger: Flinger, scheme: Scheme) -> None:
		"""Draw crown and trunk."""
		scale: float = flinger.get_scale(self.coordinates)

		radius: float
		if diameter_crown := self.get_float("diameter_crown") is not None:
			radius = diameter_crown / 2.0
		else:
			radius = 2.0

		color: Color = scheme.get_color("evergreen_color")
		svg.add(svg.circle(self.point, radius * scale, fill=color, opacity=0.3))

		if (circumference := self.get_float("circumference")) is not None:
			radius = circumference / 2.0 / np.pi
			circle = svg.circle(self.point, radius * scale, fill=scheme.get_color("trunk_color"))
			svg.add(circle)
