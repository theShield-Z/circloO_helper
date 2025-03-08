The primary part of circloO Helper, this folder contains a WIP library to simplify creating circloO levels via code.

Not everything is finished at the moment, but it's fully usable. Message me if there are any bugs (current version is not fully tested).

# Features

- Creation and editing of levels and objects
- Full documentation of level and object attributes
- Explicit object definitions (so you don't have to memorize the syntax of each object!)
- Parse and edit existing levels
- Mechanisms!

# Usage

An example level-creation file is in `main.py`

First, add the library to your project. You can do this either by copying all `.py` files to your project's folder (you may have to mess with some import statements, im too tired to fix it rn -_-), or preferably by installing the standalone library from the standalone circloO_helper_library branch via pip.

Create a level:
```
lvl = ch.Level()
```

Create objects with `ch.objects.[object]`:
```
obj_1 = ch.objects.Player(1500, 1500)    # create Player object at the center of the screen

# or, if you know the syntax of each object and want more control:
obj_2 = ch.Object(['y', 1500, 1500, 1, 1, 1])
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
then work with it just like you would a level created from scratch.

## Mechanisms

circloO Helper now also supports mechanisms–groups of objects that perform a specific function. There are currently only three supported (Right/Left and Pause detectors and Ring Counters), but there may eventually be more.
Create a mechanism, then add it to your level:
```
mechanism = ch.mechanisms.LeftRightDetector(1500, 1500, lvl.get_len())     # create a right/left detector at the center of the level
mechanism.add_to(lvl)       # add mechanism to level
```



# To Do

- more tools
- de-clunkify usage (especially mechanisms)
