from .object import Object as _O


class _ObjectType(_O):
    def __init__(self):
        super().__init__()


class Solid(_ObjectType):
    pass


class Moveable(_ObjectType):
    def __init__(self):
        super().__init__()
        self.density: int | float = 1
        self.damping: int | float = 0
        self.fix_rotation: bool = False
        self.bullet: bool = False

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.fix_rotation:
            self._add_modifier("fixrot")
        if self.bullet:
            self._add_modifier("bullet")


class Generator(_ObjectType):
    def __init__(self):
        super().__init__()
        self.disappear_after: int | float = 5
        self.wait_between: int | float = 1
        self.init_delay: int | float = 0
        self.no_fade: bool = False
        self.start_off: bool = False

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.no_fade:
            self._add_modifier("noanim")
        if self.start_off:
            self._add_modifier("off")


class Growing(_ObjectType):
    def __init__(self):
        super().__init__()
        self.keep_pos: bool = False

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.keep_pos:
            self._add_modifier("samePosition")


class Rotatable(_ObjectType):
    def __init__(self):
        super().__init__()
        self.motor_speed: int | float = 0
        self.torque: int | float = 100
