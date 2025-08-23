#!/usr/bin/env python3
#
#  workspace.py
"""
File and directory path in the project.
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

__all__ = ["Workspace", "check_and_create"]

HERE: Path = Path(__file__).parent


def check_and_create(directory: Path) -> Path:
	"""Create directory if it doesn't exist and return it."""
	if not directory.is_dir():
		directory.mkdir(parents=True, exist_ok=True)
	return directory


class Workspace:
	"""Project file and directory paths and generated files and directories."""

	# Project directories and files, that are the part of the repository.

	SCHEME_PATH: Path = HERE / "scheme"
	DEFAULT_SCHEME_PATH: Path = SCHEME_PATH / "default.yml"
	ICONS_PATH: Path = HERE / "icons" / "icons.svg"
	ICONS_CONFIG_PATH: Path = HERE / "icons" / "config.json"
	ICONS_LICENSE_PATH: Path = HERE / "icons" / "LICENSE"

	DOCUMENTATION_PATH: Path = Path("doc")
	GRID_PATH: Path = DOCUMENTATION_PATH / "grid.svg"

	# Generated directories and files.

	MAPCSS_ICONS_DIRECTORY_NAME: str = "icons"

	def __init__(self, output_path: Path) -> None:
		self.output_path: Path = check_and_create(output_path)

		self._icons_by_id_path: Path = output_path / "icons_by_id"
		self._icons_by_name_path: Path = output_path / "icons_by_name"
		self._mapcss_path: Path = output_path / "map_machine_mapcss"
		self._tile_path: Path = output_path / "tiles"

	def find_scheme_path(self, identifier: str) -> Path:
		"""
		Find map scheme file by its identifier.

		:param identifier: scheme identifier or file path.
		:returns:
		  - default scheme file `default.yml` if identifier is not specified,
		  - `<identifier>.yml` from the default scheme directory (`scheme`) if
		    exists,
		  - path if identifier is a relative or absolute path to a scheme file.
		  - `None` otherwise.

		See `Scheme`.
		"""
		if not identifier:
			return self.DEFAULT_SCHEME_PATH

		path: Path = self.SCHEME_PATH / (identifier + ".yml")
		if path.is_file():
			return path

		path = Path(identifier)
		if path.is_file():
			return path

		raise FileNotFoundError(path.as_posix())

	def get_icons_by_id_path(self) -> Path:
		"""Directory for the icon files named by identifiers."""
		return check_and_create(self._icons_by_id_path)

	def get_icons_by_name_path(self) -> Path:
		"""Directory for the icon files named by human-readable names."""
		return check_and_create(self._icons_by_name_path)

	def get_tile_path(self) -> Path:
		"""Directory for tiles."""
		return check_and_create(self._tile_path)

	def get_mapcss_path(self) -> Path:
		"""Directory for MapCSS files."""
		return check_and_create(self._mapcss_path)

	def get_mapcss_file_path(self) -> Path:
		"""Directory for MapCSS files."""
		return self.get_mapcss_path() / "map_machine.mapcss"

	def get_mapcss_icons_path(self) -> Path:
		"""Directory for icons used by MapCSS file."""
		return check_and_create(self.get_mapcss_path() / self.MAPCSS_ICONS_DIRECTORY_NAME)

	def get_icon_grid_path(self) -> Path:
		"""Icon grid path."""
		return self.output_path / "icon_grid.svg"

	def get_taginfo_file_path(self) -> Path:
		"""Path to file with project information for Taginfo."""
		return self.output_path / "map_machine_taginfo.json"


workspace = Workspace(Path("out"))
