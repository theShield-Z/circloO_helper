from .object import Object as _Object


class Player(_Object):
    def __init__(self, x_pos, y_pos, size=1, speed=1, density=1, bullet=True):
        """
        The circle that you control with left & right.
        :param x_pos:   Position of center
        :param y_pos:   Position of center
        :param size:    Radius of circle; default is 1
        :param speed:   Player speed; default is 1
        :param density: Circle density (how much it is affected by gravity); default is 1
        :param bullet:  if True, enables setting to improve high-speed physics; default is True
        """
        super().__init__(['y', x_pos, y_pos, size, speed, density])
        if bullet:
            self.modifiers.append('bullet')

# SOLID OBJECTS ########################################################################################################


class Circle(_Object):
    def __init__(self, x_pos, y_pos, radius, attractor=0):
        """
        Immovable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        """
        super().__init__(['c', x_pos, y_pos, radius])
        if attractor != 0:
            self.add_modifier(f"attr {attractor}")


class Rectangle(_Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0):
        """
        Immovable Rectangle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param width:       Half of displayed width (measured radially from center)
        :param height:      Half of displayed height (measured radially from center)
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        """
        super().__init__(['b', x_pos, y_pos, width, height, rotation])


class Triangle(_Object):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        """
        Immovable Triangle
        :param x1: Position of 1st point
        :param y1: Position of 1st point
        :param x2: Position of 2nd point
        :param y2: Position of 2nd point
        :param x3: Position of 3rd point
        :param y3: Position of 3rd point
        """
        super().__init__(['t', x1, y1, x2, y2, x3, y3])


class Line(_Object):
    def __init__(self, x1, y1, x2, y2, thickness=3):
        """
        Solid Line
        :param x1:          Position of 1st point
        :param y1:          Position of 1st point
        :param x2:          Position of 2nd point
        :param y2:          Position of 2nd point
        :param thickness:   Thickness of line; default is 3
        """
        super().__init__(['l_at', x1, y1, x2, y2, thickness])


class Arc(_Object):
    """Arcs are confusing as hell. No support for 3-point arcs atm."""
    def __init__(self, x_pos, y_pos, start_pos, end_pos, radius, ctr_x=-1, ctr_y=-1, thickness=3):
        """
        Circular arc (outer edge of a circle)
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param start_pos:   Starting angle in degrees
        :param end_pos:     Ending angle in degrees
        :param radius:      Radius of circle
        :param ctr_x:       Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
        :param ctr_y:       Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
        :param thickness:   Thickness of outer edge; default is 3
        """
        # The function of the extra '2' is unclear
        super().__init__(['/ LE_ARC_DESCRIPTION', x_pos, y_pos, start_pos, end_pos, radius, ctr_x, ctr_y, 2, thickness])


class Curve(_Object):
    def __init__(self, start_x, start_y, ctr1_x, ctr1_y, ctr2_x, ctr2_y, end_x, end_y, thickness=3, resolution=100):
        """
        Bézier Curve
        :param start_x:     Position of starting point
        :param start_y:     Position of starting point
        :param ctr1_x:      Position of 1st control point
        :param ctr1_y:      Position of 1st control point
        :param ctr2_x:      Position of 2nd control point
        :param ctr2_y:      Position of 2nd control point
        :param end_x:       Position of ending point
        :param end_y:       Position of ending point
        :param thickness:   Thickness of line; default is 3
        :param resolution:  Béziers are made up of smaller lines. Resolution is how many smaller lines there are; default is 100
        """
        super().__init__(['curve', start_x, start_y, ctr1_x, ctr1_y, ctr2_x, ctr2_y, end_x, end_y, thickness, resolution])


class GrowingCircle(_Object):
    def __init__(self, x_pos, y_pos, radius, keep_pos=False, attractor=0):
        """
        Solid circle that grows when a collectable is collected
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param keep_pos:    If True, maintain the x- and y-positions. If False, move relative to new level size; default is False
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        """
        super().__init__(['gc', x_pos, y_pos, radius])
        if keep_pos:
            self.add_modifier("samePosition")
        if attractor != 0:
            self.add_modifier(f"attr {attractor}")


class GrowingRectangle(_Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, keep_pos=False):
        """
        Solid rectangle that grows when a collectable is collected
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param width:       Half of displayed width (measured radially from center)
        :param height:      Half of displayed height (measured radially from center)
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param keep_pos:    If True, maintain the x- and y-positions. If False, move relative to new level size; default is False
        """
        super().__init__(['rGr', x_pos, y_pos, width, height, rotation])
        if keep_pos:
            self.add_modifier("samePosition")

# MOVEABLE OBJECTS #####################################################################################################
#   side note: 'movable' is spelled wrong in the whole game, so I will spell it wrong here too lol


class MoveableCircle(_Object):
    def __init__(self, x_pos, y_pos, radius, density=1, damping=0, wheel_image=False, attractor=0):
        """
        Movable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param density:     Density of circle; make 0 to turn solid; default is 1
        :param damping:     How quickly the object is slowed when no force is applied; default is 0
        :param wheel_image: Use the wheel sprite instead of the solid circle sprite if True; default is False
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        """
        super().__init__(['mc', x_pos, y_pos, radius, density, damping])
        if wheel_image:
            self.add_modifier("wheelsprite")
        if attractor != 0:
            self.add_modifier(f"attr {attractor}")


class MoveableRectangle(_Object):
    def __init__(self, x_pos, y_pos, width, height, density=1, damping=-1, rotation=0, fix_rotation=False):
        """
        Movable Rectangle
        :param x_pos:           Position of center
        :param y_pos:           Position of  center
        :param width:           Half of displayed width (measured radially from center)
        :param height:          Half of displayed height (measured radially from center)
        :param density:         Density of rectangle; make 0 to turn solid; default is 1
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param rotation:        Rotation of rectangle; increase to rotate clockwise; default is 0
        :param fix_rotation:    Disable rotation if True; default is False
        """
        super().__init__(['mb', x_pos, y_pos, width, height, density, damping, rotation, damping])
        if fix_rotation:
            self.add_modifier("fixrot")


class MoveableTriangle(_Object):
    def __init__(self, x1, y1, x2, y2, x3, y3, density=1, fix_rotation=False):
        """
        Movable Triangle
        :param x1:              Position of 1st point
        :param y1:              Position of 1st point
        :param x2:              Position of 2nd point
        :param y2:              Position of 2nd point
        :param x3:              Position of 3rd point
        :param y3:              Position of 3rd point
        :param density:         Density of triangle; make 0 to turn solid; default is 1
        :param fix_rotation:    Disable rotation if True; default is False
        """
        super().__init__(['mt', x1, y1, x2, y2, x3, y3, density])
        if fix_rotation:
            self.add_modifier("fixrot")

# SPECIAL OBJECTS ######################################################################################################


class RotatableRectangle(_Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, density=1, damping=0):
        """
        Rotatable Rectangle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param width:       Full width of rectangle (unlike all other rectangle objects)
        :param height       Full height of rectangle (unlike all other rectangle objects)
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param density:     Density of rectangle; default is 1
        :param damping:     How quickly the object is slowed when no force is applied; default is 0
        """
        super().__init__(['rr', x_pos, y_pos, width, height, rotation, density, damping])


class RotatableCircle(_Object):
    def __init__(self, x_pos, y_pos, radius, motor_speed=0, torque=100):
        """
        Rotatable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param motor_speed: Speed of rotation; default is 0
        :param torque:      Torque of rotation; default is 100
        """
        super().__init__(['rc', x_pos, y_pos, radius, motor_speed, torque])


class SpringyRectangle(_Object):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, density=1, frequency=2, damping=.3, fulcrum_offset=0, fulcrum_radius=10):
        """
        Rectangle that returns to a resting position of 0 degrees when rotated
        :param x_pos:           Position of center of rectangle
        :param y_pos:           Position of center of rectangle
        :param width:           Half of displayed width of rectangle (measured radially from its center)
        :param height:          Half of displayed height of rectangle (measured radially from its center)
        :param rotation:        Starting rotation; default is 0. Note that regardless of this value, resting rotation is still 0 degrees.
        :param density:         Density of object; default is 1
        :param frequency:       Frequency of spring; default is 2
        :param damping:         How quickly the object is slowed when no force is applied; default is .3
        :param fulcrum_offset:  Position of fulcrum (point of rotation) relative to rectangle's center; default is 0
        :param fulcrum_radius:  Radius of fulcrum; does not affect rotation; default is 10
        """
        super().__init__(['wr', x_pos, y_pos, width, height, rotation, density, frequency, damping, fulcrum_offset, fulcrum_radius])


class BallGenerator(_Object):
    def __init__(self, x_pos, y_pos, radius, density=1, disappear_after=5, wait_between=1, init_delay=0, damping=0, no_fade=False, start_off=False):
        """
        Generates movable circles at timed intervals.
        :param x_pos:           Position of center
        :param y_pos:           Position of center
        :param radius:          Radius of circle
        :param density:         Density of circle; set to 0 to turn solid; default is 1
        :param disappear_after: Time (in seconds) that circle exists before disappearing; default is 5
        :param wait_between:    Time (in seconds) between a circle disappearing and a new circle generating; default is 1
        :param init_delay:      Time (in seconds) before the generator begins generating circles; defalut is 0
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param no_fade:         If True, disables the fading animation; default is False
        :param start_off:       If True, the generator does not start until triggered with a special connection; default is False
        """
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        super().__init__(['tmc', x_pos, y_pos, radius, density, disappear_after*60, wait_between*60, init_delay*60])
        if damping != 0:
            self.add_modifier(f"damping {damping}")
        if no_fade:
            self.add_modifier("noanim")
        if start_off:
            self.add_modifier("off")


class RectangleGenerator(_Object):
    def __init__(self, x_pos, y_pos, width, height, density=1, rotation=0, damping=0, disappear_after=5,
                 wait_between=1, init_delay=0, fix_rotation=False, no_fade=False, start_off=False):
        """
        Generates movable rectangles at timed intervals.
        :param x_pos:           Position of center
        :param y_pos:           Position of  center
        :param width:           Half of displayed width (measured radially from center)
        :param height:          Half of displayed height (measured radially from center)
        :param density:         Density of rectangle; make 0 to turn solid; default is 1
        :param rotation:        Rotation of rectangle; increase to rotate clockwise; default is 0
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param disappear_after: Time (in seconds) that circle exists before disappearing; default is 5
        :param wait_between:    Time (in seconds) between a circle disappearing and a new circle generating; default is 1
        :param init_delay:      Time (in seconds) before the generator begins generating circles; defalut is 0
        :param fix_rotation:    Disable rotation if True; default is False
        :param no_fade:         If True, disables the fading animation; default is False
        :param start_off:       If True, the generator does not start until triggered with a special connection; default is False
        """
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        super().__init__(['tmb', x_pos, y_pos, width, height, density, damping, rotation, damping, disappear_after*60, wait_between*60, init_delay*60])
        if fix_rotation:
            self.add_modifier('fixrot')
        if no_fade:
            self.add_modifier('noanim')
        if start_off:
            self.add_modifier('off')


class TriangleGenerator(_Object):
    def __init__(self, x1, y1, x2, y2, x3, y3, density=1, disappear_after=5, wait_between=1, init_delay=0, fix_rotation=False, no_fade=False, start_off=False):
        """
        Generates movable triangles at timed intervals.
        :param x1:              Position of 1st point
        :param y1:              Position of 1st point
        :param x2:              Position of 2nd point
        :param y2:              Position of 2nd point
        :param x3:              Position of 3rd point
        :param y3:              Position of 3rd point
        :param density:         Density of triangle; make 0 to turn solid; default is 1
        :param disappear_after: Time (in seconds) that circle exists before disappearing; default is 5
        :param wait_between:    Time (in seconds) between a circle disappearing and a new circle generating; default is 1
        :param init_delay:      Time (in seconds) before the generator begins generating circles; defalut is 0
        :param fix_rotation:    Disable rotation if True; default is False
        :param no_fade:         If True, disables the fading animation; default is False
        :param start_off:       If True, the generator does not start until triggered with a special connection; default is False
        """
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        # The function of the extra -1's is unclear.
        super().__init__(['tmt', x1, y1, x2, y2, x3, y3, density, -1, -1, disappear_after*60, wait_between*60, init_delay*60])
        if fix_rotation:
            self.add_modifier('fixrot')
        if no_fade:
            self.add_modifier('noanim')
        if start_off:
            self.add_modifier('off')


class Portal(_Object):
    def __init__(self, portal_x, portal_y, target_x, target_y, deactivate_circle=7, min_time=0):
        """
        Teleports the player that touches it to a target location.
        :param portal_x:            X coordinate of portal
        :param portal_y:            Y coordinate of portal
        :param target_x:            X coordinate of target location
        :param target_y:            Y coordinate of target location
        :param deactivate_circle:   Circle (number of collected collectables) after which to deactivate portal; default is 7
        :param min_time:            Minimum touch time required for portal to trigger; default is 0
        """
        # The function of the extra '1' is unclear.
        super().__init__(['portal', portal_x, portal_y, target_x, target_y, 1, deactivate_circle, min_time])

# CONNECTIONS ##########################################################################################################


class Glue(_Object):
    def __init__(self, obj1, obj2):
        """
        Glues two movable objects together
        :param obj1: id of obj 1
        :param obj2: id of obj 2
        """
        super().__init__(['/ GLUE', obj1, obj2])


class Rope(_Object):
    def __init__(self, obj1, obj2, offset1_x=0, offset1_y=0, offset2_x=0, offset2_y=0, max_length=0):
        """
        Connect two objects with the ability to move semi-independently
        :param obj1:        id of obj 1
        :param obj2:        id of obj 2
        :param offset1_x:   offset from obj 1; default is 0
        :param offset1_y:   offset from obj 1; default is 0
        :param offset2_x:   offset from obj 2; default is 0
        :param offset2_y:   offset from obj 2; default is 0
        :param max_length:  maximum length the rope can extend beyond the distance between obj1 & obj2; default is 0
        """
        super().__init__(['r', offset1_x, offset1_y, offset2_x, offset2_y, max_length])
        self.set_connections([obj1, obj2])


class PortalRope(_Object):
    """I don't know why this is a separate object?"""
    def __init__(self, obj1, obj2, also_move_destination=False):
        """
        A rope connected between a portal and another object
        :param obj1: id of portal
        :param obj2: id of other object
        :param also_move_destination: if True, also moves destination of portal; default is False
        """
        super().__init__(['fd', int(also_move_destination)])
        self.set_connections([obj1, obj2])


class Pulley(_Object):
    def __init__(self, obj1, obj2, pulley1_x=0, pulley1_y=-100, pulley2_x=0, pulley2_y=-100,
                 offset1_x=0, offset1_y=0, offset2_x=0, offset2_y=0, ratio=1, unlock_movement=False):
        """
        Connect objects via a pulley system.
        Note that the offsets are unavailable in the editor, and they can be buggy if not set to 0.
        :param obj1:            id of first object
        :param obj2:            id of second object
        :param pulley1_x:       location of first pulley, relative to obj1; default is 0
        :param pulley1_y:       location of first pulley, relative to obj1; default is -100
        :param pulley2_x:       location of first pulley, relative to obj2; default is 0
        :param pulley2_y:       location of first pulley, relative to obj2; default is -100
        :param offset1_x:       offset of connection to obj1; default is 0
        :param offset1_y:       offset of connection to obj1; default is 0
        :param offset2_x:       offset of connection to obj2; default is 0
        :param offset2_y:       offset of connection to obj2; default is 0
        :param ratio:           how 'strongly' the right side pulls compared to the left; default is 1
        :param unlock_movement: allow for horizontal movement of the pulleys; default is False
        """
        super().__init__(['/ p_description', offset1_x, offset1_y, offset2_x, offset2_y, pulley1_x, pulley1_y, pulley2_x, pulley2_y, ratio])
        self.set_connections([obj1, obj2])
        if unlock_movement:
            self.add_modifier("p_free_hmovement")


class Hinge(_Object):
    def __init__(self, obj1, obj2, offset_x=0, offset_y=0, draw_connection_line=False, enable_collisions=False, motor_speed=0, torque=100):
        """
        Connect two objects rigidly while allowing rotation.
        :param obj1:                    id of obj 1
        :param obj2:                    id of obj 2
        :param offset_x:                offset of pivot point from obj 1; default is 0
        :param offset_y:                offset of pivot point from obj 1; default is 0
        :param draw_connection_line:    if True, shows a line between the connected objects; default is False
        :param enable_collisions:       if True, enables connected objects to collide with each other; default is False
        :param motor_speed:             speed of rotation; default is 0
        :param torque:                  torque of rotation; default is 100
        """
        super().__init__(['hinge', offset_x, offset_y, int(draw_connection_line), int(enable_collisions), motor_speed, torque])
        self.set_connections([obj1, obj2])


class Slider(_Object):
    def __init__(self, obj1, obj2, offset_x=0, offset_y=0):
        """
        Connect objects rigidly with the ability to move in a straight line between each other.
        :param obj1:        id of obj 1
        :param obj2:        id of obj 2
        :param offset_x:    offset from obj 1; default is 0
        :param offset_y:    offset from obj 1; default is 0
        """
        # The functions of the unassigned attributes are unclear.
        super().__init__(['pr', 1.00, -0.00, -1, -1, offset_x, offset_y])
        self.set_connections([obj1, obj2])


class SpecialConnection(_Object):
    def __init__(self, collectable, target, action):
        """
        Perform an action to a target object upon the collection of a collectable.
        Supported Actions:
            'Disconnect' - disconnects ropes & hinges (currently crashes game),
            'Follow' - sets camera to follow object,
            'Reset' - enables & resets timer of generators,
            'Now' - generates one object from a generator,
            'On' - enables generator or portal,
            'Off' - disables generator or portal,
            'Teleport' - teleports player to end point of connected portal
        :param collectable: id of connected special collectable
        :param target:      id of target object
        :param action:      action to perform on target object
        """
        super().__init__(['spc', action])
        self.set_connections([collectable, target])

# COLLECTABLES #########################################################################################################


class Collectable(_Object):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'io' if collect_from_object else 'i'
        super().__init__([f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)

    def init_modifiers(self, part_of_segment, zoom, is_trigger):
        """
        Initialize object's modifiers
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        """
        if part_of_segment != 0:
            self.add_modifier(f"iGrow {part_of_segment}")
        if zoom != -1:
            self.add_modifier(f"zoomFactor {zoom}")
        if is_trigger:
            self.add_modifier("trigger")

    def set_sound(self, group='', note=0, volume=1, pitch=1, play_if_no_function=False):
        """
        Set sound effect to be played upon collection.
        Supported Groups:
            '' (empty string) - default
            'drum' - percussion
            'piano' - piano
            'house' - miscellaneous
            'none' - silent
        :param group:               Note group to play from; default is ''
        :param note:                Sound number in list of supported notes (does not correspond to pitch); default is 0
        :param volume:              Volume of sound; default is 1
        :param pitch:               Pitch of note; default is 1
        :param play_if_no_function: if True, trigger plays even if it does nothing else; -1 --> Auto, 1 --> Yes, 0 --> No; default is False
        """
        self.add_modifier(f"sfx '{group}{note}' {volume} {pitch} {int(play_if_no_function)}")

    def mute(self):
        self.add_modifier(f"sfx 'none'")


class GravityCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, grav_dir=270, grav_strength=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle that changes gravity.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param grav_dir:            Direction of new gravity; default is 270 (down)
        :param grav_strength:       Strength of new gravity; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'im' if collect_from_object else 'ig'
        _Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, grav_dir, grav_strength])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SizeCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, size=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle that changes player size.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param size:                New size of player; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'iso' if collect_from_object else 'is'
        _Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, size])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class DisconnectCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle that disconnects player from all connections.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'irbo' if collect_from_object else 'irb'
        _Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SpeedCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1, speed=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle that changes player speed.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param speed:               New speed of player; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'ipso' if collect_from_object else 'ips'
        _Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment, speed])
        self.init_modifiers(part_of_segment, zoom, is_trigger)


class SpecialCollectable(Collectable):
    def __init__(self, x_pos, y_pos, appear_at_segment=1,
                 part_of_segment=0, zoom=-1, is_trigger=False, collect_from_object=False):
        """
        Collectable circle that performs an action on an object connected to it via a special connection.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        """
        tag = 'ispo' if collect_from_object else 'isp'
        _Object.__init__(self, [f"ic '{tag}'", x_pos, y_pos, appear_at_segment])
        self.init_modifiers(part_of_segment, zoom, is_trigger)

