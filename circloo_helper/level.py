from random import randint
from object import Object


class Level:

    def __init__(self,
                 segments: int | float = 7,
                 grav_scale: int | float = 1,
                 grav_dir: int | float = 270,
                 start_full: bool = False,
                 color: int | float = randint(0, 255),
                 music: tuple[int, int] = (0, 0),
                 rec_sfx: bool = False):
        """
        circloO Level
        :param segments:    Number of collectables to collect before level is completed; default is 7
        :param grav_scale:  Strength of initial gravity; default is 1
        :param grav_dir:    Direction of initial gravity; default is 270 (down)
        :param start_full:  Start the level as full; default is False
        :param color:       Level color, 0-255; default is random
        :param music:       Played music track; (1, track) for preferred or (2, track) to force; track 4 is silence; default is (0, 0)
        :param rec_sfx:     Set to true to ask players to enable sfx; default is False
        """
        self.objs = []

        # Header variables.
        self.segments = segments
        self.grav_scale = grav_scale
        self.grav_dir = grav_dir
        self.start_full = start_full
        self.color = color
        self.music = music
        self.rec_sfx = rec_sfx

    # OBJECTS ##########################################################################################################

    def add(self, obj: Object):
        """Insert a new object at the end of the level."""
        new_obj = obj.copy()
        new_obj.set_id(self.get_len())
        self.objs.append(new_obj)

    def insert(self, line: int, obj: Object):
        """Insert a new object at the given line."""
        new_obj = obj.copy()
        new_obj.set_id(line)
        self.objs.insert(line, new_obj)

        # Shift ids of following objects.
        for obj_line in range(line + 1, self.get_len()):
            self.objs[obj_line].increment_id()

    def replace(self, line: int, obj: Object) -> Object:
        """Replace an object at the given line with a new object.
        :return: previous object at the given line."""
        new_obj = obj.copy()
        new_obj.set_id(line)
        old_obj = self.objs[line]
        self.objs[line] = new_obj
        return old_obj

    def remove(self, line: int) -> Object:
        """Remove an object at the given line.
        :return: removed object"""
        old_obj = self.objs.pop(line)

        # Shift ids of following objects.
        for obj_line in range(line, self.get_len()):
            self.objs[obj_line].increment_id(-1)

        return old_obj

    def object_at(self, line: int) -> Object:
        """:return: object at the given line"""
        return self.objs[line]

    def get_len(self) -> int:
        """:return: size of level"""
        return len(self.objs)

    # VIEWING/EXPORTING ################################################################################################

    def make_header(self) -> str:
        """Convert level settings into a string header.
        :return: header string"""
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

    def to_str(self) -> str:
        text = []
        text.append(self.make_header())

        # Append each object in objs to level
        for i in range(self.get_len()):
            text.append(self.objs[i].to_str(enumeration=True))

        return '\n'.join(text)

    def __str__(self) -> str:
        return self.to_str()

    def to_file(self, path: str):
        with open(path, 'w') as f:
            f.writelines(self.to_str())
        print(f"Successfully converted level to file under {path}")
