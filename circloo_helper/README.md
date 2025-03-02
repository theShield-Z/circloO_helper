The primary part of circloO Helper, this folder contains a WIP library to simplify creating levels via code.

Not everything is finished at the moment, but it's fully usable. Message me if there are any bugs.

## Features

- Full documentation of level and object attributes
- Explicit object definitions (so you don't have to memorize the syntax of each object!)
- Creation and editing of levels and objects

## Usage

Copy all the files in the circloo_helper directory to a Python project, then `import circloo_helper as ch`.

Create a level:
```
lvl = ch.Level()
```

Create objects:
```
obj_1 = ch.objects.Player(1500, 1500)
# or, without explicit objects
obj_2 = ch.Object(['y', 1500, 1500, 1, 1, 1])
```

Add an object to a level:
```
lvl.add(obj_1)
```

## To Do

- more tools
- figure out how to use git
- level parser
