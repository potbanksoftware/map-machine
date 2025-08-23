"""
Tests for Map Machine project.
"""

# stdlib
import tempfile
from pathlib import Path

# this package
from map_machine.pictogram.icon import ShapeExtractor
from map_machine.scheme import Scheme
from map_machine.workspace import Workspace

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"

workspace: Workspace = Workspace(Path(tempfile.mkdtemp("map-machine")))

SCHEME: Scheme = Scheme.from_file(workspace.DEFAULT_SCHEME_PATH)
SHAPE_EXTRACTOR: ShapeExtractor = ShapeExtractor(workspace.ICONS_PATH, workspace.ICONS_CONFIG_PATH)
