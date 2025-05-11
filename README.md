This is a work-in-progress repository of programs to make it easier for circloO level creators to create levels.

Not everything is finished at the moment, but it should fully usable. Message me if there are any bugs (current version is not fully tested).

# Features

- Creation and editing of levels and objects
- Full documentation of level and object attributes
- Video, Image, and Text conversion!
- Parse and edit existing levels
- Mechanisms
- Several miscellaneous tools

# Usage

Examples for how to use the library are in `main.py`.

First, add the library to your project. You can do this either by copying all the files to your project's folder, or preferably via pip:
`pip install git+https://github.com/theShield-Z/circloO_helper.git`


Create a level:
```
lvl = ch.Level()
```

Create objects with `ch.objects.[object]`:
```
obj_1 = ch.objects.Player(1500, 1500)

# or, if you know the syntax of each object and want more control:
obj_2 = ch.Object(['y', 1500, 1500, 1, 1, 1])

# Both create a Player object at the center of the screen.
```

Add an object to a level:
```
lvl.add(obj_1)

# or insert it at any part of the level:
lvl.insert(obj_2, 0)    # inserts obj_2 at the beginning of the level
```

Remove or replace objects:
```
lvl.remove(1)    # removes the object at id 1
lvl.replace(0, obj_1)   # replaces the object at id 0 with obj_1
```

Then, you can simply print it or save it to a file:
```
print(lvl)
lvl.to_file("my_circloO_level.txt")
```

## Parsing

You can work with an existing level using the `parse` function:
```
with open("my_circloO_level.txt", 'r') as file:
    lvl = ch.parse(file.read())
```
Then work with it just like you would a level created from scratch.

## Mechanisms

circloO Helper also supports mechanisms: groups of objects that perform a specific function. These may not all work correctly depending on your setup—it's on my to-do list.
Create a mechanism, then add it to your level:
```
mechanism = ch.mechanisms.LeftRightDetector(1500, 1500, lvl.get_len())     # create a right/left detector at the center of the level
mechanism.add_to(lvl)       # add mechanism to level
```

## Image Conversion

You can put images into your level very easily. Convert an image, then add it to the level:
```
img = ch.image_to_circloo("examples/mona_lisa.webp", 4, 1500, 1500)
lvl.add(img)
```
There are a lot of customizable parameters for this, including a downsample factor, channel weighting, and more! Details of each are in the documentation in `image_converter.py`.
It uses a very efficient algorithm to limit the amount of objects used. As long as you use a sensible downsample factor, you'll have no issue adding images to your levels.

## Video Conversion

You can put videos into your level with relative ease. Convert the video, then add it to the level:
```
video = ch.video_to_circloo("examples/Dancing Rick Astley Loop.mp4", (96, 54), 10, 3, 1500, 1500)
lvl.add(video)
```
There are a lot of customizable parameters for this, including frame size, frame skipping, fps, dithering patterns, and more! Details of each are in the documentation in `video_converter.py`.
Like the image converter, it also uses a very efficient algorithm to limit the amount of objects used. You may have to play around with frame skipping and fps to display a given video, but as long is it isn't too long, you should be fine. In general, you want to choose `frame_skip` and `fps` so that `fps = 30 / frame_skip` to match the original video's play speed (e.g., if `frame_skip` is 10, then `fps` should be 3).

## Text Conversion

You can easily add text to your circloO level, too. Convert a string of text, then add it to the level:
```
phrase = ch.write("Hello World!", 1500, 1500)
lvl.add(phrase)
```
You can also change the size of the text using `size` and the spacing of the letters using `spacing`.


# To Do / Known Bugs

- make mechanisms more robust and easier to use.
- improve examples in `main.py` to reflect the most recent version.
- Add options to the pip installer (i.e., if you know you won't use the video converter, you don't need to install opencv)
- preexisting levels with connections don't always parse properly.
- It seems like the dependencies might not be importing correctly. This is a major bug, but for now, you can fix this by just installing all of them yourself (there's only like 3 nonstandard ones: pillow, matplotlib, and opencv)
