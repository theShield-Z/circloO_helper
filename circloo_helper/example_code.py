import circloo_helper as ch

lvl = ch.Level()
lvl.add(ch.Object(["y", 1500, 1500, 1, 1, 1]))
lvl.insert(0, ch.Object(["y", 1500, 1000, 1, 1, 0], ['bullet']))
lvl.replace(0, ch.Object(["b", 1500, 1500]))
lvl.replace(0, lvl.object_at(1))
obj1 = ch.Object(["tmc", 1500, 1500, 10, 10, 0, 0, 1], ['off'])
obj2 = ch.objects.Player(1500, 1500, 5, 5, 5)
lvl.add(obj1)
lvl.add(obj2)
lvl.replace(3, obj1)
lvl.add(ch.objects.Rope(0, 1))
lvl.remove(0)
print(lvl)
print()


# OUTPUT
"""
/
/ circloO level
/ Made with circloO Level Editor
totalCircles 7 0
/ EDITOR_TOOL 1 select
/ EDITOR_VIEW 1500 1500 1
/ EDT 3303
/ _SAVE_TIME_1721799879000_END
levelscriptVersion 8
COLORS 154
grav 1 270
y 1300 1500 1 1 1
< 0
tmc 1500 1500 10 10 0 0 1
off
< 1
tmc 1500 1500 10 10 0 0 1
off
< 2
> 0
> 1
r 0 0 0 0 0
< 3
"""