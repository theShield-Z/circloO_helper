from random import randint
from object import Object


class Level:

    def __init__(self, segments=7, grav_scale=1, grav_dir=270, start_full=False, color=randint(0, 255), music=(0, 0), rec_sfx=False, objs=None):
        """
        :param segments:    Number of collectables before level is completed
        :param grav_scale:  Strength of initial gravity
        :param grav_dir:    Direction of initial gravity
        :param start_full:  Start the level as full
        :param color:       Level color, 0-255
        :param music:       Played music track; (1, track) for preferred or (2, track) to force.
        :param rec_sfx:     Set to true to ask players to enable sfx
        """
        if objs is None:
            objs = []
        self.objs = objs

        # Header variables.
        self.segments = segments
        self.grav_scale = grav_scale
        self.grav_dir = grav_dir
        self.start_full = start_full
        self.color = color
        self.music = music
        self.rec_sfx = rec_sfx

    def add(self, obj):
        new_obj = obj.copy()
        new_obj.set_id(self.get_last_line())
        self.objs.append(new_obj)

    def insert(self, line, obj):
        new_obj = obj.copy()
        new_obj.set_id(line)
        self.objs.insert(line, new_obj)
        for obj_line in range(line+1, self.get_last_line()):
            self.objs[obj_line].increment_id()

    def replace(self, line, obj):
        new_obj = obj.copy()
        new_obj.set_id(line)
        self.objs[line] = new_obj

    def remove(self, line):
        self.objs.pop(line)
        for obj_line in range(line, self.get_last_line()):
            self.objs[obj_line].increment_id(-1)

    def object_at(self, line):
        return self.objs[line]

    def get_last_line(self):
        return len(self.objs)

    def make_header(self):
        txt = ("/\n"
               "/ circloO level\n"
               "/ Made with circloO Level Editor\n"
               f"totalCircles {self.segments} {int(self.start_full)}\n"
               f"/ EDITOR_TOOL {1} {'select'}\n"
               f"/ EDITOR_VIEW {1500} {1500} {1}\n"
               "/ EDT 3303\n"
               "/ _SAVE_TIME_1721799879000_END\n"
               "levelscriptVersion 8\n"
               f"COLORS {self.color}\n"
               f"grav {self.grav_scale} {self.grav_dir}")
        if self.rec_sfx:
            txt += "\nrecommend_sfx"
        if self.music[0] != 0:
            txt += f"\nmusic {self.music[0]} {self.music[1]}"

        return txt

    def to_str(self):
        text = []
        text.append(self.make_header())
        for i in range(self.get_last_line()):
            text.append(self.objs[i].to_str(enumeration=True))

        return '\n'.join(text)

    def __str__(self):
        return self.to_str()

    def __add__(self, other):
        lvl = Level(self.segments, self.grav_scale, self.start_full)
        lvl.objs = self.objs + other.objs
        return lvl

    def to_file(self, path):
        with open(path, 'w') as f:
            f.writelines(self.to_str())
        print(f"Successfully converted level to file under {path}")
