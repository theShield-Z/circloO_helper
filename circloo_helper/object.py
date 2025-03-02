class Object:
    def __init__(self,
                 attributes: list[str, any, ...],
                 modifiers: list[any, ...] = None,
                 connections: list[int, int] = None,
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
        self.connections = connections

    def add_modifier(self, modifier: any):
        self.modifiers.append(modifier)

    # UTILITIES ########################################################################################################

    def copy(self):
        return Object(self.attributes, self.modifiers, self.connections, self.id)

    def to_str(self, enumeration: bool = False) -> str:
        primary = ' '.join(map(str, self.attributes))  # map() applies a function to every item of an iterable
        secondary = ''.join(['\n' + str(m) for m in self.modifiers])  # New lines included here.
        connstr = ""
        if len(self.connections) > 0:
            connstr = f"> {self.connections[0]}\n> {self.connections[1]}\n"  # there will only ever be two connections

        line = f"\n< {self.id}" if enumeration else ""

        return connstr + primary + secondary + line

    def __str__(self) -> str:
        return self.to_str()
