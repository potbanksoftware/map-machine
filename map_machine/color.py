#!/usr/bin/env python3
#
#  color.py
"""
Color utility.
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

# stdlib
from typing import Any

# 3rd party
from colour import Color  # type: ignore[import-untyped]

# this package
from map_machine.util import MinMax

__all__ = ["get_gradient_color", "is_bright"]


def is_bright(color: Color) -> bool:
	"""
	Check whether color is bright enough to have black outline instead of white.
	"""
	return (0.2126 * color.red + 0.7152 * color.green + 0.0722 * color.blue > 0.78125)


def get_gradient_color(value: Any, bounds: MinMax, colors: list[Color]) -> Color:
	"""
	Get color from the color scale for the value.

	:param value: given value (should be in bounds)
	:param bounds: maximum and minimum values
	:param colors: color scale
	"""
	color_length: int = len(colors) - 1
	scale: list[Color] = colors + [Color("black")]

	range_coefficient: float = (0.0 if bounds.is_empty() else (value - bounds.min_) / bounds.delta())
	# If value is out of range, set it to boundary value.
	range_coefficient = min(1.0, max(0.0, range_coefficient))
	index: int = int(range_coefficient * color_length)
	coefficient: float = (range_coefficient - index / color_length) * color_length

	return Color(
			rgb=[
					scale[index].rgb[i] + coefficient * (scale[index + 1].rgb[i] - scale[index].rgb[i])
					for i in range(3)
					]
			)
