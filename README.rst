============
map-machine
============

.. start short_desc

**Map Machine is a Python OpenStreetMap renderer and tile generator.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/potbanksoftware/map-machine/workflows/Linux/badge.svg
	:target: https://github.com/potbanksoftware/map-machine/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/potbanksoftware/map-machine/workflows/Windows/badge.svg
	:target: https://github.com/potbanksoftware/map-machine/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/potbanksoftware/map-machine/workflows/macOS/badge.svg
	:target: https://github.com/potbanksoftware/map-machine/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/potbanksoftware/map-machine/workflows/Flake8/badge.svg
	:target: https://github.com/potbanksoftware/map-machine/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/potbanksoftware/map-machine/workflows/mypy/badge.svg
	:target: https://github.com/potbanksoftware/map-machine/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/potbanksoftware/map-machine/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/potbanksoftware/map-machine/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/potbanksoftware/map-machine/master?logo=coveralls
	:target: https://coveralls.io/github/potbanksoftware/map-machine?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/potbanksoftware/map-machine?logo=codefactor
	:target: https://www.codefactor.io/repository/github/potbanksoftware/map-machine
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/potbanksoftware/map-machine
	:target: https://github.com/potbanksoftware/map-machine/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/potbanksoftware/map-machine
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/potbanksoftware/map-machine/v0.1.9
	:target: https://github.com/potbanksoftware/map-machine/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/potbanksoftware/map-machine
	:target: https://github.com/potbanksoftware/map-machine/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. end shields


The **Map Machine** project consists of


  * a Python OpenStreetMap_ renderer:

    * SVG map generation,
    * SVG and PNG tile generation,

  * the Röntgen icon set: unique CC-BY 4.0 map icons.

.. _OpenStreetMap: http://openstreetmap.org

The idea behind the Map Machine project is to **show all the richness of the OpenStreetMap data**: to have a possibility to display any map feature represented by OpenStreetMap data tags by means of colors, shapes, and icons. Map Machine is created both for map contributors: to display all changes one made on the map even if they are small, and for map users: to dig down into the map and find every detail that was mapped.

Unlike standard OpenStreetMap layers, **Map Machine is a playground for experiments** where one can easily try to support any unsupported tag, proposed tagging scheme, tags with little or even single usage, deprecated ones that are still in use.

Map Machine is intended to be highly configurable, so it can generate precise but messy maps for OSM contributors as well as pretty and clean maps for OSM users. It can also use some slow algorithms for experimental features.


Usage example
-------------

.. code-block:: shell

	map-machine render -b 2.284,48.860,2.290,48.865

will automatically download OSM data and render an SVG map of the specified area to ``out/map.svg``.

.. code-block:: shell

	map-machine tile -b 2.361,48.871,2.368,48.875

will automatically download OSM data and render PNG tiles that cover the specified area to the ``out/tiles`` directory.


Röntgen icon set
----------------

The central feature of the project is the Röntgen icon set.
It is a set of monochrome 14 × 14 px pixel-aligned icons specially created for the Map Machine project.
Unlike the Map Machine source code, which is under the MIT license,
all icons are under the `CC BY <http://creativecommons.org/licenses/by/4.0/>`_ license.
So, with the appropriate credit the icon set can be used outside the project.
Some icons can be used as emoji symbols.

All icons tend to support a common design style, which is heavily inspired by Maki_, Osmic_, and Temaki_.

.. _Maki: https://github.com/mapbox/maki
.. _Osmic: https://github.com/gmgeo/osmic
.. _Temaki: https://github.com/ideditor/temaki

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/grid.svg
	:alt: Icons

Generate an icon grid and sets of individual icons with ``map-machine icons``.
It will update the ``doc/grid.svg`` file, and create SVG files in the ``out/icons_by_id`` directory
where files are named using shape identifiers (e.g. ``power_tower_portal_2_level.svg``)
and in the ``icons_by_name`` directory where files are named using shape names (e.g. ``Röntgen portal two-level transmission tower.svg``).


Map features
------------

Extra icons
************

Map Machine uses icons to visualize tags for nodes and areas.
But unlike other renderers, Map Machine can use more than one icon to visualize an entity and can use colors to visualize
`colour <https://wiki.openstreetmap.org/wiki/Key:colour>`_ value or other entity properties
(like `material <https://wiki.openstreetmap.org/wiki/Key:material>`_ or `genus <https://wiki.openstreetmap.org/wiki/Key:genus>`_).

Isometric building shapes
**************************

With ``--buildings isometric`` or ``--buildings isometric-no-parts`` (not set by default),
buildings are drawn using isometric shapes for walls and shade in proportion to
`building:levels <https://wiki.openstreetmap.org/wiki/Key:building:levels>`_,
`building:min_level <https://wiki.openstreetmap.org/wiki/Key:building:min_level>`_,
`height <https://wiki.openstreetmap.org/wiki/Key:height>`_,
and `min_height <https://wiki.openstreetmap.org/wiki/Key:min_height>`_ values.

Example
^^^^^^^^

.. code-block:: bash

	map-machine render -c -26.19049,28.05605 -s 600,400 --buildings isometric

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/buildings.svg
	:alt: 3D buildings


Road lanes
***********

To determine the road width Map Machine uses the `width <https://wiki.openstreetmap.org/wiki/Key:width>`_ tag value
or estimates it based on the `lanes <https://wiki.openstreetmap.org/wiki/Key:lanes>`_ value.
If lane value is specified, it also draws lane separators.
This map style is highly inspired by Christoph Hormann's post `Navigating the Maze <http://blog.imagico.de/navigating-the-maze-part-2/>`_.

Example
^^^^^^^^

.. code-block:: shell

	map-machine render -c 47.61224,-122.33866 -s 600,400

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/lanes.svg
	:alt: Road Lanes

Trees
******

Visualization of tree leaf types (broadleaved or needle-leaved) and genus or taxon by means of icon shapes and leaf cycles (deciduous or evergreen) by means of color.

Example
^^^^^^^^

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/trees.svg
	:alt: Trees


Viewpoint and camera direction
********************************

`direction <https://wiki.openstreetmap.org/wiki/Key:direction>`_
tag values for `tourism <https://wiki.openstreetmap.org/wiki/Key:tourism>`_
= `viewpoint <https://wiki.openstreetmap.org/wiki/Tag:tourism=viewpoint>`_
and `camera:direction <https://wiki.openstreetmap.org/wiki/Key:camera:direction>`_
for `man_made <https://wiki.openstreetmap.org/wiki/Key:man_made>`_
= `surveillance <https://wiki.openstreetmap.org/wiki/Tag:man_made=surveillance>`_
are rendered with sectors displaying the direction and angle (15º if angle is not specified)
or the whole circle for panorama view. Radial gradient is used for surveillance
and inverted radial gradient is used for viewpoints.


Example
^^^^^^^^

.. code-block:: shell

	map-machine render -c 52.50892,13.3244 -s 600,400 -z 18.5


.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/surveillance.svg
	:alt: Surveillance


.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/viewpoints.svg
	:alt: Viewpoints


Power tower design
*******************

Visualize `design <https://wiki.openstreetmap.org/wiki/Key:design>`_
values used with `power <https://wiki.openstreetmap.org/wiki/Key:power>`_
= `tower <https://wiki.openstreetmap.org/wiki/Tag:power=tower>`_
and `power <https://wiki.openstreetmap.org/wiki/Key:power>`_
= `pole <https://wiki.openstreetmap.org/wiki/Tag:power=pole>`_
tags. ``design`` has more than 1 million usages in OpenStreetMap.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/icons_power.svg
	:alt: Power tower design

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/power.svg
	:alt: Power tower design


Colors
*******

Map icons have `colour <https://wiki.openstreetmap.org/wiki/Key:colour>`_ tag value if it is present,
otherwise, icons are displayed with dark grey color by default, purple color for shop nodes,
red color for emergency features, and special colors for natural features.
Map Machine also takes into account
`building:colour <https://wiki.openstreetmap.org/wiki/Key:building:colour>`_,
`roof:colour <https://wiki.openstreetmap.org/wiki/Key:roof:colour>`_ and other ``*:colour`` tags,
and uses the `colour <https://wiki.openstreetmap.org/wiki/Key:colour>`_ tag value to paint subway lines.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/colors.svg
	:alt: Building colors


Emergency
************

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/icons_emergency.svg
	:alt: Emergency


Japanese map symbols
*********************

Japanese maps usually use `special symbols <https://en.wikipedia.org/wiki/List_of_Japanese_map_symbols>`_
called *chizukigou* (地図記号) which are different from standard map symbols used in other countries.
They can be enabled with ``--country jp`` option.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/icons_japanese.svg
	:alt: Japanese map symbols


Indoor features
*****************

Draw indoor features specifying level with ``--level`` option.
Possible values are numbers (e.g. ``1``, ``0.5``), lists of number separated by ``;`` (e.g. ``1;2;4;4.5``),
``all``, ``overground``, and ``underground``. The default value is not ``all``, but ``overground``,
so underground objects are not shown on the map if ``--level`` option is not specified.


Example
^^^^^^^^

.. code-block:: shell

	map-machine render -c 4.5978,-74.07507 -s 600,400 -z 19.5 --level 0

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/indoor.svg
	:alt: Indoor


Shape combination
**********************

One of the key features of Map Machine is constructing icons from several shapes.


Masts
^^^^^^^^

For `man_made <https://wiki.openstreetmap.org/wiki/Key:man_made>`_ = `mast <https://wiki.openstreetmap.org/wiki/Tag:man_made=mast>`_
distinguish types (communication, lighting, monitoring, and siren) and construction (freestanding or lattice, and using of guys) are rendered by combining 7 unique icon shapes.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/mast.svg
	:alt: Mast types


Volcanoes
^^^^^^^^

For `natural <https://wiki.openstreetmap.org/wiki/Key:natural>`_ = `volcano <https://wiki.openstreetmap.org/wiki/Tag:natural=volcano>`_
status (active, dormant, extinct, or unspecified) and type (stratovolcano, shield, or scoria) are rendered by combining 7 unique icon shapes.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/volcano.svg
	:alt: Volcano types

Wireframe view
--------------

Creation time mode
*******************

Visualize element creation time with ``--mode time``.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/time.svg
	:alt: Creation time mode

Author mode
*************

Every way and node displayed with the random color picked for each author with ``--mode author``.

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/author.svg
	:alt: Author mode



Map generation
--------------

The ``render`` command is used to generate an SVG map from OpenStreetMap data. You can run it using:

.. code-block:: shell

	map-machine render \
		-b <min longitude>,<min latitude>,<max longitude>,<max latitude> \
		-o <output file name> \
		-z <OSM zoom level> \
		<other arguments>


Example
****************

.. code-block:: shell

	map-machine render \
		--boundary-box 2.284,48.860,2.290,48.865 \
		--output out/esplanade_du_trocadéro.svg

will download OSM data to ``cache/2.284,48.860,2.290,48.865.osm`` and render an SVG map of the specified area to ``out/esplanade_du_trocadéro.svg``.


Arguments
****************

* ``-i``, ``--input`` ``<path>`` -- input XML file name or names (if not specified, file will be downloaded using the OpenStreetMap API)
* ``-o``, ``--output`` ``<path>`` -- output SVG file name, default value: ``out/map.svg``
* ``-b``, ``--boundary-box`` ``<lon1>,<lat1>,<lon2>,<lat2>`` -- geo boundary box
* ``--cache`` ``<path>`` -- path for temporary OSM files, default value: ``cache``
* ``-z``, ``--zoom`` ``<float>`` -- OSM zoom level, default value: 18.0
* ``-c``, ``--coordinates`` ``<latitude>,<longitude>`` -- coordinates of any location inside the tile
* ``-s``, ``--size`` ``<width>,<height>`` -- resulted image size

plus standard map configuration options.


Tile generation
---------------

Command ``tile`` is used to generate PNG tiles for `slippy maps <https://wiki.openstreetmap.org/wiki/Slippy_Map>`_.
To use them, run Map Machine's tile server.

* ``-c``, ``--coordinates`` ``<latitude>,<longitude>`` -- coordinates of any location inside the tile
* ``-t``, ``--tile`` ``<zoom level>/<x>/<y>`` -- tile specification
* ``--cache`` ``<path>`` -- path for temporary OSM files, default value: ``cache``
* ``-b``, ``--boundary-box`` ``<lon1>,<lat1>,<lon2>,<lat2>`` -- construct the minimum amount of tiles that cover the requested boundary box
* ``-z``, ``--zoom`` ``<range>`` -- OSM zoom levels; can be list of numbers or ranges, e.g. ``16-18``, ``16,17,18``, or ``16,18-20``, default value: ``18``
* ``-i``, ``--input`` ``<path>`` -- input OSM XML file name (if not specified, the file will be downloaded using the OpenStreetMap API)

plus standard map configuration options.


Generate one tile
******************

Specify the tile coordinates:

.. code-block:: shell

	map-machine tile --tile <OSM zoom level>/<x>/<y>

or specify any geographical coordinates inside a tile:

.. code-block:: shell

	map-machine tile \
		--coordinates <latitude>,<longitude> \
		--zoom <OSM zoom levels>


The tile will be stored as an SVG file ``out/tiles/tile_<zoom level>_<x>_<y>.svg``
and a PNG file ``out/tiles/tile_<zoom level>_<x>_<y>.svg``,
where ``x`` and ``y`` are tile coordinates.
The ``--zoom`` option will be ignored if it is used with the ``--tile`` option.

Example:

.. code-block:: shell

	map-machine tile -c 55.7510637,37.6270761 -z 18


will generate an SVG file ``out/tiles/tile_18_158471_81953.svg`` and a PNG file ``out/tiles/tile_18_158471_81953.png``.


Generate a set of tiles
************************

Specify the boundary box to get the minimal set of tiles that covers the area:

.. code-block:: shell

	map-machine tile \
		--boundary-box <min longitude>,<min latitude>,<max longitude>,<max latitude> \
		--zoom <OSM zoom levels>


The boundary box will be extended to the boundaries of the minimal tileset that covers the area, then it will be extended a bit more to avoid some artifacts on the edges rounded to 3 digits after the decimal point. The map with the new boundary box coordinates will be written to the cache directory as SVG and PNG files. All tiles will be stored as SVG files ``out/tiles/tile_<zoom level>_<x>_<y>.svg`` and PNG files ``out/tiles/tile_<zoom level>_<x>_<y>.svg``, where ``x`` and ``y`` are tile coordinates.

Example:

.. code-block:: shell

	map-machine tile -b 2.361,48.871,2.368,48.875


will generate 36 PNG tiles at zoom level 18 from tile 18/132791/90164 all the way to 18/132796/90169 and two cached files ``cache/2.360,48.869,2.370,48.877_18.svg`` and ``cache/2.360,48.869,2.370,48.877_18.png``.


Tile server
-----------

The ``server`` command is used to run a tile server for slippy maps.

.. code-block:: shell

	map-machine server


Stop server interrupting the process with ``Ctrl`` + ``C``.

* ``--cache`` ``<path>`` -- path for temporary OSM files, default value: ``cache``
* ``--port`` ``<integer>`` -- port number, default value: 8080


Example
****************

Create a minimal amount of tiles that cover specified boundary box for zoom levels 16, 17, 18, and 19:

.. code-block:: shell

	map-machine tile -b 2.364,48.854,2.367,48.857 -z 16-19


Run tile server on 127.0.0.1:8080:

.. code-block:: shell

	map-machine server


Use JavaScript code for `Leaflet <https://leafletjs.com/>`_:

.. code-block:: javascript

	var map = L.map('mapid').setView([48.8555, 2.3655], 18);

	L.tileLayer('http://127.0.0.1:8080/tiles/{z}/{x}/{y}', {
		maxZoom: 19,
		attribution: 'Map data &copy; ' +
			'<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> ' +
			'contributors, imagery &copy; ' +
			'<a href="https:/github.com/enzet/map-machine">Map Machine</a>',
		id: 'map_machine',
		tileSize: 256,
		zoomOffset: 0
	}).addTo(map);


HTML code:

.. code-block:: html

	<div id="mapid" style="width: 1000px; height: 600px;"></div>


Map options
-----------

Map configuration options used by ``render`` and ``tile`` commands:

* ``--scheme`` ``<id> or <path>`` -- scheme identifier (look for ``<id>.yml`` file) or path to a YAML scheme file, default value: ``default``
* ``--buildings`` ``<mode>`` -- building drawing mode: no, flat, isometric, isometric-no-parts, default value: ``flat``
* ``--mode`` ``<string>`` -- map drawing mode: normal, author, time, white, black, default value: ``normal``
* ``--overlap`` ``<integer>`` -- how many pixels should be left around icons and text, default value: 12
* ``--labels`` ``<string>`` -- label drawing mode: no, main, all, address, default value: ``main``
* ``--level`` -- display only this floor level, default value: ``overground``
* ``--seed`` ``<string>`` -- seed for random
* ``--tooltips`` -- add tooltips with tags for icons in SVG files
* ``--country`` -- two-letter code (ISO 3166-1 alpha-2) of country, that should be used for location restrictions, default value: ``world``
* ``--ignore-level-matching`` -- draw all map features ignoring the current level
* ``--roofs`` -- draw building roofs, set by default
* ``--building-colors`` -- paint walls (if isometric mode is enabled) and roofs with specified colors
* ``--show-overlapped`` -- show hidden nodes with a dot


MapCSS 0.2 generation
---------------------

The ``mapcss`` command can be used to generate a MapCSS scheme.
``map-machine mapcss`` will create an ``out/map_machine_mapcss``
directory with simple MapCSS 0.2 scheme adding icons from the Röntgen icon set
to nodes and areas: ``.mapcss`` file and directory with icons.

To create a MapCSS style with Map Machine style also for ways and relations, run ``map-machine mapcss --ways``.

* ``--icons`` -- add icons for nodes and areas, set by default
* ``--ways`` -- add style for ways and relations
* ``--lifecycle`` -- add icons for lifecycle tags; be careful: this will increase the number of node and area selectors by 9 times, set by default


Use Röntgen as JOSM map paint style
***************************************

  * Run ``map-machine mapcss``.
  * Open `JOSM <https://josm.openstreetmap.de/>`_.
  * Go to ``Preferences`` → Third tab on the left → ``Map Paint Styles``.
  * Active styles: press ``+``.
  * URL / File: set path to ``out/map_machine_mapcss/map_machine.mapcss``.

To enable/disable the Map Machine map paint style go to ``View`` → ``Map Paint Styles`` → ``Map Machine``.


Example
^^^^^^^^

.. image:: https://raw.githubusercontent.com/potbanksoftware/map-machine/refs/heads/main/doc/josm.png
	:alt: JOSM example

Example of using Röntgen icons on top of the Mapnik style in JOSM. Map Paint Styles look like this:

  * ✓ Mapnik (true)
  * ✓ Map Machine


Installation
--------------


First install the `cairo 2D graphic library <https://www.cairographics.org/download/>`_,
and the `GEOS library <https://libgeos.org>`_.

.. start installation

``map-machine`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/potbanksoftware/map-machine

.. end installation
