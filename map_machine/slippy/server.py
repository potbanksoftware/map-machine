#!/usr/bin/env python3
#
#  server.py
"""
Map Machine tile server for slippy maps.
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
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Optional

# 3rd party
import cairosvg  # type: ignore[import-untyped]

# this package
from map_machine.map_configuration import MapConfiguration
from map_machine.slippy.tile import Tile
from map_machine.workspace import workspace

__all__ = ["TileServerHandler", "run_server"]


class TileServerHandler(SimpleHTTPRequestHandler):
	"""HTTP request handler that process sloppy map tile requests."""

	cache: Path = Path("cache")
	update_cache: bool = False
	options: Optional[argparse.Namespace] = None

	def do_GET(self) -> None:
		"""Serve a GET request."""
		parts: list[str] = self.path.split('/')
		if not (len(parts) == 5 and not parts[0] and parts[1] == "tiles"):
			return

		zoom_level: int = int(parts[2])
		x: int = int(parts[3])
		y: int = int(parts[4])
		tile: Tile = Tile(x, y, zoom_level)
		tile_path: Path = workspace.get_tile_path()
		svg_path: Path = tile.get_file_name(tile_path)
		png_path: Path = svg_path.with_suffix(".png")

		if self.update_cache:
			if not png_path.exists():
				if not svg_path.exists():
					tile.draw(
							tile_path,
							self.cache,
							MapConfiguration(zoom_level=zoom_level),  # type: ignore[call-arg]
							)
				with svg_path.open(encoding="utf-8") as input_file:
					cairosvg.svg2png(file_obj=input_file, write_to=str(png_path))
				logging.info(f"SVG file is rasterized to {png_path}.")

		if png_path.exists():
			with png_path.open("rb") as input_file:
				self.send_response(200)
				self.send_header("Content-type", "image/png")
				self.end_headers()
				self.wfile.write(input_file.read())
				return


def run_server(options: argparse.Namespace) -> None:
	"""Command-line interface for tile server."""
	server: Optional[HTTPServer] = None
	try:
		handler = TileServerHandler
		handler.cache = Path(options.cache)
		handler.options = options
		server = HTTPServer(('', options.port), handler)
		logging.info(f"Server started on port {options.port}.")
		server.serve_forever()
	finally:
		if server:
			server.socket.close()
