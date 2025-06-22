from .object import Object as _Object
from .objects import Rectangle, RectangleGenerator, RotatableRectangle, SpringyRectangle, GrowingRectangle, MoveableRectangle


class ObjectGroup:

    def __init__(self, objs: list[_Object]):
        """Group of objects that can be manipulated together."""
        self.objs = objs
        self._primary_position = (int(objs[0].attributes[1]), int(objs[0].attributes[2]))
        self._position_offsets = []
        self._find_position_offsets()

    def _find_position_offsets(self):
        for obj in self.objs:
            self._find_position_offset(obj)

    def _find_position_offset(self, obj):
        pos = []
        num = obj.number_of_positions
        for i in range(1, num * 2 + 1, 2):
            this_position = [int(obj.attributes[i]) - self._primary_position[0],
                             int(obj.attributes[i + 1]) - self._primary_position[1]]

            if isinstance(obj, Rectangle):
                if isinstance(obj, RotatableRectangle):
                    # Seriously why tf is this not the same as the rest
                    this_position[0] -= int(obj.attributes[3]) / 2
                    this_position[1] -= int(obj.attributes[4]) / 2
                else:
                    this_position[0] -= int(obj.attributes[3])
                    this_position[1] -= int(obj.attributes[4])

            pos.append(tuple(this_position))

        self._position_offsets.append(pos)

    def add(self, obj: _Object | list):
        """Insert a new object at the end of the group."""
        if isinstance(obj, list):
            self._add_all(obj)
        elif isinstance(obj, _Object):
            self.objs.append(obj)
            self._find_position_offset(obj)
        else:
            raise TypeError(f"Can only add a ch Object or list of ch Objects to an ObjectGroup")

    def _add_all(self, objs: list[_Object, ...]):
        """Add all objects of a list."""
        for obj in objs:
            self.add(obj)

    def set_position(self, pos: tuple[..., ...]):
        """
        Set the position of each object in the group.
        :param pos:     New position of first object in the group
        """

        # Set position of primary object.
        match self.objs[0].number_of_positions:
            case 0:
                pass
            case 1:
                self.objs[0].set_position(pos)
            case 2:
                self.objs[0].set_position(pos, pos)
            case 3:
                self.objs[0].set_position(pos, pos, pos)
            case 4:
                self.objs[0].set_position(pos, pos, pos, pos)

        for i in range(len(self.objs) - 1):
            # Set positions of remaining objects according to offsets.

            obj = self.objs[i + 1]
            offset = self._position_offsets[i + 1]
            num = obj.number_of_positions

            if num <= 0:
                # Object does not have any positions (connections)
                continue

            pos_1 = None
            pos_2 = None
            pos_3 = None
            pos_4 = None

            if num >= 1:
                pos_1 = (pos[0] + offset[0][0], pos[1] + offset[0][1])

            if num >= 2:
                pos_2 = (pos[0] + offset[1][0], pos[1] + offset[1][1])

            if num >= 3:
                pos_3 = (pos[0] + offset[2][0], pos[1] + offset[2][1])

            if num >= 4:
                pos_4 = (pos[0] + offset[3][0], pos[1] + offset[3][1])

            obj.set_position(pos_1, pos_2, pos_3, pos_4)

    def __str__(self):
        output = []
        for obj in self.objs:
            output.append(obj.to_str(enumeration=True))
        return '\n'.join(output)

    def copy(self):
        """Return a deep copy of an ObjectGroup instance."""
        new_objs = [obj.copy() for obj in self.objs]
        new_group = ObjectGroup(new_objs)
        return new_group

    def duplicate(self, pos: tuple[..., ...]):
        """Copy the group to a new position."""
        new_group = self.copy()
        new_group.set_position(pos)
        return new_group
