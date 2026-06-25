import circloo_helper as ch
from circloo_helper.circloo_objects import *


# BASIC WORKFLOW #######################################################################################################

# Create a level.
lvl = ch.Level(segments=1, color=160)

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
print(lvl.to_clipboard())   # Print the level and copy it to the clipboard
lvl.to_file("basic_workflow.txt")


# PARSING ##############################################################################################################

lvl = ch.read_file("gap_level.txt")

# Close the gap.
lvl.add(MoveableTriangle(1325, 1600, 1675, 1600, 1500, 1550))

lvl.to_file("parsing.txt")


# CUSTOM OBJECT CREATION ###############################################################################################

class House(ch.CustomObject, ch.object_types.Solid, ch.object_shapes.Other):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def build_objs(self):
        super().build_objs()

        width = height = 50
        self._obj_cache.append(SolidRectangle(self.x, self.y, width, height))
        self._obj_cache.append(SolidTriangle(self.x - 10, self.y,
                                             self.x + width + 10, self.y,
                                             self.x + width/2, self.y - 20))

        return self._obj_cache


lvl = ch.Level(segments=1)

lvl.add(House(1400, 1500))
lvl.add(House(1500, 1500))
lvl.add(House(1600, 1500))

lvl.to_file("custom_object_creation.txt")


# TOOLS ################################################################################################################

lvl = ch.Level(segments=1)

center = ch.polar(100, 225)
c = SolidCircle(*center, radius=1)

for i in range(0, 360, 10):
    circle = ch.pivot(c, i, 1500, 1500)
    scaled_circle = ch.scale(circle, i / 10 + 1)
    lvl.add(scaled_circle)

lvl.to_file("tools.txt")


# TEXT #################################################################################################################

lvl = ch.Level(segments=5, start_full=True)

text = ("Hello, world!\n\r"
        "This is some text that will be added to circloO :)\n\r"
        "The quick brown fox jumps over the lazy dog.")

lvl.add(ch.Text(text, SolidRectangle(600, 1500, 10, 10)))

lvl.to_file("text.txt")


# IMAGE CONVERSION #####################################################################################################

lvl = ch.Level(segments=2, start_full=True)

img = ch.CHImage("mona_lisa.webp",
                 SolidRectangle(1100, 900, 10, 10),
                 4)

lvl.add(img)
lvl.to_file("image_conversion.txt")


# VIDEO CONVERSION #####################################################################################################

lvl = ch.Level(segments=2, start_full=True, color=130)

vid = ch.CHVideo("Dancing Rick Astley Loop.mp4",
                 RectangleGenerator(1300, 1350, 5, 5, density=0, no_fade=True),
                 (80, 60),
                 5)

lvl.add(vid)

# Set up viewing.
lvl.add(Player(1500, 1850))
lvl.add(Collectable(1500, 1850, zoom=-2, is_trigger=True, disable_on_trigger=True))

lvl.to_file("video_conversion.txt")


# AUDIO CONVERSION #####################################################################################################

lvl = ch.Level(segments=20, start_full=True, color=150, grav_scale=0)

midi = ch.CHMIDI("Stereo Madness.mid", pitch=2)

lvl.add(midi)

# Set up viewing.
lvl.add(Player(1450, 1450))
lvl.add(Collectable(1450, 1450, zoom=-2, is_trigger=True, disable_on_trigger=True))

lvl.to_file("audio_conversion.txt")


########################################################################################################################
