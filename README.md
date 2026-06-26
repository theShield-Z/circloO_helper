## Contents
- Basics
  - [Setup](#setup)
  - [Basic Workflow](#basic-workflow)
- Feature Overviews
  - [Levels](#levels)
  - [Objects](#objects)
    - [Shapes](#shapes)
    - [Types](#types)
  - [Custom Objects](#custom-objects)
    - [Creating Custom Objects](#creating-custom-objects)
  - [Tools](#tools)
  - [Pixel Builder](#pixel-builder)
  - [Text Conversion](#text-conversion)
  - [Image Conversion (raster)](#image-conversion-raster)
  - [Video Conversion](#video-conversion)
  - [Dithering Module](#dithering)
  - [Image Conversion (vector)](#image-conversion-vector)
  - [Audio/MIDI Conversion](#audio-midi-conversion)
  - [Point Plotter](#point-plotter)
- [API](#api)
  - [Level](#level)
    - [Level Parsers](#level-parsers)
  - [Object](#object)
    - [Object Shapes](#object-shapes)
    - [Object Types](#object-types)
  - [All Objects](#objects-1)
    - [Solid Objects](#solid-objects)
    - [Lines](#lines)
    - [Growing Objects](#growing-objects)
    - [Moveable Objects](#moveable-objects)
    - [Special/Other Objects](#special-objects)
    - [Generators](#generators)
    - [Connections](#connections)
    - [Collectables](#collectables)
  - [Custom Object](#custom-object)
    - [Included Custom Objects](#included-custom-objects)
  - [Tools](#tools)
  - Converters
    - [Pixel Builder](#pixel-builder-1)
    - [Text](#text)
    - [Point Plotter](#plotter)
    - [CHImage](#chimage)
    - [CHVideo](#chvideo)
    - [CHSVG](#chsvg)
    - [CHMIDI](#chmidi)
    - [Dithering Module](#dithering-1)
- [To-Do & Known Issues](#to-do--known-issues)

<hr>


# [circloO Helper](https://github.com/theShield-Z/circloO_helper)

circloO Helper is a Python library for creating and editing levels for the physics platformer game [*circloO*](https://store.steampowered.com/app/2195630/circloO/). It supports procedural level generation, level parsing, custom composite objects, and conversion from text, image, videos, SVGs, and MIDI files.


## Main Features

- Creation and editing of levels and objects
- Full documentation of level and object attributes
- Video, Image (both raster & vector), and Text conversion
- Custom objects (this is a really cool one)
- Several miscellaneous tools


## Setup

This library was built and tested with Python 3.13 on Windows 10, but most features should still work with any modern Python version and OS.

Install with pip:
```commandline
pip install circloo-helper
```

You can alternatively download the source from [GitHub](https://github.com/theShield-Z/circloO_helper), navigate to the directory that contains `setup.py`, and run:
```commandline
pip install .
```

See the examples contained in [`examples/main.py`](https://github.com/theShield-Z/circloO_helper/tree/main/examples) for basic usage of most features.

### Dependencies

- numpy
- Pillow (image conversion)
- imageio & imageio-ffmpeg (video conversion)
- svgpathtools-light (svg conversion)
- mido (midi conversion)
- pyperclip (reading/writing levels to clipboard)
- numba (rectangle reduction algorithm speed)
- tripy (polygon triangulation)

All dependencies are installed automatically via pip.


## Basic Workflow

```python
# Import the library.
import circloo_helper as ch
from circloo_helper.circloo_objects import *

# Create a level.
lvl = ch.Level(segments=1, color=160)
# # You can also parse an existing level: 
# ch.parse(text)            # for strings
# ch.read_file(filepath)    # for files
# ch.read_clipboard()       # for levels exported to clipboard

# Create objects.
c = SolidCircle(1400, 1500, 30)
r = SolidRectangle(1575, 1520, 50, 50, -10)
t = SolidTriangle(1563, 1365, 1575, 1430, 1515, 1410)
plr = Player(1500, 1650)

# Add objects to the level.
lvl.add(c)
lvl.add(r)
lvl.add(t)
lvl.add(plr)

# Export the level.
print(lvl.to_clipboard())   # or simply print(lvl) or lvl.to_clipboard()
lvl.to_file("my_circloO_level.txt")
```


## Levels

Create a level by calling `ch.Level()`. You can see the full API [here](#level), but the most important Level attributes are `color`, `segments`, and `grav_scale`, which determine the level's color, the number of segments, and the gravity strength respectively. 

To add an object `obj` to a Level `lvl`, use `lvl.add(obj)`. Once you have finished programming your level, you can export to your clipboard, as a file, or simply print it to the terminal.

Existing levels created in-game can also be parsed and edited with this library. Use `parse()` to parse strings. Use `read_file()` to parse a file from a file path. Use `read_clipboard()` to parse a level from your clipboard (used in conjunction with the in-game Copy to Clipboard button).


## Objects

Objects are composed from two indepentend hierarchies:
- `ObjectShape`: Shape determines geometry (Circle, Rectangle, Triangle, etc.)
- `ObjectType`: Type determines physics behavior (Solid, Moveable, Generator, etc.)

For example, `MoveableCircle` combines the `Circle` shape with the `Moveable` type. All circloO Objects inherit from `ObjectShape`, but `ObjectType` is optional. Objects may also inherit more than one Type

See [Objects](#objects-1) for a list of all supported Objects and their attributes.

### Shapes

Object shapes represent the shape or category of an object. Shapes include:
- `Circle`
  - Circles have coordinates and a radius
- `Rectangle`
  - Rectangles have coordinates, a width, and a height
- `Triangle`
  - Triangles have coordinates
- `Line`
  - Lines have a thickness
- `Connection`
  - All connections have obj1 and obj2 attributes that reference the objects that they connect.
  - Note that, due to their levelscript representation, Glue is not a connection
- `Collectable`
  - Collectables have many attributes (see the [Collectable API](#collectables)), but the most important are:
    - Coordinates
    - `is_trigger` – determines whether it is a trigger 
    - `collect_from_object` – determines whether it is collected by Players or Moveable objects
- `Player`
  - The Player character
  - Players have coordinates, size, speed, and density
- `Other`
  - Other exists for objects that don't fall cleanly into other categories (portals, dummies, glue, etc.)

### Types

Object types represent the physics type of an object. Types include:
- `Solid`
  - Objects that do not move
  - Represented by a blue color in the level editor
- `Moveable`
  - Objects that move
  - Represented by an orange color in the level editor
- `Generator`
  - Objects that can be spawned in or destroyed while playing the level
  - All generator objects also inherit from `Moveable`
  - Represented by a green color in the level editor
- `Growing`
  - Objects that grow when a Collectable expands the level
  - Represented by a light blue color in the level editor
- `Rotatable`
  - Objects that rotate according to a speed and torque
  - Represented by a purple color in the level editor


## Custom Objects

Custom Objects are objects that are not natively in circloO, but can be created by composing multiple basic objects together. 
All Custom Objects inherit from the `CustomObject` base class, and they can be added to Levels just like regular Objects using `Level.add()`. 

circloO Helper contains a few Custom Objects:
- `OutlineRectangle`
  - An outline of a Solid Rectangle, comprising 4 SolidRectangles for each side.
- `MoveableArc`
  - An Arc that can move, comprising many small MoveableRectangles.
- `Polygon`
  - A Solid polygon, comprising SolidTriangles.

If you need more control over the base objects that a Custom Object is composed of, you can store them in a new list variable by calling the `build_objs()` method, alter them as needed, and add the contents of that list to the level. For example, if you want to connect all four sides of an OutlineRectangle to a MoveableCircle with a Rope:

```python
lvl = ch.Level()

mc = MoveableCircle(1500, 1800, 20)
lvl.add(mc)

outr_objs = OutlineRectangle(1500, 1500, 200, 150).build_objs()
for obj in outr_objs:
  lvl.add(obj)              # Add the object to the level
  lvl.add(Rope(obj, mc))    # Connect to the MoveableCircle with a Rope
```

When a `CustomObject` is added to a level, its `build_objs()` method is automatically used to generate the underlying objects and add them to the level.

### Creating Custom Objects
  
You can also create your own Custom Objects. A Custom Object should always inherit from `CustomObject`, and it is good practice to also inherit an Object Shape and Object Type if applicable. For example, OutlineRectangle is declared as `class OutlineRectangle(CustomObject, Solid, Rectangle)`.

Custom Objects need to override two functions: `__init__()` and `build_objs()`:
- `__init__()`
  - Should first call `super().__init__()`, then declare all attributes. 
  - For example, if you were to create your own OutlineRectangle class, the `__init__()` function would look roughly like this:
    - ```python
      def __init__(self, x, y, width, height, thickness):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = thickness
      ```
- `build_objs()`
  - Should first call `super().build_objs()` and should return `self._obj_cache`. 
  - All objects that are to be added to a level should be added to `self._obj_cache`, which is a simple list.  
  - For example, if you were to create your own OutlineRectangle class, the `build_objs()` function would like roughly like this:
    - ```python
      def build_objs(self):
          super().build_objs()
          
          top = SolidRectangle(self.x, self.y, self.width, self.thickness)
          left = SolidRectangle(self.x, self.y, self.thickness, self.height)
          right = SolidRectangle(self.x + self.width - self.thickness, self.y, self.thickness, self.height)
          bottom = SolidRectangle(self.x, self.y + self.height - self.thickness, self.width, self.thickness)
          
          self._obj_cache.append(top)
          self._obj_cache.append(left)
          self._obj_cache.append(right)
          self._obj_cache.append(bottom)
          
          return self._obj_cache
      ```


## Tools

circloO Helper contains a few tools to help with repeated tasks, each a function:
- `polar()`
  - Converts a set of (r, theta) polar coordinates into their cartesian counterparts
- `pivot()`
  - Rotates an object around a pivot point by an angle
- `translate()`
  - Translates (moves) an object by x and y values
- `scale()`
  - Scales an object by x and y values according to the object's centroid
- `dimensions()`
  - Returns the dimensions of an object's bounding box as (width, height)
- `centroid()`
  - Returns the (x, y) coordinate of an object's centroid 
- `push_to_android()`
  - Pushes a file to android via ADB
- `combine()`
  - Combines the contents of two levels together, keeping the attributes of the first

All tools that take an Object will return a copy of the Object (the original Object will not be altered)


## Pixel Builder

You can build a 2D or 3D binary array of pixels using the `Pixels` class. The class takes an object and tiles it according to the input array. For example,
```python
arr = [[1, 0, 1],
       [0, 1, 0],
       [1, 0, 1]]
pxls = ch.Pixels(arr, SolidCircle(1500, 1500, 10))
```
will create a checkerboard of Solid Circles with radii of 10 starting at (1500, 1500). 

The input Object for building a 3D array must be a Generator Object Type. The 3rd dimension represents time, and frame duration is determined by the generator's `disappear_after` attribute.

By default, if the input Object is a Rectangle Object Shape, Rectangles in a row and column will be merged wherever possible to reduce the number of objects that are created. The same will also be done for each frame of a 3D array.

Pixels is also implemented by the `Text`, `CHImage`, and `CHVideo` classes.


## Text Conversion

You can easily add text to a Level using the `Text` class. The class takes a string input and an Object, then converts each character into a 2D array to be built with `Pixels`.

```python
txt = ch.Text("Hello, world!", SolidRectangle(1500, 1500, 10, 10))
```

`'\n'`, `'\r'`, and `'\t'` characters are also supported (though note that `'\n'` only moves to the next line, and does not perform a carriage return—use `'\r'` as well for that)


## Image Conversion (raster)

See [Image Conversion (vector)](#image-conversion-vector) for converting SVG images.

You can easily add images (any common format) to a Level using the `CHImage` class. The class takes an input filepath, an Object, and a downsample factor, then dithers and thresholds the image into a 2D binary array that is built with `Pixels`.

```python
img = ch.CHImage("mona_lisa.webp",
                 SolidRectangle(1500, 1500, 10, 10),
                 4)
```

`downsample_factor` is an integer input by which the size of the input image is divided—it should be higher for images with higher resolutions. There are also parameters to change the image thresholding, weight of each RGB channel, and the dithering algorithm (see [Dithering](#dithering)).


## Video Conversion

You can easily add videos (any common format) to a Level using the `CHVideo` class. The class takes an input filepath, an Generator type Object, an output resolution, and an output fps, then dithers and thresholds each frame of the video into a 2D binary array that is built with `Pixels`.

```python
vid = ch.CHVideo("Dancing Rick Astley Loop.mp4",
                 RectangleGenerator(1500, 1500, 10, 10, density=0, no_fade=True),
                 (40, 30),
                 5)
```

It's recommended to set the `density` of the object to 0 (so that the video does not fall apart) and `no_fade` to True (so that each frame appears instantly). Like `CHImage`, there are also parameters to change the thresholding, RGB channel weights, and the dithering algorithm (see [Dithering](#dithering))


## Dithering

The `dithering` module includes a few tools and functions for dithering images. There are two dithering functions in the module:
- Floyd-Steinberg error diffusion dithering
- Ordered dithering

There is also an `undither()` function that returns the original image unchanged.

All dithering functions take an image as input and returns the dithered image. The `ordered_dither()` function also takes a `pattern` argument. A few common or useful patterns are included in the module, but it is trivial to make your own.

Ditherers are primarily used in image- and video-conversion. To use a specific ditherer, simply pass the function of choice into the class:
```python
img = ch.CHImage(..., ditherer=ch.dithering.floyd_steinberg)
pattern = ch.dithering.BAYER_MATRIX_8X8
vid = ch.CHVideo(..., ditherer=lambda x: ch.dithering.ordered_dither(x, pattern))
```
Note that, since `ordered_dither()` takes multiple arguments, a lambda expression is necessary.


## Image Conversion (vector)

See [Image Conversion (raster)](#image-conversion-raster) for converting raster images.

You can also easily add SVG vector images to a Level using the `CHSVG` class. The class takes an input filepath and optional parameters for the image coordinates (from the top-left corner), scale, and thickness of each line.

```python
svg = CHSVG("examples/mysvg.svg")
```


## Audio (MIDI) Conversion

Audio conversion is also fairly simple using the `CHMIDI` class. The class takes an input filepath for a MIDI file and optional parameters, including sound customization and sustained note handling.

See the [CHMIDI API section](#chmidi) for information on how to customize sounds by track.

```python
midi = CHMIDI("examples/Stereo Madness.mid")
```


## Point Plotter

You can plot a set of points using the `PointPlotter` class. The class takes an Object class (currently limited to `Line`, `Rope`, `Slider`, or `DistanceConnection`) and any number of points.

```python
pts = (1510, 1510), (1540, 1520), (1530, 1520), (1520, 1570), (1530, 1540), (1570, 1530), (1580, 1530), (1590, 1500)
plot = PointPlotter(Rope, *pts)
```

Set the `close` attribute to True to connect the final point to the initial point (thus making a closed shape).

<hr>

<br>
The sections above are intended as a conceptual overview of the most important features. The following API reference documents every class, attribute, and method exposed by the library.


# API

## Level

- Location: `ch.Level()`
- Attributes:
  - `segments (int)` - Number of collectables to collect before level is completed; default is 7
    - While this *can* be a float, it is most common to use an int
  - `grav_scale (float)` - Strength of initial gravity; default is 1
  - `grav_dir (float)` - Direction of initial gravity; default is 270 (down)
    - 0 is right, increasing rotates counter-clockwise
  - `start_full (bool)` - If True, the level starts with all segments already revealed; default is False
  - `color (int)` - Level color, 0-255; default is random
  - `music (tuple[int, int])` - Music track played when level starts; default is `(0, 0)` (no preference)
    - `(1, track)` for preferred (start this track after current ends) 
    - `(2, track)` to force
    - Track 4 is silence
  - `recommend_sfx (bool)` - If True, ask players to enable sfx when they start the level; default is False
  - `default_line_thickness (float)` - Default thickness of new Line/Curve/Arc objects when placed in the in-game editor; default is 3
  - `camera_follow_one_player_only (bool)` - If True and there are multiple Players in the level, the camera will only follow the first Player added to the level; default is False
  - `affect_all_players_by_collectables (bool)` - If True, the effects of any collectable collected will apply to all Players, rather than just the one that collected it; default is False
  - `line_extra_width (float)` - Change the size of the sprite for Line/Curve/Arc objects (but not their collisions); default is 0
    - Can be negative, causing the collision to be larger than the sprite
  - `gravcontrol (bool)` - If True, pressing left/right will also rotate the gravity direction; default is False
    - Initial direction will always be down (270), regardless of `grav_dir`
- Methods:
  - Overrides: `repr()` & `str()`, `len()`
  - `add(obj: Object)` - Adds an Object `obj` to the level
  - `object_at(index: int)` - Returns a reference to the `index`'th object added to the level
  - `get_objs()` - Returns a list of all Objects in the level
  - `to_clipboard()` - Copies the level as a string to your clipboard
    - You can then import it to the game using the Import > From Clipboard
    - Also returns the level as a string, allowing `print(Level.to_clipboard())`
  - `to_file(path: str)` - Saves the level to `path` filepath
    - You can then import it to the game using the Import > From File


### Level Parsers

- `ch.parse(level_text: str)` - Parses and returns circloO level from string `level_text`
  - Will only parse levels with a levelscript version of 10 or higher (the default at the current version of the game)
- `ch.read_file(path: str)` - Parses and returns circloO levels from a filepath `path`
  - Opens file at `path`, then calls `parse()`
- `ch.read_clipboard()` - Parses and returns circloO levels from your clipboard
  - To be used with the in-game functionality Save > Export to Clipboard
  - Reads clipboard contents, then calls `parse()`


## Object

- Location: `ch.Object`
- All circloO Objects are children of `Object`
- Methods:
  - Overrides: `repr()` & `str()`
  - `get_id()` - Returns the index of the object within a Level
    - If the object has not yet been added to a Level, the returned id is -1

### Object Shapes

- Location: `ch.object_shapes`
- Inherit from `Object` class
- Other
  - No attributes
  - Exists solely for compatibility with objects that have no clear shape
- `Player`
  - Attributes:
    - `x (float)` - X-position of Player's center
    - `y (float)` - Y-position of Player's center
    - `size (float)` - Radius multiplier of Player; default is 1
      - The actual diameter in editor units follows the formula `size * 64 + 1`
    - `speed (float)` - Player's speed; default is 1
    - `density (float)` - Density of Player; default is 1
    - `restitution (float)` - How much the Player bounces/rebounds after hitting a surface; default is 0
      - This is hidden in-game
      - 0 means no bounce; 1 is perfectly elastic
    - `bullet` - If True, turns on the Improve High-Speed Physics setting; default is True
- `Circle`
  - Attributes:
    - `x (float)` - X-position of circle's center
    - `y (float)` - Y-position of circle's center
    - `radius (float)` - Radius of circle
    - `attractor (float)` - Planet gravity: Positive pulls moveable objects to it, and negative pushes them away; default is 0
    - `wheelsprite (bool)` - If True, changes the circle's sprite to a wheel, rather than the default solid color; default is False
- `Rectangle`
  - Attributes:
    - `x (float)` - X-position of rectangle's top-left corner
    - `y (float)` - Y-position of rectangle's top-left corner
      - If `coords_by_center` is True, `x` and `y` will instead be the coordinates of the rectangle's center
    - `width (float)` - Width of rectangle
    - `height (float)` - Height of rectangle
    - `rotation (float)` - Rotation of the rectangle in degrees; default is 0
      - Increase to rotate clockwise
    - `coords_by_center (bool)` - If True, interprets given `x` and `y` coordinates as the rectangle's center
- `Triangle`
  - Attributes:
    - `x1 (float)` - X-position of 1st point
    - `y1 (float)` - Y-position of 1st point
    - `x2 (float)` - X-position of 2nd point
    - `y2 (float)` - Y-position of 2nd point
    - `x3 (float)` - X-position of 3rd point
    - `y3 (float)` - Y-position of 3rd point
- `Line`
  - Attributes:
    - `thickness (float)` - Thickness of the line; default is 3
      - This is calculated before `Level.line_extra_width` is added
- `Connection`
  - Attributes:
    - `obj1 (Object, CustomObject)` - Reference to first connected Object
      - For a `FixedDistanceConnection`, this is the Portal
      - For a `Hinge`, this is the object that will be rotated around (if no offsets are given)
      - For a `Slider`, this is the object the arrow points away from
      - For a `SpecialConnection`, this is the `SpecialCollectable` that triggers it
    - `obj2 (Object, CustomObject)` - Reference to second connected Object
      - For a `SpecialConnection`, this is the target that the action is applied to
- `Collectable`
  - Attributes:
    - `x (float)` - X-position of collectable's center
    - `y (float)` - Y-position of collectable's center
    - `appear_at_segment (int)` - Segment at which the collectable first appears
    - `part_of_segment (int)` - Number of previously collected collectables within the same segment after which the collectable appears
    - `zoom (float)` - Changes camera zoom upon collection
      - -1 is no change
      - -2 is makes the camera view the full level
      - The larger the number, the more the camera zooms in
    - `is_trigger (bool)` - If True, the collectable will not increase the current segment or part of segment upon collection; default is False
    - `collect_from_object (bool)` - If True, the collectable will only be collected upon collision with Moveable objects, rather than collision with a Player; default is False
    - `start_disabled (bool)` - If True, the collectable starts deactivated and must be reactivated by a `SpecialConnection` to collect; default is False
    - `disable_on_trigger (bool)` - If True, the trigger will deactivate upon collection and must be reactivated by a `SpecialConnection` to collect again; default is False
      - This attribute is irrelevant if the collectable is not a trigger (`is_trigger==True`).
    - `sound (Collectable.Sound)` - The sound that plays when the collectable is collected; default is None
  - Methods:
    - `set_sound(group, note, volume, pitch, play_if_no_function, sound)` - Updates the collectable's sound attribute.
      - All parameters except `sound` are equivalent to the attributes of `Collectable.Sound`
      - `sound (Collectable.Sound, None)` - If not None, this will override all other parameters and set this as the collectable's sound
    - `mute()` - Makes the collectable play no sound upon collection, or unmutes it if alread muted
<a id="collectable-sounds"></a>
  - `Collectable.Sound` inner class
    - Attributes:
      - `group (str)` - Sound type
        - `''` (empty string) is default
        - `'drum'` for percussion, `'piano'` for piano, `'house'` for miscellaneous, `'none'` for no sound
      - `note (int)` - Sound variant; default is 0
        - For piano, the note; for drum, the drum or cymbal; for house, the instrument; etc.
      - `volume (float)` - Volume of sound; default is 1
      - `pitch (float)` - Pitch of sound; default is 1
      - `play_if_no_function (bool)` - If True, the collectable will play this sound even if it does nothing else

### Object Types

- Location: `ch.object_types`
- Inherit from `Object` class
- `Solid`
  - No attributes
- `Moveable`
  - Attributes:
    - `density (float)` - Density of object; default is 1
      - Set to 0 to make the object immovable (functionally equivalent to a Solid)
    - `damping (float)` - How quickly the object is slowed when no force is applied; default is 0
    - `fix_rotation (bool)` - Disable rotation if True; default is False
      - Has no effect on Circle type objects (duh)
    - `bullet (bool)`
      - If True, turns on the Improve High-Speed Physics setting; default is False
      - In-game, this setting is available if you hold Shift while clicking on the Properties menu
- `Generator`
  - Times are measured in seconds
  - Attributes:
    - `disappear_after (float)` - The time for which the object exists before disappearing; default is 5
    - `wait_between (float)` - The time between the object disappearing and a new object generating; default is 1
    - `init_delay (float)` - The initial time that the generator waits before turning on; default is 0
      - `wait_between` is also added to this time
    - `no_fade (bool)` - If True, disables the fading animation when an object appears or disappears; default is False
    - `start_off (bool)` - If True, the generator does not start until triggered via a `SpecialConnection`; default is False
- `Growing`
  - Attributes:
    - `keep_pos (bool)` - If True, the object's x- and y-positions stay the same after growing. If False, they move relative to the new level size; default is False
- `Rotatable`
  - Attributes:
    - `motor_speed (float)` - Speed of rotation; default is 0
    - `torque (float)` - Torque of rotation; default is 100


## Objects

- Location: `ch.circloo_objects`

All Objects are indirect children of `Object`.

Most Objects also inherit an ObjectType and an ObjectShape, which both give them several attributes not shown here. See their respective Types and Shapes to find these inherited attributes.

<a id="solid-objects"></a>
- Solid Objects
  - `SolidCircle` - Solid circle
    - Type: `Solid`
    - Shape: `Circle`
    - No additional attributes
  - `SolidRectangle`
    - Type: `Solid`
    - Shape: `Rectangle`
    - No additional attributes
  - `SolidTriangle`
    - Type: `Solid`
    - Shape: `Triangle`
    - No additional attributes
<a id="lines"></a>
- Lines
  - `Line`
    - Type: `Solid`
    - Shape: `Line`
    - Additional attributes:
      - `x1` - X-position of start point
      - `y1` - Y-position of start point
      - `x2` - X-position of end point
      - `y2` - Y-position of end point
  - `Arc`
    - Type: `Solid`
    - Shape: `Line`
    - Outline of a circular arc
    - Additional attributes:
      - `center_x (float)` - X-position of arc's center
      - `center_y (float)` - Y-position of arc's center
      - `start_angle (float)` - Starting angle in degrees
      - `end_angle (float)` - Ending angle in degrees
        - An angle of 0 is right, and increasing the angle moves the point clockwise
      - `radius (float)` - Radius of arc, calculated from the center of the line thickness
      - `ctr_x (float)` - Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
      - `ctr_y (float)` - Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
  - `Curve`
    - Type: `Solid`
    - Shape: `Line`
    - Cubic Bézier Curve
    - Additional attributes:
      - `start_x` - X-position of start point
      - `start_y` - Y-position of start point
      - `ctr1_x` - X-position of 1st control point
      - `ctr1_y` - Y-position of 1st control point
      - `ctr2_x` - X-position of 2nd control point
      - `ctr2_y` - Y-position of 2nd control point
      - `end_x` - X-position of end point
      - `end_y` - Y-position of end point
      - `resolution` - Béziers are made up of smaller lines. Resolution is how many smaller lines there are; default is 100
<a id="growing-objects"></a>
- Growing Objects
  - `GrowingCircle`
    - Type: `Growing`
    - Shape: `Circle`
    - No additional attributes
  - `GrowingRectangle`
    - Type: `Growing`
    - Shape: `Rectangle`
    - No additional attributes
<a id="moveable-objects"></a>
- Moveable Objects
  - `MoveableCircle`
    - Type: `Moveable`
    - Shape: `Circle`
    - No additional attributes
  - `MoveableRectangle`
    - Type: `Moveable`
    - Shape: `Rectangle`
    - No additional attributes
  - `MoveableTriangle`
    - Type: `Moveable`
    - Shape: `Triangle`
    - No additional attributes
<a id="special-objects"></a>
- Special/Other Objects
  - `Player`
    - No Type
    - Shape: `Player`
    - The Player circle that you control by pressing left & right
    - No additional attributes
  - `RotatableRectangle`
    - Type: `Moveable`
      - Despite its name, this matches the game's implementation, where it behaves more like a `Moveable` than a true `Rotatable` object (it does not have a motor).
    - Shape: `Rectangle`
    - No additional attributes
  - `RotatableCircle`
    - Type: `Rotatable`
    - Shape: `Circle`
    - No additional attributes
  - `SpringyRectangle`
    - Type: `Moveable`
    - Shape: `Rectangle`
    - Rectangle that returns to a resting position of 0 degrees when rotated
    - Additional attributes:
      - `frequency (float)` - Frequency of spring; default is 2
        - Essentially how fast the spring bounces up/down to return to rest
      - `fulcrum_offset (float)` - X-position of the object's fulcrum (point of rotation) relative to the rectangle's center
      - `fulcrum_radius (float)` - Radius of the fulcrum; default is 10
        - Does not affect rotation
  - `Portal`
    - No Type
    - Shape: `Other`
    - Teleports a Player to a target location on contact.
    - Additional attributes:
      - `portal_x (float)` - X-coordinate of portal's center
      - `portal_y (float)` - Y-coordinate of portal's center
      - `target_x (float)` - X-coordinate of target location
      - `target_y (float)` - Y-coordinate of target location
      - `appear_at_circle (int)` - Segment at which the portal is activated; default is 1
        - Hidden in-game, and appears to not work
      - `deactivate_at_circle (int)` - Segment after which to deactivate portal; default is 7
      - `min_touch_time (float)` - Minimum time the Player needs to be touching the portal before it teleports; default is 0
      - `start_disabled (bool)` - If True, the portal starts disabled and must be reactivated by a `SpecialConnection` to use
  - `Dummy`
    - No Type
    - Shape: `Other`
    - This object literally does nothing
    - Additional attributes
      - `x (float)` - X-position of the object's center
      - `y (float)` - Y-position of the object's center
  - `ParticleRectangle`
    - No Type
    - Shape: `Rectangle`
    - Splits into many tiny movable circles with high restitution (bouncy).
      - These circles also persist across restarting the level
    - No additional attributes
<a id="generators"></a>
- Generators
  - `CircleGenerator`
    - Types: `Generator`, `Moveable`
    - Shape: `Circle`
    - Generates movable circles at timed intervals
    - No additional attributes
  - `RectangleGenerator`
    - Types: `Generator`, `Moveable`
    - Shape: `Rectangle`
    - Generates movable rectangles at timed intervals
    - No additional attributes
  - `TriangleGenerator`
    - Types: `Generator`, `Moveable`
    - Shape: `Triangle`
    - Generates movable circles at timed intervals
    - No additional attributes
<a id="connections"></a>
- Connections
  - `Glue`
    - No Type
    - Shape: `Other`
      - Note that Glue does not inherit from `Connection`, unlike all other connections
    - Rigidly connects two `Moveable` objects together.
    - Additional Attributes:
      - `obj1 (Object)` - Reference to first connected Object
      - `obj2 (Object)` - Reference to second connected Object
  - `Rope`
    - No Type
    - Shape: `Connection`
    - Connects two objects with the ability to move independently up to a maximum length
    - When connecting to `Portal` objects, instead use `FixedDistanceConnection`
    - Additional Attributes:
      - `offset1_x (float)` - X-offset from first connected Object; default is 0
      - `offset1_y (float)` - Y-offset from first connected Object; default is 0
      - `offset2_x (float)` - X-offset from second connected Object; default is 0
      - `offset2_y (float)` - Y-offset from second connected Object; default is 0
      - `max_length (float)` - Maximum length the rope can extend beyond the distance between `obj1` and `obj2`; default is 0
  - `FixedDistanceConnection`
    - No Type
    - Shape: `Connection`
    - In-game, used only to connect Portals to Moveable objects via the Rope tool.
      - `obj1` must be the `Portal` object.
    - Known/Useful Interactions:
      - In general, `obj1` will move normally, but `obj2`'s sprite and collision will desync: The sprite will stay connected to `obj1`, but the collision will move fully independently.
        - `obj2`'s sprite will also keep the same general orientation of the collision (e.g., if you rotate a `MoveableRectangle`'s collision, the sprite will also rotate).
        - `obj2`'s collision will otherwise act completely normally.
      - When `obj2` is a `CircleGenerator` or `RectangleGenerator`, the point at which the object is spawned will move with `obj1`.
        - For some reason, this is not true of Triangle generators.
    - Additional attributes:
      - `also_move_destination (bool)` - If True, when `obj1` is a Portal, the target destination will move relative to `obj2`. If False, the Portal will always teleport to the same position. Default is False
  - `DistanceConnection`
    - No Type
    - Shape: `Connection`
    - Rigidly connects any two objects together, allowing rotation on either end.
    - Hidden in-game.
    - Additional attributes:
      - `offset1_x (float)` - X-offset from first connected Object; default is 0
      - `offset1_y (float)` - Y-offset from first connected Object; default is 0
      - `offset2_x (float)` - X-offset from second connected Object; default is 0
      - `offset2_y (float)` - Y-offset from second connected Object; default is 0
  - `Pulley`
    - No Type
    - Shape: `Connection`
    - Connects two objects via a two-pulley system
    - Additional attributes:
      - `pulley1_x (float)` - X-position of first pulley, relative to obj1; default is 0
      - `pulley1_y (float)` - Y-position of first pulley, relative to obj1; default is -100
      - `pulley2_x (float)` - X-position of second pulley, relative to obj2; default is 0
      - `pulley2_y (float)` - Y-position of second pulley, relative to obj2; default is -100
      - `offset1_x (float)` - X-offset of connection from obj1; default is 0
      - `offset1_y (float)` - Y-offset of connection from obj1; default is 0
      - `offset2_x (float)` - X-offset of connection from obj2; default is 0
      - `offset2_y (float)` - Y-offset of connection from obj2; default is 0
        - Note that offsets are unavailable in the editor, and they can be buggy if not left as their default 0
      - `ratio (float)` - How 'strongly' the right side pulls compared to the left; default is 1
      - `unlock_movement (bool)` - Allow for horizontal movement of the pulleys while editing; default is False
  - `Hinge`
    - Type: `Rotatable`
    - Shape: `Connection`
    - Semi-rigidly connects two Objects while allowing rotation at an adjustable pivot point.
    - Can also rotate at a fixed speed and torque
    - Additional attributes:
      - `offset_x (float)` - X-offset of pivot point from `obj1`; default is 0
      - `offset_y (float)` - Y-offset of pivot point from `obj1`; default is 0
      - `draw_connection_line (bool)` - If True, the Hinge is visible while playing the level; default is False
      - `enable_collisions (bool)` - If True, `obj1` and `obj2` will be able to collide with each other; default is False (both will pass through each other)
  - `Slider`
    - No Type
    - Shape: `Connection`
    - Semi-rigidly connects two Objects, allowing movement in a straight line between each other.
    - Additional attributes:
      - `offset_x (float)` - X-offset from `obj1`; default is 0
      - `offset_y (float)` - Y-offset from `obj1`; default is 0
  - `SpecialConnection`
    - No Type
    - Shape: `Connection`
    - Performs an action on `obj2` upon the collection of `obj1`, where `obj1` must be a `SpecialCollectable` or `InputTrigger`
    - Supported actions:
      - `Disconnect` - Destroys/disconnects a Rope or Hinge
      - `Follow` - Sets the camera to follow most Objects
      - `Reset` - For Generators, enables and resets the `init_delay` countdown
      - `Now` - For Generators, Generates a single Object
      - `NowIf` - For Generators, Generates an Object only if no Objects generated from that Generator currently exist
      - `Destroy` - For Generators, destroys all instances of generated Objects
      - `On` - Enables Portals or turns on Generators
      - `Off` - Disables Portals or turns off Generators
      - `Teleport` - For Portals, immediately teleports all Players to the target position
      - `RotationOn` - For `Moveable` Objects, allows the Object to rotate
      - `RotationOff` - For `Moveable` Objects, disables rotation of the Object
      - `SetSpeed` - Sets the x and y speed of a Solid or Moveable Object
        - Requires two additional attributes: new x speed and new y speed
        - If the Object is a Solid, it will keep moving until another `SetSpeed` action is applied
        - Set either x or y to 9999 to not change the speed in that direction
      - `Impulse` - Applies a force to an Object in the x- and y-directions
        - Requires two additional attributes: x-impulse and y-impulse
      - `Trigger` - For Collectables, collects and triggers the collectable
      - `TriggerRandom` - For Collectables, collects and triggers connected collectables randomly
        - If multiple Collectables are connected to the same `obj1` trigger, one of them is chosen at random
        - If a single Collectable is connected to a trigger, that Collectable will be triggered with a 50% chance
    - Additional attributes:
      - `collectable (Collectable)` - Reference to the Collectable that triggers the SpecialConnection
      - `target (Object)` - Reference to target Object which `action` is performed upon
      - `action (str)` - Action performed upon `target` (see above for supported actions)
      - `*args (tuple)` - Additional arguments required when `action` is `SetSpeed` or `Impulse`
<a id="collectables"></a>
- Collectables
  - `Collectable`
    - No Type
    - Shape: `Collectable`
    - The default Collectable Object that performs no special functions upon collection
    - No additional attributes
  - `GravityCollectable`
    - No Type
    - Shape: `Collectable`
    - Changes level gravity upon collection
    - Additional attributes:
      - `grav_dir (float)` - Direction of new gravity in degrees; default is 270 (down)
        - An angle of 0 is right, and increasing the angle rotates counter-clockwise
      - `grav_strength (float)` - Strength of new gravity; default is 1
  - `SizeCollectable`
    - No Type
    - Shape: `Collectable`
    - Changes Player size upon collection
    - Additional attributes:
      - `size (float)` - New radius/size of player; default is 1
      - `by_player_percent (bool)` - If False, new size is measured in editor units
        - The new radius is generally determined by a percentage of the default Player radius, rather than the actual diameter
        - Note that (for some reason), in-game, the Size Collectable's `size` is not the same as the Player's `size`.
  - `DisconnectCollectable`
    - No Type
    - Shape: `Collectable`
    - Disconnects all Players from all Connections upon collection
    - No additional attributes
  - `SpeedCollectable`
    - No Type
    - Shape: `Collectable`
    - Changes Player speed upon collection; only affects Player that collected it
    - Additional attributes:
      - `speed (float)` - New speed of Player; default is 1
  - `SpecialCollectable`
    - No Type
    - Shape: `Collectable`
    - Performs an action on an Object connected to it via a `SpecialConnection`
    - No additional attributes
  - `InputTrigger`
    - No Type
    - Shape: `Collectable`
    - Performs an action on an Object connected to it via a `SpecialConnection` once a certain input has been pressed
    - Additional attributes
      - `input (str)` - The type of input that activates the trigger
        - `left`, `right`, or `both` activates the trigger when you action the left button, right button, or both buttons
        - `every_frame` sets the trigger to activate on every frame
        - `on_trigger` sets the trigger to only activate when triggered by a `SpecialConnection` with a `Trigger` or `TriggerRandom` action
      - `action (str)` - How the input must be actioned to activate the trigger
        - Only matters for `left`, `right`, and `both` inputs.
        - `pressed` and `released` activate the trigger when the button(s) is pressed or released, respectively.
        - `down` activates the trigger every frame while the button is held down.
  

## Custom Object

- Location: `ch.CustomObject`
- Methods:
  - Overrides: `repr()` & `str()`, `len()`
  - `get_id()` - Returns the index of the object within a Level
    - If the object has not yet been added to a Level, the returned id is -1
  - `build_objs()` - Clears the object cache, adds all necessary objects to the cache, then returns the cache
    - To be overridden in all child classes with the following structure:
      ```python
      def build_objs(self):
        super().build_objs()  # Clears self._obj_cache
        # Create objects and add them to self.obj_cache
        return self._obj_cache
      ```

### Included Custom Objects

- Location: `ch.custom_objects`
- All custom objects included in the library inherit from `CustomObject`
- All converters and several other objects are also Custom Objects, but they have their own dedicated sections.
- `OutlineRectangle`
  - Type: `Solid`
  - Shape: `Rectangle`
  - A solid outline of a Rectangle, where the outline is along the inner edge.
  - No additional attributes
- `MoveableArc`
  - Type: `Moveable`
  - Shape: `Line`
  - A movable arc of a circle, where the outline is centered on the radius
  - Additional attributes:
    - `radius (float)` - Radius of the arc
    - `start_angle (float)` - Starting angle of the outline in degrees; default is 0 (right)
    - `end_angle (float)` - Ending angle of the outline in degrees; default is 360 (creates a full circle with `start_angle`'s default value)
    - `resolution (int)` - Number of rectangles that make up the final arc; default is None
      - If None, resolution is calculated automatically for a good combination of resolution and low object count.
- `Polygon`
  - Type: `Solid`
  - Shape: `Other`
  - A simple polygon built using ear-clipping from the tripy library
  - Additional attributes:
    - `*points (tuple[float])` - Any number of (x, y) points


## Tools

- Most transformation tools do not work with Custom Objects
- `ch.polar(r, theta, start_x, start_y, in_degrees)`
  - Converts a point in polar coordinates to rectangular coordinates.
  - Returns the rectangular coordinates.
  - `r` is the distance from (`start_x`, `start_y`).
    - (`start_x`, `start_y`) is the center of the level (1500, 1500) by default
  - `theta` is the rotation angle, where 0 is to the right.
  - If `in_degrees` is True, `theta` will be interpreted in degrees. If False, it will be interpreted in radians.
- `ch.pivot(obj, theta, pivot_x, pivot_y, in_degrees)`
  - Rotates an Object `obj` around a pivot point.
  - Returns a copy of `obj` and leaves the original unaltered
  - `theta` is the rotation angle, where 0 is to the right.
  - If `in_degrees` is True, `theta` will be interpreted in degrees. If False, it will be interpreted in radians.
  - `pivot_x` and `pivot_y` are the coordinates of the pivot point.
- `ch.translate(obj, by_x, by_y)`
  - Translates (moves) an Object `obj` by an x and y value.
  - Returns a copy of `obj` and leaves the original unaltered
  - `by_x` and `by_y` are both 0 by default, and are the values by which `obj` is shifted.
- `ch.scale(obj, by_x, by_y)`
  - Scales an Object `obj` by an x and y value.
  - Returns a copy of `obj` and leaves the original unaltered
  - `by_x` and `by_y` are the values by which `obj` is scaled.
  - If `by_y` is None, the same value as `by_x` will be used, scaling both axes by the same amount.
- `ch.dimensions(obj)`
  - Returns the dimensions of an Object `obj`'s bounding box as (width, height)
- `ch.centroid(obj)`
  - Returns the centroid (geometric center) of an Object `obj` as (x, y)
- `ch.push_to_android(file_path, destination)`
  - Uses ADB to send a file at `file_path` to an Android device's `destination` path.
- `ch.combine(level_1, level_2)`
  - Combines the contents of two Levels `level_1` and `level_2`
  - The header/attributes of `level_1` are kept.
  - Duplicate Objects that occur in each level are discarded


## Converters

### Pixel Builder

- Location: `ch.Pixels`
- Child of `CustomObject`
- Tiles an input Object according to an input 2D or 3D binary numpy array.
- Attributes:
  - `arr (np.array)` - 2D or 3D binary array
    - A copy of `obj` is created in each cell that contains a 1.
    - If the array is 3D, the third dimension is time. As such, `obj` must be of type `Generator` when using a 3D array.
      - The time between each frame of the 3D array will be `obj.disappear_after`
      - The Generator will be set to Generate Only Once (`wait_between = 9999`)
  - `obj (Object)` - The Object to be tiled.
    - The top-left Object of the array will have the same coordinates as `obj`
  - `scale_x (float, None)` - Horizontal distance between each object; default is None
    - If None, the horizontal distance will be the width of `obj`
  - `scale_y (float, None)` - Vertical distance between each object; default is None
    - If None, the vertical distance will be the height of `obj`
  - `reduce_objects (bool)` - If True, multiple object-count–reduction steps will be taken; default is True
    - For `Rectangle` shape objects, greedy rectangle decomposition will be performed.
    - For 3D arrays, consecutive frames with a 1 in the same cell will be merged into a single Generator that stays on for the duration of all frames.
    - Setting this to False is highly discouraged for large arrays.


### Text

- Location: `ch.Text`
- Child of `CustomObject`
- Converts a string of text into circloO Objects. 
- Allows use of \n (new line), \r (carriage return), and \t (tabulation).
- Unsupported characters will be replaced with a large blank box.
- A `Text` object is a composition of `Pixels` objects.
- Attributes:
  - `text (str)` - String of text to be converted
  - `obj (Object)` - Object to be tiled to create each letter
  - `spacing (float)` - Space between each letter as a scaler to the width of `obj`; default is 1


### Plotter

- Location: `ch.PointPlotter`
- Child of `CustomObject`
- Connects several points in a straight line.
- Attributes:
  - `obj_type (class)` - Type of circloO Object that displays a straight line
    - Supported Objects: `Line`, `Rope`, `Slider`, `DistanceConnection`
  - `points (tuple[float])` - Any number of (x, y) points
  - `close (bool)` - If True, connects the ending point to the starting point with another line, making a closed polygon; default is True
  - `line_thickness (float)` - If `obj_type` is `Line`, the thickness of each Line; default is 3


### CHImage

- Location: `ch.CHImage`
- Child of `CustomObject`
- Converts an image into circloO objects via dithering and grayscale conversion.
- Uses `Pixels` to create final array of Objects.
- Note that primitive support for this is included in-game with Ctrl+Shift+F4
  - Does not dither and converts everything into `MoveableRectangle` objects
- Attributes:
  - `filepath (str)` - Path to input image
    - Image is opened using the PIL library, so most common extensions are supported.
  - `obj (Object)` - Object to be tiled into image. 
    - The coordinates of this Object will be used as the top-left corner of the image.
  - `downsample_factor (int)` - Factor to downscale/downsample image
    - 1 will keep the image the same resolution
    - For images with higher resolutions, it is recommended to increase this value.
  - `threshold (float)` - Threshold for binarization; default is 0.5
    - Should be between 0 and 1.
  - `channel_weights (tuple[float])` - Weights for each channel to apply a weighted average for grayscale conversion; default is (1, 1, 1) (equal weights for each channel)
  - `ditherer (function)` - Dithering function (found in `dithering` module); default ditherer is Floyd-Steinberg
  - `show_img (bool)` - If True, displays the processed binary image before converting to circloO Objects; default is True


### CHVideo

- Location: `ch.CHVideo`
- Child of `CustomObject`
- Converts a video into circloO objects via dithering and grayscale conversion.
- Uses `Pixels` to create the final array of Objects.
- Attributes:
  - `filepath (str)` - Path to input video
    - Video is opened using the imageio library, so most common extensions are supported.
  - `obj (Object)` - Object to be tiled into video
    - Must be of Type `Generator`
    - The coordinates of this Object will be used as the top-left corner of the video.
  - `resolution (tuple[int])` - Output resolution of the video in pixels as (width, height)
  - `fps (float)` - Output displayed frames per second of video
  - `threshold (float)` - Threshold for binarization; default is 0.5
    - Should be between 0 and 1.
  - `channel_weights (tuple[float])` - Weights for each channel to apply a weighted average for grayscale conversion; default is (1, 1, 1) (equal weights for each channel)
  - `ditherer (function)` - Dithering function (found in `dithering` module); default ditherer is Ordered dithering with a line pattern
  - `show_img (bool)` - If True, displays the processed frames of the video as it is being processed; default is True


### CHSVG

- Location: `ch.CHSVG`
- Child of `CustomObject`
- Converts a vector/svg image into circloO objects.
- Attributes:
  - `filepath (str)` - Path to input image
  - `x_pos (float)` - X-coordinate of top-left corner; default is 1500 (center)
  - `y_pos (float)` - Y-coordinate of top-left corner; default is 1500 (center)
  - `scale (float)` - Scale of image; default is 1 (no scaling)
  - `line_thickness (float)` - Thickness of each line; default is 3


### CHMIDI

- Location: `ch.CHMIDI`
- Child of `CustomObject`
- Converts a MIDI (.mid) file into circloO objects.
- The conversion follows the General MIDI standard for converting percussion, assuming that all percussion notes are on channel 10 of the score.
  - Default percussion instrument sounds are provided.
  - All sounds can be overridden by track with `track_params` in case the General standard is not followed.
- Attributes:
  - `filepath (str)` - Path to midi file
  - `start_x (float)` - X-position of top-left-most trigger; default is 1500 (center of level)
  - `start_y (float)` - Y-position of top-left-most trigger; default is 1500 (center of level)
  - `min_duration (float)` - The minimum necessary duration of a note (in seconds) before a sustained trigger is used instead of a simpler one
    - To disable this & use simple triggers for every note, set this to a very large value (e.g., 9999)
  - `long_start_x (float)` - X-position of top-left trigger of the sustained trigger section; default is None
  - `long_start_y (float)` - Y-position of top-left trigger of the sustained trigger section; default is None
    - If None, the section will be placed just to the left of the main body of the system.
    - The sustained trigger section will be a vertical line of triggers with two columns.
  - `pitch (float)` - Default pitch of all trigger sounds if none is provided for the track or note in `track_params`; default is 1
  - `volume (float)` - Default volume of all trigger sounds if none is provided for the track or note in `track_params`; default is 1
  - `labels (bool)` - If True, tracks will be labeled in-game (using the `Text` converter) with their names; default is True
  - `track_params (dict)` - Dictionary of track sound overrides.
  - Syntax:
    - `track_params` is a dictionary where each key is the number of a track within the score. 
    - For each track, you can set the default pitch and default volume of the track, which overrides the default `pitch` and `volume` attributes of the Object. 
    - For each track, you can also further override specific notes within the track by setting their full Collectable Sounds (see [Object Shapes > Collectable.Sound](#collectable-sounds)).
      - Sound attributes are provided as a tuple: `(group, note, pitch, volume)`
      - [This](https://musescore.org/sites/musescore.org/files/General%20MIDI%20Standard%20Percussion%20Set%20Key%20Map.pdf) pdf from Musescore is a good resource that shows each note's integer value, their corresponding note, and their corresponding percussion instrument sound.
    - Any value within each layer of the dictionary can be omitted.
    - Pitch/volume override hierarchy (from highest to lowest priority): `note_value` in `"note_overrides"` -> `"pitch"`/`"volume"` in `track_num` -> `CHMIDI.pitch`/`CHMIDI.volume`
    ```python
    track_params = {
      track_num:                # Track number (integer)
      {
        "pitch": ...,           # The default pitch used for all triggers in this track if not further overridden in "note_overrides" 
        "volume": ...,          # The default volume used for all triggers in this track if not further overridden in "note_overrides"
        "note_overrides":       # Overrides specific note values within the track.
        {
          # note_value is an integer label of the midi note. See the General MIDI standard for more information.
          note_value: (group, note, pitch, volume),   # A tuple of the sound's attributes. Uses the same scheme as Collectable.Sound
          note_value: (...),    # You can override any number of notes within the track
          note_value: (...),
        }
      },
      track_num: {...},         # You can add overrides for any number of tracks within the score
      track_num: {...}
    }
    ```


### Dithering

A module that provides several dithering functions for grayscale arrays.

- Location: `ch.dithering`

Includes both Floyd-Steinberg error diffusion dithering and Ordered dithering.

If you want to implement your own dithering function, the input parameter and return value of each should be an image with three channels as a numpy array.

Note that, if using ordered dithering for the `ditherer` parameter of CHVideo or CHImage, you must pass in the dithering pattern via a lambda function: (e.g., `ditherer=lambda x: ordered_dither(x, BAYER_MATRIX_8X8)`)

Ordered dithering patterns:
- `BAYER_MATRIX_8X8` - Basic 8x8 Bayer matrix; recommended for images or small videos.
- `LINE_DITHER_8X8` - Dithers in straight horizontal lines; recommended for large videos, since it maximizes the amount width-first rectangle decomposition algorithms help.
- `DOTTED_LINE_DITHER` - Similar to `LINE_DITHER_8X8`, but alternates the lines and positions for a little more detail; recommended for medium videos.
- You can also make your own pattern (they're just 2D numpy arrays with values between 0 & 1 :p)


<hr>

# To-Do & Known Issues

TODO: Implement this section.

For now, search through the code for comments prefixed by `TODO: `
