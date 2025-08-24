#!/usr/bin/env python3
#
#  mapper.py
"""
Simple OpenStreetMap renderer.
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
import logging
import sys
from pathlib import Path
from typing import Iterator, Optional

# 3rd party
import numpy as np
import svgwrite  # type: ignore[import-untyped]
from colour import Color  # type: ignore[import-untyped]
from svgwrite.container import Group  # type: ignore[import-untyped]
from svgwrite.path import Path as SVGPath  # type: ignore[import-untyped]
from svgwrite.shapes import Rect  # type: ignore[import-untyped]

# this package
from map_machine.constructor import Constructor
from map_machine.drawing import draw_text
from map_machine.feature.building import BUILDING_SCALE, Building, draw_walls
from map_machine.feature.road import Intersection, Road, RoadPart
from map_machine.figure import StyledFigure
from map_machine.geometry.boundary_box import BoundaryBox
from map_machine.geometry.flinger import Flinger, MercatorFlinger
from map_machine.geometry.vector import Segment
from map_machine.map_configuration import BuildingMode, DrawingMode, LabelMode, MapConfiguration
from map_machine.osm.osm_getter import get_osm
from map_machine.osm.osm_reader import OSMData, OSMNode
from map_machine.pictogram.icon import ShapeExtractor
from map_machine.pictogram.point import Occupied, Point
from map_machine.scheme import Scheme
from map_machine.workspace import workspace

__all__ = ["Map", "render_map"]

ROAD_PRIORITY: float = 40.0
DEFAULT_SIZE: tuple[float, float] = (800.0, 600.0)


class Map:
	"""Map drawing."""

	def __init__(
			self,
			flinger: Flinger,
			svg: svgwrite.Drawing,
			configuration: MapConfiguration,
			) -> None:
		self.flinger: Flinger = flinger
		self.svg: svgwrite.Drawing = svg
		self.scheme: Scheme = configuration.scheme
		self.configuration = configuration

		self.background_color: Color = self.scheme.get_color("background_color")
		if color := self.configuration.background_color():
			self.background_color = color

	def draw(self, constructor: Constructor) -> None:
		"""Draw map."""
		self.svg.add(Rect((0.0, 0.0), self.flinger.size, fill=self.background_color))
		logging.info("Drawing ways...")

		figures: list[StyledFigure] = constructor.get_sorted_figures()

		top_figures: list[StyledFigure] = [x for x in figures if x.line_style.priority >= ROAD_PRIORITY]
		bottom_figures: list[StyledFigure] = [x for x in figures if x.line_style.priority < ROAD_PRIORITY]

		for figure in bottom_figures:
			path_commands: str = figure.get_path(self.flinger)
			if path_commands:
				path: SVGPath = SVGPath(d=path_commands)
				path.update(figure.line_style.style)
				self.svg.add(path)

		constructor.roads.draw(self.svg, self.flinger)

		for figure in top_figures:
			path_commands = figure.get_path(self.flinger)
			if path_commands:
				path = SVGPath(d=path_commands)
				path.update(figure.line_style.style)
				self.svg.add(path)

		if self.scheme.draw_trees:
			for tree in constructor.trees:
				tree.draw(self.svg, self.flinger, self.scheme)

		if self.scheme.draw_craters:
			for crater in constructor.craters:
				crater.draw(self.svg, self.flinger)

		if self.scheme.draw_buildings:
			self.draw_buildings(constructor, self.configuration.use_building_colors)

		if self.scheme.draw_directions:
			for direction_sector in constructor.direction_sectors:
				direction_sector.draw(self.svg, self.scheme)

		# All other points

		if self.scheme.draw_nodes:
			occupied: Optional[Occupied]
			if self.configuration.overlap == 0:
				occupied = None
			else:
				occupied = Occupied(
						self.flinger.size[0],
						self.flinger.size[1],
						self.configuration.overlap,
						)

			nodes: list[Point] = sorted(constructor.points, key=lambda x: -x.priority)
			logging.info("Drawing main icons...")
			for node in nodes:
				node.draw_main_shapes(self.svg, occupied)

			logging.info("Drawing extra icons...")
			for point in nodes:
				point.draw_extra_shapes(self.svg, occupied)

			logging.info("Drawing texts...")
			for point in nodes:
				if (not self.configuration.is_wireframe() and self.configuration.label_mode != LabelMode.NO):
					point.draw_texts(self.svg, occupied, self.configuration.label_mode)

		if self.configuration.show_credit:
			self.draw_credits(constructor.flinger.size)

	def draw_buildings(self, constructor: Constructor, use_building_colors: bool) -> None:
		"""Draw buildings: shade, walls, and roof."""
		if self.configuration.building_mode == BuildingMode.NO:
			return
		if self.configuration.building_mode == BuildingMode.FLAT:
			for building in constructor.buildings:
				building.draw(self.svg, self.flinger, use_building_colors)
			return

		logging.info("Drawing isometric buildings...")

		scale: float = self.flinger.get_scale()
		building_shade: Group = Group(opacity=0.1)
		for building in constructor.buildings:
			building.draw_shade(building_shade, self.flinger)
		self.svg.add(building_shade)

		walls: dict[Segment, Building] = {}

		for building in constructor.buildings:
			for part in building.parts:
				walls[part] = building

		sorted_walls = sorted(walls.keys())

		previous_height: float = 0.0
		for height in sorted(constructor.heights):
			shift_1: np.ndarray = np.array((0.0, -previous_height * scale * BUILDING_SCALE))
			shift_2: np.ndarray = np.array((0.0, -height * scale * BUILDING_SCALE))
			for wall in sorted_walls:
				building = walls[wall]
				if building.height < height or building.min_height >= height:
					continue

				draw_walls(
						self.svg,
						building,
						wall,
						height,
						shift_1,
						shift_2,
						use_building_colors,
						)

			if self.configuration.draw_roofs:
				for building in constructor.buildings:
					if building.height == height:
						building.draw_roof(self.svg, self.flinger, scale, use_building_colors)

			previous_height = height

	def draw_simple_roads(self, roads: Iterator[Road]) -> None:
		"""Draw road as simple SVG path."""
		nodes: dict[OSMNode, set[RoadPart]] = {}

		for road in roads:
			for index in range(len(road.nodes) - 1):
				node_1: OSMNode = road.nodes[index]
				node_2: OSMNode = road.nodes[index + 1]
				point_1: np.ndarray = self.flinger.fling(node_1.coordinates)
				point_2: np.ndarray = self.flinger.fling(node_2.coordinates)
				scale: float = self.flinger.get_scale(node_1.coordinates)
				part_1: RoadPart = RoadPart(point_1, point_2, road.lanes, scale)
				part_2: RoadPart = RoadPart(point_2, point_1, road.lanes, scale)
				# part_1.draw_normal(self.svg)

				for node in node_1, node_2:
					if node not in nodes:
						nodes[node] = set()

				nodes[node_1].add(part_1)
				nodes[node_2].add(part_2)

		for node, parts in nodes.items():
			if len(parts) < 4:
				continue
			intersection: Intersection = Intersection(list(parts))
			intersection.draw(self.svg, True)

	def draw_credits(self, size: np.ndarray) -> None:
		"""
		Add OpenStreetMap credit and the link to the project itself.
		OpenStreetMap requires to use the credit “© OpenStreetMap contributors”.

		See https://www.openstreetmap.org/copyright
		"""
		right_margin: float = 15.0
		bottom_margin: float = 15.0
		font_size: float = 10.0
		vertical_spacing: float = 2.0

		text_color: Color = Color("#888888")
		outline_color: Color = Color("#FFFFFF")

		credit_list: list[tuple[str, tuple[float, float]]]
		credit_list = [(f"Rendering: Map Machine", (right_margin, bottom_margin))]
		if self.configuration.credit:
			data_credit: tuple[str, tuple[float, float]] = (
					f"Data: {self.configuration.credit}",
					(right_margin, bottom_margin + font_size + vertical_spacing),
					)
			credit_list.append(data_credit)

		for text, point in credit_list:
			for stroke_width, stroke, opacity in (
				(3.0, outline_color, 0.7),
				(1.0, None, 1.0),
			):
				draw_text(
						self.svg,
						text,
						size - np.array(point),
						font_size,
						text_color,
						anchor="end",
						stroke_width=stroke_width,
						stroke=stroke,
						opacity=opacity,
						)


def render_map(
		input_file_names: list[Path],
		output_file_name: str,
		boundary_box: tuple[float, float, float, float],
		zoom: float,
		coordinates: tuple[float, float],
		size: tuple[float, float],
		scheme: str,
		cache: str,
		building_mode: BuildingMode,
		drawing_mode: DrawingMode,
		overlap: int,
		label_mode: LabelMode,
		level: str,
		seed: str,
		country: str,
		show_tooltips: bool,
		ignore_level_matching: bool,
		draw_roofs: bool,
		use_building_colors: bool,
		show_overlapped: bool,
		hide_credit: bool,
		) -> None:
	"""
	Map rendering entry point.

	:param arguments: command-line arguments
	"""
	scheme_path: Optional[Path] = workspace.find_scheme_path(scheme)
	if scheme_path is None:
		raise ValueError(f"Scheme `{scheme}` not found.")

	configuration: MapConfiguration = MapConfiguration(
			Scheme.from_file(scheme_path),
			drawing_mode=drawing_mode,
			building_mode=building_mode,
			label_mode=label_mode,
			zoom_level=zoom,
			overlap=overlap,
			level=level,
			seed=seed,
			show_tooltips=show_tooltips,
			country=country,
			ignore_level_matching=ignore_level_matching,
			draw_roofs=draw_roofs,
			use_building_colors=use_building_colors,
			show_overlapped=show_overlapped,
			show_credit=not hide_credit,
			)
	cache_path: Path = Path(cache)
	cache_path.mkdir(parents=True, exist_ok=True)

	# Compute boundary box.

	boundary_box_obj: Optional[BoundaryBox] = None

	# If boundary box is specified explicitly, use it or stop the rendering
	# process if the box is invalid.
	if boundary_box:
		boundary_box_obj = BoundaryBox(*boundary_box)
		if not boundary_box_obj:
			raise ValueError("Invalid boundary box.")
		if coordinates:
			logging.warning("Boundary box is explicitly specified. Coordinates are ignored.")

	elif coordinates:

		if len(coordinates) != 2:
			raise ValueError("Wrong coordinates format.")

		boundary_box_obj = BoundaryBox.from_coordinates(coordinates, configuration.zoom_level, *size)

	# Determine files.

	if not input_file_names and boundary_box_obj:
		cache_file_path: Path = (cache_path / f"{boundary_box_obj.get_format()}.osm")
		get_osm(boundary_box_obj, cache_file_path)
		input_file_names = [cache_file_path]
	else:
		logging.critical("Specify either --input, or --boundary-box, or --coordinates.")
		sys.exit(1)

	# Get OpenStreetMap data.

	assert input_file_names is not None

	osm_data: OSMData = OSMData()
	for input_file_name in input_file_names:
		if not input_file_name.is_file():
			raise ValueError(f"No such file: {input_file_name}.")

		if input_file_name.name.endswith(".json"):
			osm_data.parse_overpass(input_file_name)
		else:
			osm_data.parse_osm_file(input_file_name)

	if not boundary_box_obj:
		boundary_box_obj = osm_data.view_box
	if not boundary_box_obj:
		boundary_box_obj = osm_data.boundary_box

	assert boundary_box_obj is not None

	# Render the map.

	flinger: MercatorFlinger = MercatorFlinger(boundary_box_obj, zoom, osm_data.equator_length)
	svg: svgwrite.Drawing = svgwrite.Drawing(output_file_name, flinger.size)
	icon_extractor: ShapeExtractor = ShapeExtractor(workspace.ICONS_PATH, workspace.ICONS_CONFIG_PATH)

	constructor: Constructor = Constructor(
			osm_data=osm_data,
			flinger=flinger,
			extractor=icon_extractor,
			configuration=configuration,
			)
	constructor.construct()

	map_: Map = Map(flinger=flinger, svg=svg, configuration=configuration)
	map_.draw(constructor)

	logging.info(f"Writing output SVG to {output_file_name}...")
	with open(output_file_name, 'w', encoding="utf-8") as output_file:
		svg.write(output_file)
