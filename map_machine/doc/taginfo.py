#!/usr/bin/env python3
#
#  taginfo.py
"""
Creating Taginfo project file.

See https://wiki.openstreetmap.org/wiki/Taginfo/Projects
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
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# this package
from map_machine import __author__, __email__
from map_machine.scheme import Scheme
from map_machine.workspace import workspace

__all__ = ["TaginfoProjectFile", "write_taginfo_project_file"]


class TaginfoProjectFile:
	"""JSON structure with OpenStreetMap tag usage."""

	def __init__(self, path: Path, scheme: Scheme) -> None:
		self.path: Path = path

		self.structure: Dict[str, Any] = {
				"data_format": 1,
				"data_url": "https://github.com/potbanksoftware/map-machine/" + str(path),
				"data_updated": datetime.now().strftime("%Y%m%dT%H%M%SZ"),
				"project": {
						"name": "Map Machine",
						"description": "Map Machine is a Python OpenStreetMap renderer and tile generator.",
						"project_url": "https://github.com/potbanksoftware/map-machine",
						"icon_url": "http://enzet.ru/map-machine/image/logo.png",
						"contact_name": __author__,
						"contact_email": __email__,
						},
				"tags": [],
				}
		tags: list[dict[str, Any]] = self.structure["tags"]

		for matcher in scheme.node_matchers:
			if (
					not matcher.location_restrictions and matcher.shapes and len(matcher.tags) == 1
					and not matcher.add_shapes
					):
				key: str = list(matcher.tags.keys())[0]
				value: str = matcher.tags[key]
				ids: list[str] = [(shape if isinstance(shape, str) else shape["shape"]) for shape in matcher.shapes]
				icon_id: str = "___".join(ids)
				if value == '*':
					continue
				tag = {
						"key": key,
						"value": value,
						"object_types": ["node", "area"],
						"description": "Rendered",
						"icon_url": f"http://enzet.ru/map-machine/roentgen_icons_mapcss/{icon_id}.svg",
						}
				tags.append(tag)

	def write(self) -> None:
		"""Write Taginfo JSON file."""
		with self.path.open("w+", encoding="utf-8") as output_file:
			json.dump(self.structure, output_file, indent=4, sort_keys=True)


def write_taginfo_project_file(scheme: Scheme) -> None:
	"""Write Taginfo JSON file."""
	out_file: Path = workspace.get_taginfo_file_path()
	logging.info(f"Write Map Machine project file for Taginfo to {out_file}...")
	taginfo_project_file: TaginfoProjectFile = TaginfoProjectFile(out_file, scheme)
	taginfo_project_file.write()
