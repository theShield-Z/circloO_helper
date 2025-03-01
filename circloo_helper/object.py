class Object:
    def __init__(self, attributes, modifiers=None, connections=None, line=-1):
        if modifiers is None:
            modifiers = []
        if connections is None:
            connections = []
        self.attributes = attributes
        self.modifiers = modifiers
        self.connections = connections      # only used for objects like ropes & hinges that connect two objects
        self.id = line

    def to_str(self, enumeration=False):
        primary = ' '.join(map(str, self.attributes))  # map() applies a function to every item of an iterable
        secondary = ''.join(['\n' + str(m) for m in self.modifiers])  # New lines included here.
        connstr = ""
        if len(self.connections) > 0:
            connstr = f"> {self.connections[0]}\n> {self.connections[1]}\n" # there will only ever be two connections

        line = f"\n< {self.id}" if enumeration else ""

        return connstr + primary + secondary + line

    def __str__(self):
        return self.to_str()

    def set_id(self, line):
        self.id = line

    def get_id(self):
        return self.id

    def set_attributes(self, attributes: list):
        self.attributes = attributes

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    # UNTESTED
    def set_connections(self, connections: list):
        self.connections = connections

    def increment_id(self, num=1):
        self.id += num

    def copy(self):
        return Object(self.attributes, self.modifiers, self.connections, self.id)
