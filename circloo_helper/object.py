class Object:
    def __init__(self):
        self._id = -1
        self._attributes = []
        self._modifiers = []

    def __repr__(self):
        return self._to_str()

    def get_id(self) -> int:
        return self._id

    def _set_id(self, id: int):
        import traceback
        self._id = id

    def _set_attributes(self, *args):
        """This method must be called in every subclass."""
        self._attributes = list(args)

    def _add_modifier(self, modifier):
        self._modifiers.append(modifier)

    def _update_modifiers(self):
        """This method must be overridden in each subclass that uses modifiers."""
        self._modifiers.clear()

    def _to_str(self, enumeration: bool = False) -> str:
        """This should be overridden in every subclass to call _set_attributes()."""
        self._update_modifiers()
        primary = ' '.join(map(str, self._attributes))
        secondary = ''.join(['\n' + str(m) for m in self._modifiers])  # New lines included here.
        connstr = ""
        if hasattr(self, 'obj1') and hasattr(self, 'obj2'):
            connstr = f"> {self.obj1.get_id()}\n> {self.obj2.get_id()}\n"

        line_enumeration = f"\n< {self._id}" if enumeration else ""

        return connstr + primary + secondary + line_enumeration
