#!/usr/bin/env python3
#
#  building.py
"""
Buildings on the map.
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
import svgwrite  # type: ignore[import-untyped]
from colour import Color  # type: ignore[import-untyped]
from svgwrite import Drawing
from svgwrite.container import Group  # type: ignore[import-untyped]
from svgwrite.path import Path  # type: ignore[import-untyped]

# this package
from map_machine.drawing import PathCommands
from map_machine.figure import Figure
from map_machine.geometry.flinger import Flinger
from map_machine.geometry.vector import Segment
from map_machine.osm.osm_reader import OSMNode
from map_machine.scheme import Scheme

__all__ = ["Building", "draw_walls"]

BUILDING_MINIMAL_HEIGHT: float = 8.0
BUILDING_SCALE: float = 0.33
LEVEL_HEIGHT: float = 2.5
SHADE_SCALE: float = 0.4


class Building(Figure):
	"""Building on the map."""

	def __init__(
			self,
			tags: dict[str, str],
			inners: list[list[OSMNode]],
			outers: list[list[OSMNode]],
			flinger: Flinger,
			scheme: Scheme,
			) -> None:
		super().__init__(tags, inners, outers)

		self.is_construction: bool = (tags.get("building") == "construction" or tags.get("construction") == "yes")
		self.has_walls: bool = tags.get("building") != "roof"

		self.default_fill: Color
		self.default_stroke: Color
		if self.is_construction:
			self.default_fill = scheme.get_color("building_construction_color")
			self.default_stroke = scheme.get_color("building_construction_border_color")
		else:
			self.default_fill = scheme.get_color("building_color")
			self.default_stroke = scheme.get_color("building_border_color")

		self.fill: Color
		self.stroke: Color
		if color := tags.get("roof:colour"):
			self.fill = scheme.get_color(color)
			self.stroke = Color(self.fill)
			self.stroke.set_luminance(self.fill.get_luminance() * 0.85)
		else:
			self.fill = scheme.get_color("building_color")
			self.stroke = scheme.get_color("building_border_color")

		self.parts: list[Segment] = []

		for nodes in self.inners + self.outers:
			for i in range(len(nodes) - 1):
				flung_1: np.ndarray = flinger.fling(nodes[i].coordinates)
				flung_2: np.ndarray = flinger.fling(nodes[i + 1].coordinates)
				self.parts.append(Segment(flung_1, flung_2))

		self.parts = sorted(self.parts)

		self.height: float = BUILDING_MINIMAL_HEIGHT
		self.min_height: float = 0.0

		self.wall_default_color: Color
		if self.is_construction:
			self.wall_default_color = scheme.get_color("wall_construction_color")
		else:
			self.wall_default_color = scheme.get_color("wall_color")

		self.wall_color: Color = self.wall_default_color
		if material := tags.get("building:material"):
			if material in scheme.material_colors:
				self.wall_color = Color(scheme.material_colors[material])
		if color := tags.get("building:colour"):
			self.wall_color = scheme.get_color(color)
		if color := tags.get("colour"):
			self.wall_color = scheme.get_color(color)

		if levels := self.get_float("building:levels"):
			self.height = BUILDING_MINIMAL_HEIGHT + levels * LEVEL_HEIGHT

		if levels := self.get_float("building:min_level"):
			self.min_height = BUILDING_MINIMAL_HEIGHT + levels * LEVEL_HEIGHT

		if height := self.get_length("height"):
			self.height = BUILDING_MINIMAL_HEIGHT + height

		if height := self.get_length("min_height"):
			self.min_height = BUILDING_MINIMAL_HEIGHT + height

	def draw(self, svg: Drawing, flinger: Flinger, use_building_colors: bool) -> None:
		"""Draw simple building shape."""
		path: Path = Path(
				d=self.get_path(flinger),
				stroke=self.stroke.hex if use_building_colors else self.default_stroke.hex,
				fill=self.fill.hex if use_building_colors else self.default_fill.hex,
				stroke_linejoin="round",
				)
		svg.add(path)

	def draw_shade(self, building_shade: Group, flinger: Flinger) -> None:
		"""Draw shade cast by the building."""
		scale: float = flinger.get_scale() * SHADE_SCALE
		shift_1: np.ndarray = np.array((scale * self.min_height, 0.0))
		shift_2: np.ndarray = np.array((scale * self.height, 0.0))
		commands: str = self.get_path(flinger, shift_1)
		path: Path = Path(commands, fill="#000000", stroke="#000000", stroke_width=1.0)
		building_shade.add(path)
		for nodes in self.inners + self.outers:
			for i in range(len(nodes) - 1):
				flung_1 = flinger.fling(nodes[i].coordinates)
				flung_2 = flinger.fling(nodes[i + 1].coordinates)
				command: PathCommands = [
						'M',
						np.add(flung_1, shift_1),
						'L',
						np.add(flung_2, shift_1),
						np.add(flung_2, shift_2),
						np.add(flung_1, shift_2),
						'Z',
						]
				path = Path(command, fill="#000000", stroke="#000000", stroke_width=1.0)
				building_shade.add(path)

	def draw_walls(
			self,
			svg: Drawing,
			height: float,
			previous_height: float,
			scale: float,
			use_building_colors: bool,
			) -> None:
		"""Draw building walls."""
		if not self.has_walls:
			return

		shift_1: np.ndarray = np.array((0.0, -previous_height * scale * BUILDING_SCALE))
		shift_2: np.ndarray = np.array((0.0, -height * scale * BUILDING_SCALE))

		for segment in self.parts:
			draw_walls(
					svg,
					self,
					segment,
					height,
					shift_1,
					shift_2,
					use_building_colors,
					)

	def draw_roof(
			self,
			svg: Drawing,
			flinger: Flinger,
			scale: float,
			use_building_colors: bool,
			) -> None:
		"""Draw building roof."""

		fill: Color = self.fill if use_building_colors else self.default_fill
		stroke: Color = (self.stroke if use_building_colors else self.default_stroke)

		path: Path = Path(
				d=self.get_path(flinger, np.array([0.0, -self.height * scale * BUILDING_SCALE])),
				stroke=stroke,
				fill="none" if self.is_construction else fill.hex,
				stroke_linejoin="round",
				)
		svg.add(path)


def draw_walls(
		svg: svgwrite.Drawing,
		building: Building,
		segment: Segment,
		height: float,
		shift_1: np.ndarray,
		shift_2: np.ndarray,
		use_building_colors: bool,
		) -> None:
	"""
    Draw walls for buildings as a quadrangle.

    Color of the wall is based on illumination.
    """
	color: Color = (building.wall_color if use_building_colors else building.wall_default_color)

	if building.is_construction:
		color_part: float = segment.angle * 0.2
		color = Color(
				rgb=(
						color.get_red() + color_part,
						color.get_green() + color_part,
						color.get_blue() + color_part,
						)
				)
	elif height <= 0.25 / BUILDING_SCALE:
		color = Color(color)
		color.set_luminance(color.get_luminance() * 0.70)
	elif height <= 0.5 / BUILDING_SCALE:
		color = Color(color)
		color.set_luminance(color.get_luminance() * 0.85)
	else:
		color_part = segment.angle * 0.2 - 0.1
		color = Color(
				rgb=(
						max(min(color.get_red() + color_part, 1), 0),
						max(min(color.get_green() + color_part, 1), 0),
						max(min(color.get_blue() + color_part, 1), 0),
						)
				)

	command: PathCommands = [
			'M',
			segment.point_1 + shift_1,
			'L',
			segment.point_2 + shift_1,
			segment.point_2 + shift_2,
			segment.point_1 + shift_2,
			segment.point_1 + shift_1,
			'Z',
			]
	path: Path = Path(
			d=command,
			fill=color.hex,
			stroke=color.hex,
			stroke_width=1,
			stroke_linejoin="round",
			)
	svg.add(path)
