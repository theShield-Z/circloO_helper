from object import Object


class Player(Object):
    def __init__(self, x_pos, y_pos, size=1, speed=1, density=1, bullet=True):
        super().__init__(['y', x_pos, y_pos, size, speed, density])
        if bullet:
            self.modifiers.append('bullet')

# SOLID OBJECTS ########################################################################################################


class Circle(Object):
    def __init__(self, x_pos, y_pos, radius, attractor=0):
        super().__init__(['c', x_pos, y_pos, radius])
        if attractor != 0:
            self.add_modifier([f"attr {attractor}"])


class Box(Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0):
        """
        :param x_pos: measured at center
        :param y_pos: measured at center
        :param width: half of displayed width
        :param height: half of displayed height
        :param rotation:
        """
        super().__init__(['b', x_pos, y_pos, width, height, rotation])


class Triangle(Object):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        super().__init__(['t', x1, y1, x2, y2, x3, y3])


class Line(Object):
    def __init__(self, x1, y1, x2, y2, thickness=3):
        super().__init__(['l_at', x1, y1, x2, y2, thickness])


class Arc(Object):
    """Arcs are confusing as hell. No support for 3-point arcs atm."""
    def __init__(self, x_pos, y_pos, start_pos, end_pos, radius, thickness=3):
        super().__init__(['/ LE_ARC_DESCRIPTION', x_pos, y_pos, start_pos, end_pos, radius, -1, -1, 2, thickness])  # seriously what are the -1's and 2 for???


class Curve(Object):
    def __init__(self, start_x, start_y, ctr1_x, ctr1_y, ctr2_x, ctr2_y, end_x, end_y, thickness=3, resolution=100):
        super().__init__(['curve', start_x, start_y, ctr1_x, ctr1_y, ctr2_x, ctr2_y, end_x, end_y, thickness, resolution])


class GrowingCircle(Object):
    def __init__(self, x_pos, y_pos, radius, keep_pos=False):
        super().__init__(['gc', x_pos, y_pos, radius])
        if keep_pos:
            self.add_modifier("samePosition")


class GrowingRectangle(Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, keep_pos=False):
        super().__init__(['rGr', x_pos, y_pos, width, height, rotation])
        if keep_pos:
            self.add_modifier("samePosition")

# MOVEABLE OBJECTS #####################################################################################################
#   side note: 'movable' is spelled wrong in the whole game, so I will spell it wrong here too lol


class MoveableCircle(Object):
    def __init__(self, x_pos, y_pos, radius, density=1, damping=0, wheel_image=False):
        super().__init__(['mc', x_pos, y_pos, radius, density, damping])
        if wheel_image:
            self.add_modifier("wheelsprite")


class MoveableRectangle(Object):
    def __init__(self, x_pos, y_pos, width, height, density=1, damping=-1, rotation=0, fix_rotation=False):
        """
        :param x_pos:   x at center
        :param y_pos:   x at center
        :param width:   half of width shown in editor
        :param height:  half of height shown in editor
        :param density:
        :param damping:
        :param fix_rotation:
        """
        super().__init__(['mb', x_pos, y_pos, width, height, density, damping, rotation, damping])
        if fix_rotation:
            self.add_modifier("fixrot")


class MoveableTriangle(Object):
    def __init__(self, x1, y1, x2, y2, x3, y3, density=1, fix_rotation=False):
        super().__init__(['mt', x1, y1, x2, y2, x3, y3, density])
        if fix_rotation:
            self.add_modifier("fixrot")

# SPECIAL OBJECTS ######################################################################################################


class RotatableRectangle(Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, density=1, damping=0):
        """
        :param x_pos:   x at center
        :param y_pos:   y at center
        :param width:   full width as shown in editor
        :param height:  full height as shown in editor
        :param rotation:
        :param density:
        :param damping:
        """
        super().__init__(['rr', x_pos, y_pos, width, height, rotation, density, damping])


class RotatableCircle(Object):
    def __init__(self, x_pos, y_pos, radius, motor_speed=0, torque=100):
        super().__init__(['rc', x_pos, y_pos, radius, motor_speed, torque])


class SpringyRectangle(Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, density=1, frequency=2, damping=.3, fulcrum_offset=0, fulcrum_radius=10):
        super().__init__(['wr', x_pos, y_pos, width, height, rotation, density, frequency, damping, fulcrum_offset, fulcrum_radius])


class BallGenerator(Object):
    def __init__(self, x_pos, y_pos, radius, density=1, disappear_after=5, wait_between=1, init_delay=0, damping=0, no_fade=False, start_off=False):
        super().__init__(['tmc', x_pos, y_pos, radius, density, disappear_after*60, wait_between*60, init_delay*60])
        if damping != 0:
            self.add_modifier(f"damping {damping}")
        if no_fade:
            self.add_modifier("noanim")
        if start_off:
            self.add_modifier("off")


class RectangleGenerator(Object):
    def __init__(self, x_pos, y_pos, width, height, density=1, rotation=0, damping=0, disappear_after=5,
                 wait_between=1, init_delay=0, fix_rotation=False, no_fade=False, start_off=False):
        super().__init__(['tmb', x_pos, y_pos, width, height, density, damping, rotation, damping, disappear_after*60, wait_between*60, init_delay*60])
        if fix_rotation:
            self.add_modifier('fixrot')
        if no_fade:
            self.add_modifier('noanim')
        if start_off:
            self.add_modifier('off')


class Portal(Object):
    def __init__(self, portal_x, portal_y, target_x, target_y, deactivate_circle=7, min_time=0):
        # I can't figure out what the extra '1' is for.
        super().__init__(['portal', portal_x, portal_y, target_x, target_y, 1, deactivate_circle, min_time])

# CONNECTIONS ##########################################################################################################


class Glue(Object):
    def __init__(self, obj1, obj2):
        super().__init__(['/ GLUE', obj1, obj2])


class Rope(Object):
    def __init__(self, obj1, obj2, offset1_x=0, offset1_y=0, offset2_x=0, offset2_y=0, max_length=0):
        """

        :param obj1:
        :param obj2:
        :param offset1_x:   offset from obj 1
        :param offset1_y:   offset from obj 1
        :param offset2_x:   offset from obj 2
        :param offset2_y:   offset from obj 2
        :param max_length:
        """
        super().__init__(['r', offset1_x, offset1_y, offset2_x, offset2_y, max_length])
        self.set_connections([obj1, obj2])


class Pulley(Object):
    def __init__(self, obj1, obj2, pulley1_x=0, pulley1_y=-100, pulley2_x=0, pulley2_y=-100,
                 offset1_x=0, offset1_y=0, offset2_x=0, offset2_y=0, ratio=1, unlock_movement=False):
        """
        Note that the offsets are unavailable in the editor, and they can be buggy if not set to 0.
        :param obj1:
        :param obj2:
        :param pulley1_x: location of first pulley, relative to obj1
        :param pulley1_y: location of first pulley, relative to obj1
        :param pulley2_x: location of first pulley, relative to obj2
        :param pulley2_y: location of first pulley, relative to obj2
        :param offset1_x: offset of connection to obj1
        :param offset1_y: offset of connection to obj1
        :param offset2_x: offset of connection to obj2
        :param offset2_y: offset of connection to obj2
        :param ratio: how 'strongly' the right side pulls compared to the left
        :param unlock_movement: allow for horizontal movement of the pullies
        """
        super().__init__(['/ p_description', offset1_x, offset1_y, offset2_x, offset2_y, pulley1_x, pulley1_y, pulley2_x, pulley2_y, ratio])
        self.set_connections([obj1, obj2])
        if unlock_movement:
            self.add_modifier("p_free_hmovement")


class Hinge(Object):
    def __init__(self, obj1, obj2, offset_x=0, offset_y=0, draw_connection_line=False, enable_collisions=False, motor_speed=0, torque=100):
        """
        :param obj1:
        :param obj2:
        :param offset_x:    offset from obj 1
        :param offset_y:    offset from obj 1
        :param draw_connection_line:
        :param enable_collisions:
        :param motor_speed:
        :param torque:
        """
        super().__init__(['hinge', offset_x, offset_y, int(draw_connection_line), int(enable_collisions), motor_speed, torque])
        self.set_connections([obj1, obj2])


class Slider(Object):
    def __init__(self, obj1, obj2, offset_x, offset_y):
        """

        :param obj1:
        :param obj2:
        :param offset_x:    offset from obj 1
        :param offset_y:    offset from obj 1
        """
        # I can't figure out what the other 4 attributes do.
        super().__init__(['pr', 1.00, -0.00, -1, -1, offset_x, offset_y])
        self.set_connections([obj1, obj2])


class SpecialConnection(Object):
    def __init__(self, collectable, target, action):
        """
        Supported Actions:
            'Disconnect' - disconnects ropes & hinges (currently crashes game),
            'Follow' - sets camera to follow object,
            'Reset' - enables & resets timer of generators,
            'Now' - generates one object from a generator,
            'On' - enables generator or portal,
            'Off' - disables generator or portal,
            'Teleport' - teleports player to end point of connected portal
        :param collectable:
        :param target:
        :param action:
        """
        super().__init__(['spc', action])
        self.set_connections([collectable, target])

# COLLECTABLES #########################################################################################################


class Collectable(Object):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """

        :param x_pos:
        :param y_pos:
        :param appear_at_segment:
        :param part_of_segment:
        :param zoom: -1 --> no change, -2 --> full level
        :param is_trigger:
        """
        tag = 'io' if collect_from_object else 'i'
        super().__init__([f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)

    def init_modifiers(self, part_of_segment, zoom, is_trigger):
        if part_of_segment != 0:
            self.add_modifier(f"iGrow {part_of_segment}")
        if zoom != -1:
            self.add_modifier(f"zoomFactor {zoom}")
        if is_trigger:
            self.add_modifier("trigger")

    def set_sound(self, group, note, volume, pitch, play_if_no_function):
        """
        :param group:
        :param note:
        :param volume:
        :param pitch:
        :param play_if_no_function: -1 --> Auto, 1 --> Yes, 0 --> No
        :return:
        """
        self.add_modifier(f"sfx '{group}{note}' {volume} {pitch} {play_if_no_function}")


class GravityCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, grav_dir=270, grav_strength=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        tag = 'im' if collect_from_object else 'ig'
        Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, grav_dir, grav_strength])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SizeCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, size=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        tag = 'iso' if collect_from_object else 'is'
        Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, size])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class DisconnectCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        tag = 'irbo' if collect_from_object else 'irb'
        Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SpeedClt(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, speed=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        tag = 'ipso' if collect_from_object else 'ips'
        Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, speed])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SpecialClt(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        tag = 'ispo' if collect_from_object else 'isp'
        Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)

