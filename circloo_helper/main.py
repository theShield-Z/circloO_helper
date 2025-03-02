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


