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
    - [Creating your own](#creating-custom-objects)
  - [Tools](#tools)
  - [Pixel Builder](#pixel-builder)
  - [Text Conversion](#text-conversion)
  - [Image Conversion (raster)](#image-conversion-raster)
  - [Image Conversion (vector)](#image-conversion-vector)
  - [Video Conversion](#video-conversion)
  - [Dithering Module](#dithering)
  - [Point Plotter](#point-plotters)
- [API](#api)
- [To-Do & Know Issues](#to-do--known-issues)


# circloO Helper

circloO Helper is a Python library to programmatically generate and alter circloO levels.


## Main Features

- Creation and editing of levels and objects
- Full documentation of level and object attributes
- Video, Image (both raster & vector), and Text conversion
- Custom objects (this is a really cool one)
- Several miscellaneous tools


## Setup

```commandline
pip install git+https://github.com/theShield-Z/circloO_helper.git
```

You can alternatively download the source from GitHub, navigate to the directory that contains `setup.py`, and run:
```commandline
pip install .
```


## Basic Workflow

```python
# Import the library.
# TODO: maybe include ropes/connections in this example
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

Create a level by calling `ch.Level()`. You can see the full API [here](), but the most important Level attributes are `color`, `segments`, and `grav_scale`, which determine the level's color, the number of segments, and the gravity strength respectively. 

To add an object `obj` to a Level `lvl`, use `lvl.add(obj)`. Once you have finished programming your level, you can export to your clipboard, as a file, or simply print it to the terminal.

Existing levels created in-game can also be parsed and edited with this library. Use `parse()` to parse strings. Use `read_file()` to parse a file from a file path. Use `read_clipboard()` to parse a level from your clipboard (used in conjunction with the in-game Copy to Clipboard button).


## Objects

Every object is a child class that inherits from ObjectShape and often also ObjectType, which themselves inherit from the base Object class in `object.py`.

### Shapes

Object shapes represent the shape or category of an object. Shapes include:
- Circle
  - Circles have coordinates and a radius
- Rectangle
  - Rectangles have coordinates, a width, and a height
- Triangle
  - Triangles have coordinates
- Line
  - Lines have a thickness
- Connection
  - All connections have obj1 and obj2 attributes that reference the objects that they connect.
  - Note that, due to their levelscript representation, Glue is not a connection
- Collectable
  - Collectables have many attributes (see the [Collectable API](#api)), but the most important are:
    - Coordinates
    - `is_trigger` – determines whether it is a trigger 
    - `collect_from_object` – determines whether it is collected by Players or Moveable objects
- Player
  - The Player character
  - Players have coordinates, size, speed, and density
- Other
  - Other exists for objects that don't fall cleanly into other categories (portals, dummies, glue, etc.)

### Types

Object types represent the physics type of an object. Types include:
- Solid
  - Objects that do not move
  - Represented by a blue color in the level editor
- Moveable
  - Objects that move
  - Represented by an orange color in the level editor
- Generator
  - Objects that can be spawned in or destroyed while playing the level
  - All generator objects also inherit from Moveable
  - Represented by a green color in the level editor
- Growing
  - Objects that grow when a Collectable is collected that causes the level to expand
  - Represented by a light blue color in the level editor
- Rotatable
  - Objects that rotate according to a speed and torque
  - Represented by a purple color in the level editor


## Custom Objects

Custom Objects are objects that are not natively in circloO, but can be created by composing multiple basic objects together. All Custom Objects inherit from the `CustomObject` base class. circloO Helper contains a few Custom Objects:
- `OutlineRectangle`
  - An outline of a Solid Rectangle, comprising 4 SolidRectangles for each side.
- `MoveableArc`
  - An Arc that can move, comprising many small MoveableRectangles.
- `Polygon`
  - A Solid polygon, comprising SolidTriangles.

If you need more control over the base objects that a Custom Object is composed of, you can store them in a new list variable by calling the `build_objs()` method, alter them as needed, and add the contents of that list to the level. For example, if you want to all four sides of an OutlineRectangle to a MoveableCircle:

```python
lvl = ch.Level()

mc = MoveableCircle(1500, 1800, 20)
lvl.add(mc)

outr_objs = OutlineRectangle(1500, 1500, 200, 150).build_objs()
for obj in outr_objs:
  lvl.add(obj)              # Add the object to the level
  lvl.add(Rope(obj, mc))    # Connect to the MoveableCircle with a Rope
```

### Creating Custom Objects
  
You can also create your own Custom Objects. A Custom Object should always inherit from `CustomObject`, and it is good practice to also inherit an Object Shape and Object Type if applicable. For example, OutlineRectangle is declared as `class OutlineRectangle(CustomObject, Solid, Rectangle)`.

Custom Objects need to override two functions: `__init__()` and `build_objs()`:
- `__init__()`
  - Should first call `super().__init__()`, then declare all attributes. 
  - For example, if you were to create your own OutlineRectangle class, the `__init__()` function would like roughly like this:
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

The input Object for building a 3D array must be a Generator Object Type. The 3rd dimension will be time, using the generator's `disappear_after` attribute as the duration of each frame.

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

You can easily add images (any common format) to a Level using the `CHImage` class. The class takes an input filepath, an Object, and a downsample factor, then dithers and thresholds the image into a 2D binary array that can be built with `Pixels`.

```python
img = ch.CHImage("examples/shrek.webp",
                 SolidRectangle(1500, 1500, 10, 10),
                 4)
```

`downsample_factor` is an integer input by which the size of the input image is divided—it should be higher for images with higher resolutions. There are also parameters to change the image thresholding, weight of each RGB channel, and the dithering algorithm (see [Dithering](#dithering))


## Video Conversion

You can easily add images (any common format) to a Level using the `CHVideo` class. The class takes an input filepath, an Generator type Object, an output resolution, and an output fps, then dithers and thresholds each frame of the video into a 2D binary array that can be built with `Pixels`.

```python
vid = ch.CHVideo("examples/Dancing Rick Astley Loop.mp4",
                 RectangleGenerator(1500, 1500, 10, 10, density=0, no_fade=True),
                 (40, 30),
                 5)
```

It's recommended to set the `density` of the object to 0 (so that the video does not fall apart) and `no_fade` to True (so that each frame appears instantly). Like `CHImage`, there are also parameters to change the thresholding, RGB channel weights, and the dithering algorithm (see [Dithering](#dithering))


## Dithering

The `dithering` module includes a few tools and functions for dithering images. There are two dithering functions in the module:
- Floyd-Steinberg error diffusion dithering
- Ordered dithering

There is also an `undither()` function that returns an un-altered image.

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

## Point Plotter

You can plot a set of points using the `PointPlotter` class. The class takes an Object type (currently limited to Line, Rope, Slider, or DistanceConnection) and any number of points.

```python
pts = (1510, 1510), (1540, 1520), (1530, 1520), (1520, 1570), (1530, 1540), (1570, 1530), (1580, 1530), (1590, 1500)
plot = PointPlotter(Rope, *pts)
```

Set the `close` attribute to True to connect the final point to the initial point (thus making a closed shape).


# API

TODO: Implement this section.

## To-Do & Known Issues

TODO: Implement this section.

[//]: # ()
[//]: # ()
[//]: # (## Mechanisms &#40;deprecated in favor of Custom Objects&#41;)

[//]: # ()
[//]: # (circloO Helper also supports mechanisms: groups of objects that perform a specific function. These may not all work correctly depending on your setup—it's on my to-do list.)

[//]: # (Create a mechanism, then add it to your level:)

[//]: # (```)

[//]: # (mechanism = ch.mechanisms.LeftRightDetector&#40;1500, 1500, lvl.get_len&#40;&#41;&#41;     # create a right/left detector at the center of the level)

[//]: # (mechanism.add_to&#40;lvl&#41;       # add mechanism to level)

[//]: # (```)

[//]: # ()
[//]: # (## Image Conversion)

[//]: # ()
[//]: # (You can put images into your level very easily. Convert an image, then add it to the level:)

[//]: # (```)

[//]: # (img = ch.image_to_circloo&#40;"examples/mona_lisa.webp", 4, 1500, 1500&#41;)

[//]: # (lvl.add&#40;img&#41;)

[//]: # (```)

[//]: # (There are a lot of customizable parameters for this, including a downsample factor, channel weighting, and more! Details of each are in the documentation in `image_converter.py`.)

[//]: # (It uses a very efficient algorithm to limit the amount of objects used. As long as you use a sensible downsample factor, you'll have no issue adding images to your levels.)

[//]: # ()
[//]: # (## Video Conversion)

[//]: # ()
[//]: # (You can put videos into your level with relative ease. Convert the video, then add it to the level:)

[//]: # (```)

[//]: # (video = ch.video_to_circloo&#40;"examples/Dancing Rick Astley Loop.mp4", &#40;96, 54&#41;, 10, 3, 1500, 1500&#41;)

[//]: # (lvl.add&#40;video&#41;)

[//]: # (```)

[//]: # (There are a lot of customizable parameters for this, including frame size, frame skipping, fps, dithering patterns, and more! Details of each are in the documentation in `video_converter.py`.)

[//]: # (Like the image converter, it also uses a very efficient algorithm to limit the amount of objects used. You may have to play around with frame skipping and fps to display a given video, but as long is it isn't too long, you should be fine. In general, you want to choose `frame_skip` and `fps` so that `fps = 30 / frame_skip` to match the original video's play speed &#40;e.g., if `frame_skip` is 10, then `fps` should be 3&#41;.)

[//]: # ()
[//]: # (## Text Conversion)

[//]: # ()
[//]: # (You can easily add text to your circloO level, too. Convert a string of text, then add it to the level:)

[//]: # (```)

[//]: # (phrase = ch.write&#40;"Hello World!", 1500, 1500&#41;)

[//]: # (lvl.add&#40;phrase&#41;)

[//]: # (```)

[//]: # (You can also change the size of the text using `size` and the spacing of the letters using `spacing`.)

[//]: # ()
[//]: # ()
[//]: # (# To Do / Known Bugs)

[//]: # ()
[//]: # (- add a defaults module that contains example levels and former mechanisms)

[//]: # (- improve examples in `main.py` to reflect the most recent version.)

[//]: # (- update the README with new features for this version)

[//]: # (- preexisting levels with connections don't always parse properly... for *some* reason??)
