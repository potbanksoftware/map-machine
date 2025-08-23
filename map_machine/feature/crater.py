#!/usr/bin/env python3
#
#  crater.py
"""
Crater on the map.
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

__all__ = ["Crater"]


class Crater(Tagged):
	"""Volcano or impact crater on the map."""

	def __init__(self, tags: dict[str, str], coordinates: np.ndarray, point: np.ndarray) -> None:
		super().__init__(tags)
		self.coordinates: np.ndarray = coordinates
		self.point: np.ndarray = point

	def draw(self, svg: Drawing, flinger: Flinger) -> None:
		"""Draw crater ridge."""
		scale: float = flinger.get_scale(self.coordinates)
		assert "diameter" in self.tags
		radius: float = float(self.tags["diameter"]) / 2.0
		radial_gradient = svg.radialGradient(
				center=self.point + np.array((0.0, radius * scale / 7.0)),
				r=radius * scale,
				gradientUnits="userSpaceOnUse",
				)
		color: Color = Color("#000000")
		gradient = svg.defs.add(radial_gradient)
		(
				gradient.add_stop_color(0.0, color.hex,
										opacity=0.2).add_stop_color(0.7, color.hex, opacity=0.2
																	).add_stop_color(1.0, color.hex, opacity=1.0)
				)  # fmt: skip
		circle = svg.circle(
				self.point,
				radius * scale,
				fill=gradient.get_funciri(),
				opacity=0.2,
				)
		svg.add(circle)
