class Object:
    def __init__(self,
                 attributes: list[str, any, ...],
                 modifiers: list[any, ...] = None,
                 connections: list[...] = None,
                 obj_id: int = -1):
        """
        Level object
        :param attributes:  Required properties
        :param modifiers:   Optional properties
        :param connections: Connected objects (maximum of two)
        :param obj_id:      ID number of object
        """
        if modifiers is None:
            modifiers = []
        if connections is None:
            connections = []
        self.attributes = attributes
        self.modifiers = modifiers
        self.connections = connections  # only used for objects like ropes & hinges that connect two objects
        self.id = obj_id

        self.number_of_positions = None

    # ID ###############################################################################################################
    def set_id(self, obj_id: int):
        self.id = obj_id

    def get_id(self) -> int:
        return self.id

    def increment_id(self, num: int = 1):
        self.id += num

    # PROPERTIES #######################################################################################################

    def set_attributes(self, attributes: list[str, any, ...]):
        self.attributes = attributes

    def set_connections(self, connections: list[int, int]):
        if len(connections) == 2:
            self.connections = connections
        else:
            raise ConnectionError("There must be exactly two objects for a connection.")

    def add_modifier(self, modifier: any):
        self.modifiers.append(modifier)

    def get_tag(self):
        if self.attributes[0] == '/':
            return ' '.join(self.attributes[0:2])
        return self.attributes[0]

    def get_position(self):
        match self.number_of_positions:
            case 0:
                return []
            case 1:
                return [(int(self.attributes[1]), int(self.attributes[2]))]
            case 2:
                return [(int(self.attributes[1]), int(self.attributes[2])),
                        (int(self.attributes[3]), int(self.attributes[4]))]
            case 3:
                return [(int(self.attributes[1]), int(self.attributes[2])),
                        (int(self.attributes[3]), int(self.attributes[4])),
                        (int(self.attributes[5]), int(self.attributes[6]))]
            case 4:
                return [(int(self.attributes[1]), int(self.attributes[2])),
                        (int(self.attributes[3]), int(self.attributes[4])),
                        (int(self.attributes[5]), int(self.attributes[6])),
                        (int(self.attributes[7]), int(self.attributes[8]))]
            case _:
                return None

    def set_position(self, pos_1: tuple[..., ...],
                     pos_2: tuple[..., ...] = None,
                     pos_3: tuple[..., ...] = None,
                     pos_4: tuple[..., ...] = None):
        """Changes the position of the object. Note that using this on objects without a position (connections, etc.)
        or with multiple positions (triangles, lines, etc.) may result in error."""

        if self.number_of_positions is None:
            raise Exception(f"Please initialize the number of positions to use function set_position(): {self}")

        if self.number_of_positions == 0:
            raise Exception(f"Object {self} does not have a position variable to change.")
        self.attributes[1] = pos_1[0]
        self.attributes[2] = pos_1[1]

        if pos_2 is not None:
            if self.number_of_positions < 2:
                raise Exception(f"Too many positions entered for object {self}.")
            self.attributes[3] = pos_2[0]
            self.attributes[4] = pos_2[1]

        if pos_3 is not None:
            if self.number_of_positions < 3:
                raise Exception(f"Too many positions entered for object {self}.")
            self.attributes[5] = pos_3[0]
            self.attributes[6] = pos_3[1]

        if pos_4 is not None:
            if self.number_of_positions < 4:
                raise Exception(f"Too many positions entered for object {self}.")
            self.attributes[7] = pos_4[0]
            self.attributes[8] = pos_4[1]

    # UTILITIES ########################################################################################################

    def copy(self):
        new_obj = Object(self.attributes.copy(), self.modifiers.copy(), self.connections.copy(), self.id)       # MAYBE CHANGE ID TO BE -1 FOR EVERY COPY?
        new_obj.number_of_positions = self.number_of_positions
        return new_obj

    def to_str(self, enumeration: bool = False) -> str:
        primary = ' '.join(map(str, self.attributes))
        secondary = ''.join(['\n' + str(m) for m in self.modifiers])  # New lines included here.
        connstr = ""
        if len(self.connections) > 0:
            try:
                connstr = f"> {self.connections[0].get_id()}\n> {self.connections[1].get_id()}\n"
            except:
                raise TypeError(f"Object at id {self.get_id()} has invalid connections: {self.connections}")

        line = f"\n< {self.id}" if enumeration else ""

        return connstr + primary + secondary + line

    def __str__(self) -> str:
        return self.to_str()

    @staticmethod
    def parse(txt: str, lvl):
        lines: list = txt.splitlines()

        if lines[0].startswith("music") or lines[0].startswith("recommend_sfx"):
            # Line incorrectly labeled as an object. Throw away.
            return

        if lines[0][0] == '>':
            # Object is a connection.
            obj = Object(lines[2].split())  # Attributes on line 2 b/c connections are on 0 & 1
            obj.set_connections([lvl.object_at(int(lines[0][2:])), lvl.object_at(int(lines[1][2:]))])   # mmm spaghetti

            for i in range(3, len(lines)-1):
                obj.add_modifier(lines[i])

        else:
            obj = Object(lines[0].split())

            for i in range(1, len(lines)-1):
                obj.add_modifier(lines[i])

        return obj
