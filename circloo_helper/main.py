import circloo_helper as ch

lvl = ch.Level(segments=2, start_full=True, color=185)

lvl.add(ch.objects.Player(1500, 1500))  # id=0
lvl.add(ch.objects.Rectangle(1500, 1575, 100, 25))  # id=1
lvl.add(ch.objects.Circle(1500, 1275, 25))  # id=2

generator_1 = ch.objects.BallGenerator(1350, 1300, 25, disappear_after=1, wait_between=3)
generator_2 = ch.objects.BallGenerator(1650, 1300, 25, disappear_after=1, wait_between=3, init_delay=2)
lvl.add(generator_1)    # id=3
lvl.add(generator_2)    # id=4

lvl.add(ch.objects.Rope(2, 3))  # Circle + Gen 1
lvl.add(ch.objects.Rope(2, 4))  # Circle + Gen 2

collectable = ch.objects.Collectable(1500, 1400, collect_from_object=True, is_trigger=True)
collectable.set_sound('house', 0)
lvl.add(collectable)

lvl.to_file("example_level.txt")


# The file should contain the following:
"""example_level.txt
/
/ circloO level
/ Made with circloO Level Editor
totalCircles 2 1
/ EDITOR_TOOL 1 select
/ EDITOR_VIEW 1500 1500 1
/ EDT 3303
/ _SAVE_TIME_1721799879000_END
levelscriptVersion 8
COLORS 185
grav 1 270
y 1500 1500 1 1 1
bullet
< 0
b 1500 1575 100 25 0
< 1
c 1500 1275 25
< 2
tmc 1350 1300 25 1 60 180 0
< 3
tmc 1650 1300 25 1 60 180 120
< 4
> 2
> 3
r 0 0 0 0 0
< 5
> 2
> 4
r 0 0 0 0 0
< 6
ic 'io' 1500 1400 1
trigger
sfx 'house0' 1 1 False
< 7
"""

