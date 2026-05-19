class Object:
    def __init__(self):
        self._id = -1
        self._attributes = []
        self._modifiers = []

    def __repr__(self):
        return self._to_str()

    def _set_id(self, id: int):
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
        if (hasattr(self, 'obj1')
                and hasattr(self, 'obj2')
                and type(self).__name__ != 'Glue'):     # Glue has connections but does not label them the same way.
            connstr = f"> {self.obj1.get_id()}\n> {self.obj2.get_id()}\n"

        line_enumeration = f"\n< {self._id}" if enumeration else ""

        return connstr + primary + secondary + line_enumeration

    def get_id(self) -> int:
        return self._id


class CustomObject:
    def __init__(self):
        super().__init__()
        self._id: int = -1
        self._obj_cache: list[Object | 'CustomObject'] = list()

    def __str__(self):
        return self._to_str(enumeration=True)

    def __len__(self):
        return len(self.build_objs())

    def build_objs(self):
        """
        Creates the Objects that will be added to the Level.
        This method must be overridden in all child classes with the following basic structure:\n
            super().build_objs()\n
            # Implementation / Object definition; each Object should be added to self._obj_cache\n
            return self._obj_cache\n
        """
        self._obj_cache.clear()
        return list()

    def _update_ids(self):
        if self._id == -1:
            return

        cur_id = self._id
        for obj in self._obj_cache:
            obj._set_id(cur_id)
            cur_id += 1

    def _set_id(self, id: int):
        self._id = id

    def get_id(self):
        return self._id

    def _to_str(self, enumeration: bool = False) -> str:
        self.build_objs()
        self._update_ids()

        text = []
        for obj in self._obj_cache:
            text.append(obj._to_str(enumeration=enumeration))

        return '\n'.join(text)
