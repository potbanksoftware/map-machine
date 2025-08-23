#!/usr/bin/env python3
#
#  figure.py
"""
Figures displayed on the map.
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

# this package
from map_machine.geometry.flinger import Flinger
from map_machine.geometry.vector import Polyline
from map_machine.osm.osm_reader import OSMNode, Tagged
from map_machine.scheme import LineStyle

__all__ = ["Figure", "StyledFigure", "get_path", "is_clockwise", "make_clockwise", "make_counter_clockwise"]


class Figure(Tagged):
	"""Some figure on the map: way or area."""

	def __init__(
			self,
			tags: dict[str, str],
			inners: list[list[OSMNode]],
			outers: list[list[OSMNode]],
			) -> None:
		super().__init__(tags)

		if inners and outers:
			self.inners: list[list[OSMNode]] = list(map(make_clockwise, inners))
			self.outers: list[list[OSMNode]] = list(map(make_counter_clockwise, outers))
		else:
			self.inners = inners
			self.outers = outers

	def get_path(self, flinger: Flinger, offset: np.ndarray = np.array((0.0, 0.0))) -> str:
		"""
		Get SVG path commands.

		:param flinger: converter for geo coordinates
		:param offset: offset vector
		"""
		path: str = ''

		for outer_nodes in self.outers:
			path += f"{get_path(outer_nodes, offset, flinger)} "

		for inner_nodes in self.inners:
			path += f"{get_path(inner_nodes, offset, flinger)} "

		return path


class StyledFigure(Figure):
	"""Figure with stroke and fill style."""

	def __init__(
			self,
			tags: dict[str, str],
			inners: list[list[OSMNode]],
			outers: list[list[OSMNode]],
			line_style: LineStyle,
			) -> None:
		super().__init__(tags, inners, outers)
		self.line_style: LineStyle = line_style

	def get_path(
			self,
			flinger: Flinger,
			offset: np.ndarray = np.array((0.0, 0.0)),
			) -> str:
		"""
		Get SVG path commands.

		:param flinger: converter for geo coordinates
		:param offset: offset vector
		"""
		path: str = ''

		for outer_nodes in self.outers:
			commands: str = get_path(outer_nodes, offset, flinger, self.line_style.parallel_offset)
			path += f"{commands} "

		for inner_nodes in self.inners:
			commands = get_path(inner_nodes, offset, flinger, self.line_style.parallel_offset)
			path += f"{commands} "

		return path

	def get_layer(self) -> float:
		"""
		Get figure layer value or 0 if it is not specified.

		TODO: support values separated by "," or ";".
		"""
		try:
			if "layer" in self.tags:
				return float(self.tags["layer"])
		except ValueError:
			return 0.0
		return 0.0

	def __lt__(self, other: "StyledFigure") -> bool:
		"""Compare figures based on priority and layer."""
		if self.get_layer() != other.get_layer():
			return self.get_layer() < other.get_layer()

		return self.line_style.priority < other.line_style.priority


def is_clockwise(polygon: list[OSMNode]) -> bool:
	"""
	Return true if polygon nodes are in clockwise order.

	:param polygon: list of OpenStreetMap nodes
	"""
	count: float = 0.0
	for index, node in enumerate(polygon):
		next_index: int = 0 if index == len(polygon) - 1 else index + 1
		count += (polygon[next_index].coordinates[0] - node.coordinates[0]) * (
				polygon[next_index].coordinates[1] + node.coordinates[1]
				)
	return count >= 0.0


def make_clockwise(polygon: list[OSMNode]) -> list[OSMNode]:
	"""
	Make polygon nodes clockwise.

	:param polygon: list of OpenStreetMap nodes
	"""
	return polygon if is_clockwise(polygon) else list(reversed(polygon))


def make_counter_clockwise(polygon: list[OSMNode]) -> list[OSMNode]:
	"""
	Make polygon nodes counter-clockwise.

	:param polygon: list of OpenStreetMap nodes
	"""
	return polygon if not is_clockwise(polygon) else list(reversed(polygon))


def get_path(
		nodes: list[OSMNode],
		shift: np.ndarray,
		flinger: Flinger,
		parallel_offset: float = 0.0,
		) -> str:
	"""Construct SVG path commands from nodes."""
	return Polyline([flinger.fling(node.coordinates) + shift for node in nodes]).get_path(parallel_offset)
