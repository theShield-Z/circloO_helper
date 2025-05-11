from random import randint as _randint
from .object import Object as _O


class Level:

    def __init__(self,
                 segments: int | float = 7,
                 grav_scale: int | float = 1,
                 grav_dir: int | float = 270,
                 start_full: bool = False,
                 color: int | float = _randint(0, 255),
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

    def add(self, obj: _O) -> int:
        """Insert a new object at the end of the level."""
        if isinstance(obj, list):
            self._add_all(obj)
        elif isinstance(obj, _O):
            new_obj = obj.copy()
            new_obj.set_id(self.get_len())
            self.objs.append(new_obj)
            return new_obj.get_id()
        else:
            raise TypeError(f"Can only add a ch Object or list of ch Objects to a Level")

    def _add_all(self, objs: list[_O, ...]):
        """Add all objects of a list."""
        for obj in objs:
            self.add(obj)

    def insert(self, line: int, obj: _O):
        """Insert a new object at the given line."""
        new_obj = obj.copy()
        new_obj.set_id(line)
        self.objs.insert(line, new_obj)

        # Shift ids of following objects.
        for obj_line in range(line + 1, self.get_len()):
            self.objs[obj_line].increment_id()

    def replace(self, line: int, obj: _O) -> _O:
        """Replace an object at the given line with a new object.
        :return: previous object at the given line."""
        new_obj = obj.copy()
        new_obj.set_id(line)
        old_obj = self.objs[line]
        self.objs[line] = new_obj
        return old_obj

    def remove(self, line: int) -> _O:
        """Remove an object at the given line.
        :return: removed object"""
        old_obj = self.objs.pop(line)

        # Shift ids of following objects.
        for obj_line in range(line, self.get_len()):
            self.objs[obj_line].increment_id(-1)

        return old_obj

    def remove_all(self, tag: str):
        """Remove all instances of a type of object in the level
        :param tag: tag of the object to be removed"""
        i = self.get_len() - 1
        while i > 0:
            if self.object_at(i).get_tag() == tag:
                self.remove(i)
            i -= 1

    def object_at(self, line: int) -> _O:
        """:return: object at the given line"""
        return self.objs[line]

    def get_len(self) -> int:
        """:return: number of objects in the level"""
        return len(self.objs)

    # OTHER ############################################################################################################

    def _make_header(self) -> str:
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
        """Convert the level into a string"""
        text = []
        text.append(self._make_header())

        # Append each object in objs to level
        for i in range(self.get_len()):
            text.append(self.objs[i].to_str(enumeration=True))

        return '\n'.join(text)

    def __str__(self) -> str:
        return self.to_str()

    def to_file(self, path: str):
        """Save the level to a .txt file"""
        with open(path, 'w') as f:
            f.writelines(self.to_str())
        print(f"Successfully converted level to file under {path}")

    def copy(self):
        """Return a copy of the level."""
        new_level = Level(self.segments, self.grav_scale, self.grav_dir, self.start_full, self.color, self.music, self.rec_sfx)
        for obj in self.objs:
            new_level.add(obj.copy())
        return new_level


def parse(txt: str):
    """Parse an existing level so that you can edit it with this library."""
    split_txt = txt.splitlines(keepends=True)
    lvl = Level()

    # Parse Header.
    for line in split_txt:
        if line.startswith("totalCircles"):
            circles = line[13:].split()
            lvl.segments = float(circles[0])
            lvl.start_full = bool(circles[1])

        elif line.startswith("COLORS"):
            lvl.color = int(line[7:])

        elif line.startswith("grav"):
            gravity = line[5:].split()
            lvl.grav_scale = float(gravity[0])
            lvl.grav_dir = float(gravity[1])

        elif line.startswith("music"):
            lvl.music = tuple(line[6:].split())

        elif line.startswith("recommend_sfx"):
            lvl.rec_sfx = True

        elif line.startswith("<"):
            # Don't loop through the rest of the level.
            break

    # Split Objects.
    obj_list = []
    temp = ''
    for line in split_txt:
        if line.startswith('<') or line.startswith("grav") or line.startswith("music") or line == "recommend_sfx":
            temp += line
            obj_list.append(temp)
            temp = ''
        else:
            temp += line

    # Add Objects to Level.
    for obj_txt in obj_list[1:]:  # index 0 is header
        obj = _O.parse(obj_txt)
        if obj is not None:
            lvl.add(obj)

    return lvl


