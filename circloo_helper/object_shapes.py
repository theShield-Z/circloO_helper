from .object import Object as _O


class _ObjectShape(_O):
    def __init__(self):
        super().__init__()


class Player(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.x: int | float = -1
        self.y: int | float = -1
        self.size: int | float = 1
        self.speed: int | float = 1
        self.density: int | float = 1
        self.restitution: int | float = 0
        self.bullet: bool = True

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.bullet:
            self._add_modifier("bullet")


class Other(_ObjectShape):
    pass


class Circle(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.x: int | float = -1
        self.y: int | float = -1
        self.radius: int | float = -1
        self.attractor: int | float = 0
        self.wheelsprite: bool = False

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.attractor != 0:
            self._add_modifier(f"attr {self.attractor}")
        if self.wheelsprite:
            self._add_modifier("wheelsprite")


class Rectangle(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.x: int | float = -1
        self.y: int | float = -1
        self.width: int | float = -1
        self.height: int | float = -1
        self.rotation: int | float = 0
        self.coords_by_center: bool = False


class Triangle(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.x1: int | float = -1
        self.y1: int | float = -1
        self.x2: int | float = -1
        self.y2: int | float = -1
        self.x3: int | float = -1
        self.y3: int | float = -1


class Line(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.thickness: int | float = 3


class Connection(_ObjectShape):
    def __init__(self):
        super().__init__()
        self.obj1: _O | None = None
        self.obj2: _O | None = None


class Collectable(_ObjectShape):
    class Sound:
        def __init__(self, group='', note=0, volume=1, pitch=1, play_if_no_function=-1):
            """
            Sound that plays when collectable is activated.
            :param group:   Sound type; any of '' (default), 'drum', 'piano', 'house' (assorted), 'none' (mute).
            :param note:    Sound variant; note for piano, instrument for assorted, etc.
            :param volume:  Volume of sound.
            :param pitch:   Pitch of sound.
            :param play_if_no_function: whether sound plays if collectable does nothing else.
                                        -1 --> auto (default), 0 --> no, 1 --> yes
            """
            self.group: str = group
            self.note: int = note
            self.volume: int | float = volume
            self.pitch: int | float = pitch
            self.play_if_no_function: int = play_if_no_function

    def __init__(self):
        super().__init__()
        self.x: int | float = -1
        self.y: int | float = -1
        self.appear_at_segment: int = 1
        self.part_of_segment: int = 0
        self.zoom: int | float = -1
        self.is_trigger: bool = False
        self.collect_from_object: bool = False
        self.start_disabled: bool = False
        self.disable_on_trigger: bool = False
        self.sound: Collectable.Sound | None = None
        self._is_mute: bool = False

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.part_of_segment != 0:
            self._add_modifier(f"iGrow {self.part_of_segment}")
        if self.zoom != -1:
            self._add_modifier(f"zoomFactor {self.zoom}")
        if self.is_trigger:
            self._add_modifier("trigger")
        if self.start_disabled:
            self._add_modifier("off")
        if self.disable_on_trigger:
            self._add_modifier("ott")

        if self._is_mute:
            self._add_modifier("sfx 'none'")
        elif self.sound is not None:
            sound_txt = f"sfx '{self.sound.group}{self.sound.note}'"
            if self.sound.volume != 1 or self.sound.pitch != 1 or self.sound.play_if_no_function != -1:
                sound_txt += f" {self.sound.volume} {self.sound.pitch} {self.sound.play_if_no_function}"
            self._add_modifier(sound_txt)



    def set_sound(self, group='', note=0, volume=1, pitch=1, play_if_no_function=False, sound: Sound = None):
        if sound is not None:
            self.sound = sound
        else:
            self.sound = self.Sound(group, note, volume, pitch, play_if_no_function)

    def mute(self):
        """Toggle mute: Make the collectable silent upon collection, or unmute it if already muted."""
        self._is_mute = not self._is_mute
