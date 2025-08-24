#!/usr/bin/env python3
#
#  element.py
"""
Entry point for element drawing: nodes, ways, and relations.
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
from pathlib import Path

# this package
from map_machine.element.grid import Grid
from map_machine.osm.osm_reader import OSMNode, Tags

__all__ = ["draw_area", "draw_element", "draw_node", "draw_way"]


def draw_node(tags: Tags, path: Path) -> None:
	"""Draw separate node."""
	grid: Grid = Grid(show_credit=False, margin=7.5)
	grid.add_node(tags, 0, 0)
	grid.draw(path)


def draw_way(tags: Tags, path: Path) -> None:
	"""Draw way."""
	grid: Grid = Grid(show_credit=False, margin=3.5)
	node_1: OSMNode = grid.add_node({}, 0, 0)
	node_2: OSMNode = grid.add_node({}, 1, 1)
	grid.add_way(tags, [node_1, node_2])
	grid.draw(path)


def draw_area(tags: Tags, path: Path) -> None:
	"""Draw closed way that should be interpreted as an area."""
	grid: Grid = Grid(show_credit=False, margin=0.5)
	node: OSMNode = grid.add_node({}, 0, 0)
	nodes: list[OSMNode] = [
			node,
			grid.add_node({}, 0, 1),
			grid.add_node({}, 1, 1),
			grid.add_node({}, 1, 0),
			node,
			]
	grid.add_way(tags, nodes)
	grid.draw(path)


def draw_element(draw_type: str, tags: str, output_file: Path) -> None:
	"""Entry point for element drawing."""
	tags_description: Tags = {x.split('=')[0]: x.split('=')[1] for x in tags.split(',')}
	if draw_type == "node":
		draw_node(tags_description, Path(output_file))
	elif draw_type == "way":
		draw_way(tags_description, Path(output_file))
	elif draw_type == "area":
		draw_area(tags_description, Path(output_file))
	else:
		raise ValueError(f"Unknown element type `{draw_type}`, please choose from `node`, `way`, and `area`.")
