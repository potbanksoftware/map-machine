#!/usr/bin/env python3
#
#  main.py
"""
Map Machine entry point.
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
from typing import Callable, Optional

# 3rd party
import click
from consolekit import __version__, click_group
from consolekit.options import _C, flag_option

# this package
from map_machine.geometry.boundary_box import LATITUDE_MAX_DIFFERENCE, LONGITUDE_MAX_DIFFERENCE
from map_machine.map_configuration import BuildingMode, DrawingMode, LabelMode
from map_machine.mapper import DEFAULT_SIZE
from map_machine.osm.osm_reader import STAGES_OF_DECAY

__all__ = ["main"]

RENDER_INPUT_HELP = "input XML file name or names (if not specified, file will be downloaded using the OpenStreetMap API)"
LIFECYCLE_HELP = f"add icons for lifecycle tags; be careful: this will increase the number of node and area selectors by {len(STAGES_OF_DECAY) + 1} times"


class BoundaryBox(click.ParamType):

	def get_metavar(self, *args, **kwargs) -> str:
		return "<LON1,LAT1,LON2,LAT2>"

	def convert(
			self,
			value: str,
			param: Optional[click.Parameter],
			ctx: Optional[click.Context],
			) -> tuple[float, float, float, float]:
		value = super().convert(value, param, ctx)
		boundary_box = []
		elems = value.split(',')

		if len(elems) != 4:
			self.fail(value + (" (expected 4 values)"), param, ctx)

		for elem in elems:
			try:
				boundary_box.append(float(elem))
			except ValueError:
				self.fail(value, param, ctx)

		left, bottom, right, top = boundary_box

		if left >= right:
			raise ValueError("Negative horizontal boundary.")
		if bottom >= top:
			raise ValueError("Negative vertical boundary.")
		if (right - left > LONGITUDE_MAX_DIFFERENCE or top - bottom > LATITUDE_MAX_DIFFERENCE):
			raise ValueError("Boundary box is too big.")

		return tuple(boundary_box)  # type: ignore[return-value]


class Coordinates(click.ParamType):

	def get_metavar(self, *args, **kwargs) -> str:
		return "<LATITUDE,LONGITUDE>"

	def convert(
			self,
			value: str,
			param: Optional[click.Parameter],
			ctx: Optional[click.Context],
			) -> tuple[float, float]:
		value = super().convert(value, param, ctx)
		boundary_box = []
		elems = value.split(',')
		if len(elems) != 2:
			self.fail(value + (" (expected 2 values)"), param, ctx)

		for elem in elems:
			try:
				boundary_box.append(float(elem))
			except ValueError:
				self.fail(value, param, ctx)

		return tuple(boundary_box)  # type: ignore[return-value]


class Size(click.ParamType):

	def get_metavar(self, *args, **kwargs) -> str:
		return "<WIDTH,HEIGHT>"

	def convert(
			self,
			value: str,
			param: Optional[click.Parameter],
			ctx: Optional[click.Context],
			) -> tuple[float, float]:
		value = super().convert(value, param, ctx)
		boundary_box = []
		elems = value.split(',')
		if len(elems) != 2:
			self.fail(value + (" (expected 2 values)"), param, ctx)

		for elem in elems:
			try:
				boundary_box.append(float(elem))
			except ValueError:
				self.fail(value, param, ctx)

		return tuple(boundary_box)  # type: ignore[return-value]


@click.version_option(__version__, prog_name="Map Machine")
@click_group()
def main() -> None:
	"""
	Map Machine, OpenStreetMap renderer and tile generator.
	"""

	# https://github.com/python/typeshed/issues/3049
	sys.stdin.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
	sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

	logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)


def cache_option() -> Callable[[_C], _C]:
	return click.option(
			"--cache",
			help="path for temporary OSM files",
			type=click.Path(file_okay=False),
			default="cache",
			)


def common_map_options(f: _C) -> _C:
	click.option(
			"--scheme",
			metavar="<id> or <path>",
			default="default",
			help="scheme identifier (look for `<id>.yml` file) or path to a YAML scheme file",
			)(
					f
					)
	click.option(
			"--buildings",
			metavar="<mode>",
			default=BuildingMode.FLAT,
			type=click.Choice(BuildingMode),  # type: ignore[arg-type]
			help="Building drawing mode",
			)(
					f
					)
	click.option(
			"--mode",
			default=DrawingMode.NORMAL,
			metavar="<string>",
			type=click.Choice(DrawingMode),  # type: ignore[arg-type]
			help="Map drawing mode",
			)(
					f
					)
	click.option(
			"--overlap",
			default=12,
			type=int,
			help="how many pixels should be left around icons and text",
			)(
					f
					)
	click.option(
			"--labels",
			"label_mode",
			default=LabelMode.MAIN,
			metavar="<string>",
			type=click.Choice(LabelMode),  # type: ignore[arg-type]
			help="Label drawing mode",
			)(
					f
					)
	click.option(
			"--level",
			default="overground",
			help="display only this floor level",
			)(
					f
					)
	click.option(
			"--seed",
			default='',
			help="seed for random",
			metavar="<string>",
			)(
					f
					)
	click.option(
			"--country",
			help="two-letter code (ISO 3166-1 alpha-2) of country, that should be used for location restrictions",
			default="world",
			)(
					f
					)
	flag_option(
			"--tooltips",
			help="add tooltips with tags for icons in SVG files",
			)(
					f
					)

	flag_option(
			"--ignore-level-matching",
			help="draw all map features ignoring the current level",
			)(
					f
					)
	flag_option(
			"--roofs/--no-roofs",
			help="draw building roofs",
			default=True,
			)(
					f
					)
	flag_option(
			"--building-colors",
			help="paint walls (if isometric mode is enabled) and roofs with "
			"specified colors",
			)(
					f
					)
	flag_option(
			"--show-overlapped",
			help="show hidden nodes with a dot",
			)(
					f
					)
	flag_option(
			"--hide-credit",
			help="hide credit",
			)(
					f
					)

	return f


@common_map_options
@cache_option()
@click.option(
		"-s",
		"--size",
		type=Size(),
		default=','.join(map(str, DEFAULT_SIZE)),
		help="resulted image size",
		)
@click.option(
		"-c",
		"--coordinates",
		type=Coordinates(),
		help="coordinates of any location inside the tile",
		)
@click.option(
		"-z",
		"--zoom",
		type=float,
		help="OSM zoom level",
		default=18.0,
		)
@click.option(
		"-b",
		"--boundary-box",
		type=BoundaryBox(),
		help="geo boundary box",
		)
@click.option(
		"-o",
		"--output",
		"output_file_name",
		type=click.Path(exists=False, dir_okay=False),
		default="out/map.svg",
		help="output SVG file name",
		)
@click.option(
		"-i",
		"--input",
		"input_file_names",
		type=click.Path(dir_okay=False),
		multiple=True,
		help=RENDER_INPUT_HELP,
		)
@main.command()
def render(
		input_file_names: list[str],
		output_file_name: str,
		boundary_box: tuple[float, float, float, float],
		zoom: float,
		coordinates: tuple[float, float],
		size: tuple[float, float],
		scheme: str,
		cache: str,
		buildings: BuildingMode,
		mode: DrawingMode,
		overlap: int,
		label_mode: LabelMode,
		level: str,
		seed: str,
		country: str,
		tooltips: bool,
		ignore_level_matching: bool,
		roofs: bool,
		building_colors: bool,
		show_overlapped: bool,
		hide_credit: bool,
		) -> None:
	"""
	Render an area of OpenStreetMap as SVG.

	Use --boundary-box to specify geo boundaries,
	--input to specify OSM XML or JSON input file,
	or --coordinates and --size to specify central point and resulting image size.
	"""

	# this package
	from map_machine import mapper
	mapper.render_map(
			input_file_names=list(map(Path, input_file_names)),
			output_file_name=output_file_name,
			boundary_box=boundary_box,
			zoom=zoom,
			coordinates=coordinates,
			size=size,
			scheme=scheme,
			cache=cache,
			building_mode=buildings,
			drawing_mode=mode,
			overlap=overlap,
			label_mode=label_mode,
			level=level,
			seed=seed,
			country=country,
			show_tooltips=tooltips,
			ignore_level_matching=ignore_level_matching,
			draw_roofs=roofs,
			use_building_colors=building_colors,
			show_overlapped=show_overlapped,
			hide_credit=hide_credit,
			)


@common_map_options
@cache_option()
@click.option(
		"-t",
		"--tile",
		metavar="<zoom level>/<x>/<y>",
		help="tile specification",
		)
@click.option(
		"-c",
		"--coordinates",
		type=Coordinates(),
		help="coordinates of any location inside the tile",
		)
@click.option(
		"-z",
		"--zoom",
		type=str,
		metavar="<range>",
		help="OSM zoom levels; can be list of numbers or ranges, e.g. `16-18`, "
		"`16,17,18`, or `16,18-20`",
		default="18",
		)
@click.option(
		"-b",
		"--boundary-box",
		type=BoundaryBox(),
		help="construct the minimum amount of tiles that cover the requested boundary box",
		)
@click.option(
		"-i",
		"--input",
		"input_file_name",
		type=click.Path(dir_okay=False),
		help="input XML file name (if not specified, file will be downloaded using the OpenStreetMap API)",
		)
@main.command(help="Generate SVG and PNG tiles for slippy maps")
def tile(
		input_file_name: Optional[str],
		boundary_box: tuple[float, float, float, float],
		zoom: str,
		coordinates: tuple[float, float],
		tile: tuple[int, float, float],
		cache: str,
		scheme: str,
		buildings: BuildingMode,
		mode: DrawingMode,
		overlap: int,
		label_mode: LabelMode,
		level: str,
		seed: str,
		country: str,
		tooltips: bool,
		ignore_level_matching: bool,
		roofs: bool,
		building_colors: bool,
		show_overlapped: bool,
		hide_credit: bool,
		) -> None:
	"""
	Generate SVG and PNG 256 × 256 px tiles for slippy maps.

	You can use server command to run server in order to display generated tiles as a map (e.g. with Leaflet).
	"""
	# this package
	from map_machine.slippy.tile import generate_tiles

	if input_file_name:
		input_file = Path(input_file_name)
	else:
		input_file = None

	generate_tiles(
			input_file_name=input_file,
			boundary_box=boundary_box,
			zoom=zoom,
			coordinates=coordinates,
			tile=tile,
			cache=cache,
			scheme=scheme,
			building_mode=buildings,
			drawing_mode=mode,
			overlap=overlap,
			label_mode=label_mode,
			level=level,
			seed=seed,
			country=country,
			show_tooltips=tooltips,
			ignore_level_matching=ignore_level_matching,
			draw_roofs=roofs,
			use_building_colors=building_colors,
			show_overlapped=show_overlapped,
			hide_credit=hide_credit,
			)


@main.command()
def icons() -> None:
	"""
	Generate Röntgen icons as a grid and as separate SVG icons.
	"""

	# this package
	from map_machine.pictogram.icon_collection import draw_icons

	draw_icons()


@flag_option(
		"--lifecycle/--no-lifecycle",
		help=LIFECYCLE_HELP,
		)
@flag_option(
		"--ways",
		help="add style for ways and relations",
		)
@flag_option(
		"--icons/--no-icons",
		help="add icons for nodes and areas",
		)
@main.command()
def mapcss(icons: bool, ways: bool, lifecycle: bool) -> None:
	"""
	Write directory with MapCSS file and generated Röntgen icons.
	"""

	# this package
	from map_machine import mapcss

	mapcss.generate_mapcss(icons, ways, lifecycle)


@click.option("-o", "--output-file", default="out/element.svg")
@click.argument("tags")
@click.argument("draw_type", metavar="TYPE")
@main.command()
def draw(draw_type: str, tags: str, output_file: str) -> None:
	"""
	Draw map element separately.
	"""

	# this package
	from map_machine.element.element import draw_element

	draw_element(draw_type, tags, Path(output_file))


@cache_option()
@click.option(
		"--port",
		help="port number",
		default=8080,
		type=int,
		)
@main.command(help="Run tile server")
def server(port: int, cache: str) -> None:
	"""
	Run server to display generated tiles as a map (e.g. with Leaflet).
	"""
	# this package
	from map_machine.slippy import server

	server.run_server(port=port, cache=cache)


@main.command()
def taginfo() -> None:
	"""
	Generate JSON file for Taginfo project.
	"""

	# this package
	from map_machine.doc.taginfo import write_taginfo_project_file
	from map_machine.scheme import Scheme
	from map_machine.workspace import Workspace

	workspace: Workspace = Workspace(Path("out"))

	write_taginfo_project_file(Scheme.from_file(workspace.DEFAULT_SCHEME_PATH))


if __name__ == "__main__":
	main()
