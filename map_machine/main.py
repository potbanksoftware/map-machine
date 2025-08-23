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
import argparse
import logging
import sys
from pathlib import Path

# this package
from map_machine.ui.cli import parse_arguments
from map_machine.workspace import Workspace

__all__ = ["main"]


def main() -> None:
	"""Map Machine command-line entry point."""
	# https://github.com/python/typeshed/issues/3049
	sys.stdin.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
	sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

	logging.basicConfig(format="%(levelname)s %(message)s", level=logging.INFO)
	workspace: Workspace = Workspace(Path("out"))

	arguments: argparse.Namespace = parse_arguments(sys.argv)

	if not arguments.command:
		logging.fatal("No command provided. See --help.")

	elif arguments.command == "render":
		# this package
		from map_machine import mapper

		mapper.render_map(arguments)

	elif arguments.command == "tile":
		# this package
		from map_machine.slippy import tile

		tile.generate_tiles(arguments)

	elif arguments.command == "icons":
		# this package
		from map_machine.pictogram.icon_collection import draw_icons

		draw_icons()

	elif arguments.command == "mapcss":
		# this package
		from map_machine import mapcss

		mapcss.generate_mapcss(arguments)

	elif arguments.command == "draw":
		# this package
		from map_machine.element.element import draw_element

		draw_element(arguments)

	elif arguments.command == "server":
		# this package
		from map_machine.slippy import server

		server.run_server(arguments)

	elif arguments.command == "taginfo":
		# this package
		from map_machine.doc.taginfo import write_taginfo_project_file
		from map_machine.scheme import Scheme

		write_taginfo_project_file(Scheme.from_file(workspace.DEFAULT_SCHEME_PATH))


if __name__ == "__main__":
	main()
