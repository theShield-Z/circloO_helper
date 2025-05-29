import circloo_helper as ch


# Basic #
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
collectable.set_sound('house', 0)   # Change collectable's sfx to a chime
lvl.add(collectable)

lvl.to_file("examples/example_level.txt")


# Parsing #
with open("examples/parse_example.txt", 'r') as f:
    lvl = ch.parse(f.read())
    lvl.remove_all('tmc')   # Remove all circle generators
    lvl.add(ch.objects.Collectable(1830, 1630))
    lvl.to_file("examples/fixed_level.txt")


# Mechanisms #
lvl = ch.Level(segments=2, start_full=True)
#   Create right/left detector
rl = ch.mechanisms.LeftRightDetector(1500, 1300, lvl.get_len())
rl.add_to(lvl)
#   Create ring counter
counter = ch.mechanisms.RingCounter(1400, 1500, 5, lvl.get_len())
counter.add_to(lvl)
#   Connect right/left detector to counter so that counter increases when right is pressed
trigger_1 = ch.objects.SpecialCollectable(1470, 1250, is_trigger=True, collect_from_object=True)
generator_1 = ch.objects.BallGenerator(1675, 1500, 15, density=0, disappear_after=.1, start_off=True)
trig_gen_conn = ch.objects.SpecialConnection(40, 41, 'NowIf')   # Generate ball when Right pressed

lvl.add(trigger_1)
lvl.add(generator_1)
lvl.add(trig_gen_conn)

lvl.to_file("examples/mechanism_level.txt")
