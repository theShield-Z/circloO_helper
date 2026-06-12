from random import randint as _randint
import time
import pyperclip

from .object import Object, CustomObject


class Level:

    def __init__(self,
                 segments: int | float = 7,
                 grav_scale: int | float = 1,
                 grav_dir: int | float = 270,
                 start_full: bool = False,
                 color: int = _randint(0, 255),
                 music: tuple[int, int] = (0, 0),
                 recommend_sfx: bool = False,
                 default_line_thickness: int | float = 3,
                 camera_follow_one_player_only: bool = False,
                 affect_all_players_by_collectables: bool = False,
                 line_extra_width: int | float = 0,
                 gravcontrol: bool = False):
        """
        circloO Level
        :param segments:    Number of collectables to collect before level is completed; default is 7
        :param grav_scale:  Strength of initial gravity; default is 1
        :param grav_dir:    Direction of initial gravity; default is 270 (down)
        :param start_full:  Start the level as full; default is False
        :param color:       Level color, 0-255; default is random
        :param music:       Played music track; (1, track) for preferred or (2, track) to force; track 4 is silence; default is (0, 0)
        :param recommend_sfx:     Set to true to ask players to enable sfx; default is False
        :param default_line_thickness:              Default thickness of new line/curve/arc when placed in-game; default is 3
        :param camera_follow_one_player_only:       If True, only follow one player when there are multiple; default is False
        :param affect_all_players_by_collectables:  If True, affect all players by collectables; default is False
        :param line_extra_width:                    Alter size of sprite for line/curve/arc; can be negative; default is 0
        :param gravcontrol:         If True, control direction of gravity with left/right instead of horizontal speed
        """
        self._objs = []
        self._size = 0
        self._LEVELSCRIPT_VERSION = 10

        # Header variables.
        self.segments = segments
        self.grav_scale = grav_scale
        self.grav_dir = grav_dir
        self.start_full = start_full
        self.color = color % 256

        # Level Modifiers
        ### TODO: change single music parameter to music_mode and music_choice (based on le_import_script)
        self.music = music
        self.recommend_sfx = recommend_sfx
        self.default_line_thickness = default_line_thickness
        self.camera_follow_one_player_only = camera_follow_one_player_only
        self.affect_all_players_by_collectables = affect_all_players_by_collectables
        self.line_extra_width = line_extra_width
        self.gravcontrol = gravcontrol

    def __len__(self):
        return self._size

    def __repr__(self):
        return self._to_str()

    def _make_header(self):
        """
        Convert level settings into a string header.
        :return: header string
        """
        txt = ("/\n"
               "/ circloO level\n"
               "/ Made with circloO Level Editor\n"
               f"totalCircles {self.segments} {int(self.start_full)}\n"
               f"/ EDITOR_TOOL {1} {'select'}\n"
               f"/ EDITOR_VIEW {1500} {1500} {.3}\n"  # Centered, full screen
               f"/ EDT {14400}\n"  # Cannot upload immediately if <14400
               f"/ _SAVE_TIME_{int(time.time())}_END\n"  # Unix time at export
               f"levelscriptVersion {self._LEVELSCRIPT_VERSION}\n"
               f"COLORS {self.color}\n"
               f"grav {self.grav_scale} {self.grav_dir}")

        if self.recommend_sfx:
            txt += "\nrecommend_sfx"
        if self.music[0] != 0:
            txt += f"\nmusic {self.music[0]} {self.music[1]}"
        if self.default_line_thickness != 3:
            txt += f"\n/ LE_DEFAULT_LINE_THICKNESS {self.default_line_thickness}"
        if self.camera_follow_one_player_only:
            txt += "\nfollowOne"
        if self.affect_all_players_by_collectables:
            txt += "\naffectAllPlayersByCollectibles"
        if self.line_extra_width != 0:
            txt += f"\nuse_legacy_line_drawing {self.line_extra_width}"
        if self.gravcontrol:
            txt += "\ngravcontrol"

        return txt

    def _to_str(self) -> str:
        """Convert the level into a string."""
        text = []
        text.append(self._make_header())

        # Append each object in objs to level
        for obj in self._objs:
            text.append(obj._to_str(enumeration=True))

        return '\n'.join(text)

    def add(self, obj: Object | CustomObject):
        """Add an object to the Level."""
        obj._set_id(len(self))
        self._objs.append(obj)

        # Update level size.
        if isinstance(obj, CustomObject):
            self._size += len(obj)
        else:
            self._size += 1

    def object_at(self, index):
        """:return: the object at the given index."""
        return self._objs[index]

    def get_objs(self):
        """:return: list of all objects in the Level."""
        return self._objs

    def to_clipboard(self) -> str:
        """
        Copy level text contents to clipboard.
        Also returns the level text, so you can do print(Level().to_clipboard) to simplify workflows.
        """
        txt = str(self)
        pyperclip.copy(txt)
        return txt

    def to_file(self, path: str):
        """
        Save level text to path.
        """
        txt = str(self)
        with open(path, 'w') as f:
            f.write(txt)
