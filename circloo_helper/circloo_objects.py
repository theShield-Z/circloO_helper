from warnings import warn as _warn

import circloo_helper.object_types as _ot
import circloo_helper.object_shapes as _os

_INPUT_TRIGGER_MAP = {
    ('left', 'pressed'): 0,
    ('right', 'pressed'): 1,
    ('left', 'released'): 2,
    ('right', 'released'): 3,
    ('both', 'pressed'): 4,
    ('both', 'released'): 5,
    ('left', 'down'): 6,
    ('right', 'down'): 7,
    ('both', 'down'): 8,
    ('every_frame', None): 9,
    ('on_trigger', None): 10
}


class Player(_os.Player):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 size: int | float = 1,
                 speed: int | float = 1,
                 density: int | float = 1,
                 restitution: int | float = 0,
                 bullet: bool = True):
        """
        The circle that you control with left & right.
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param size:        Radius of circle; default is 1
        :param speed:       Player speed; default is 1
        :param density:     Circle density (how much it is affected by gravity); default is 1
        :param restitution: How much the player bounces after hitting a surface; hidden in-game; default is 0
        :param bullet:  if True, enables setting to improve high-speed physics; default is True
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.speed = speed
        self.density = density
        self.restitution = restitution
        self.bullet = bullet

    def _to_str(self, enumeration: bool = False) -> str:
        if self.restitution != 0:
            self._set_attributes('y', self.x, self.y, self.size, self.speed, self.density, self.restitution)
        else:
            self._set_attributes('y', self.x, self.y, self.size, self.speed, self.density)
        return super()._to_str(enumeration)


# SOLID OBJECTS ########################################################################################################

class SolidCircle(_ot.Solid, _os.Circle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 attractor: int | float = 0,
                 wheelsprite: bool = False):
        """
        Immovable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        :param wheelsprite: Use the wheel sprite instead of the solid circle sprite if True; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.attractor = attractor
        self.wheelsprite = wheelsprite

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('c', self.x, self.y, self.radius)
        return super()._to_str(enumeration)


class SolidRectangle(_ot.Solid, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 rotation: int | float = 0,
                 coords_by_center: bool = False):
        """
        Immovable Rectangle
        :param x_pos:       Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:       Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:       Width of Rectangle
        :param height:      Height of Rectangle
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        if self.coords_by_center:
            self._set_attributes('b', self.x, self.y, self.width / 2, self.height / 2, self.rotation)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('b', self.x + half_w, self.y + half_h, half_w, half_h, self.rotation)
        return super()._to_str(enumeration)


class SolidTriangle(_ot.Solid, _os.Triangle):
    def __init__(self,
                 x1: int | float,
                 y1: int | float,
                 x2: int | float,
                 y2: int | float,
                 x3: int | float,
                 y3: int | float):
        """
        Immovable Triangle
        :param x1: Position of 1st point
        :param y1: Position of 1st point
        :param x2: Position of 2nd point
        :param y2: Position of 2nd point
        :param x3: Position of 3rd point
        :param y3: Position of 3rd point
        """
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('t', self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        return super()._to_str(enumeration)


class Line(_ot.Solid, _os.Line):
    def __init__(self,
                 x1: int | float,
                 y1: int | float,
                 x2: int | float,
                 y2: int | float,
                 thickness: int | float = 3):
        """
        Solid Line
        :param x1:          Position of 1st point
        :param y1:          Position of 1st point
        :param x2:          Position of 2nd point
        :param y2:          Position of 2nd point
        :param thickness:   Thickness of line; default is 3
        """
        super().__init__()
        self.x1: int | float = x1
        self.y1: int | float = y1
        self.x2: int | float = x2
        self.y2: int | float = y2
        self.thickness = thickness

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('l_at', self.x1, self.y1, self.x2, self.y2, self.thickness)
        return super()._to_str(enumeration)


class Arc(_ot.Solid, _os.Line):
    def __init__(self,
                 center_x: int | float,
                 center_y: int | float,
                 start_angle: int | float,
                 end_angle: int | float,
                 radius: int | float,
                 ctr_x: int | float = -1,
                 ctr_y: int | float = -1,
                 thickness: int | float = 3):
        """
        Circular arc (outer edge of a circle).
        :param center_x:    Position of center
        :param center_y:    Position of center
        :param start_angle: Starting angle in degrees
        :param end_angle:   Ending angle in degrees
        :param radius:      Radius of circle
        :param ctr_x:       Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
        :param ctr_y:       Position of control point (3-point arc only); set to -1 to keep as center arc; default is -1
        :param thickness:   Thickness of outer edge; default is 3
        """
        super().__init__()
        self.center_x: int | float = center_x
        self.center_y: int | float = center_y
        self.start_angle: int | float = start_angle
        self.end_angle: int | float = end_angle
        self.radius: int | float = radius
        self.ctr_x: int | float = ctr_x
        self.ctr_y: int | float = ctr_y
        self.thickness = thickness

    def _to_str(self, enumeration: bool = False) -> str:
        # The extra 2 value is labeled as precision in the level import script, so in theory it should be the number of
        #   individual lines that make up the arc (like for Béziers), but it appears to have no effect.
        self._set_attributes('/ LE_ARC_DESCRIPTION', self.center_x, self.center_y,
                             360 - self.start_angle, 360 - self.end_angle,
                             self.radius, self.ctr_x, self.ctr_y, 2, self.thickness)
        return super()._to_str(enumeration)


class Curve(_ot.Solid, _os.Line):
    def __init__(self,
                 start_x: int | float,
                 start_y: int | float,
                 ctr1_x: int | float,
                 ctr1_y: int | float,
                 ctr2_x: int | float,
                 ctr2_y: int | float,
                 end_x: int | float,
                 end_y: int | float,
                 thickness: int | float = 3,
                 resolution: int | float = 100):
        """
        Cubic Bézier Curve
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
        super().__init__()
        self.start_x: int | float = start_x
        self.start_y: int | float = start_y
        self.ctr1_x: int | float = ctr1_x
        self.ctr1_y: int | float = ctr1_y
        self.ctr2_x: int | float = ctr2_x
        self.ctr2_y: int | float = ctr2_y
        self.end_x: int | float = end_x
        self.end_y: int | float = end_y
        self.thickness = thickness
        self.resolution: int | float = resolution

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('curve', self.start_x, self.start_y, self.ctr1_x, self.ctr1_y,
                             self.ctr2_x, self.ctr2_y, self.end_x, self.end_y, self.thickness, self.resolution)
        return super()._to_str(enumeration)


class GrowingCircle(_ot.Growing, _os.Circle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 keep_pos: bool = False,
                 attractor: int | float = 0,
                 wheelsprite: bool = False):
        """
        Solid circle that grows when a collectable is collected
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param keep_pos:    If True, maintain the x- and y-positions. If False, move relative to new level size; default is False
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        :param wheelsprite: Use the wheel sprite instead of the solid circle sprite if True; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.keep_pos = keep_pos
        self.attractor = attractor
        self.wheelsprite = wheelsprite

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('gc', self.x, self.y, self.radius)
        return super()._to_str(enumeration)


class GrowingRectangle(_ot.Growing, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 rotation: int | float = 0,
                 keep_pos: bool = False,
                 coords_by_center: bool = False):
        """
        Solid rectangle that grows when a collectable is collected
        :param x_pos:       Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:       Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:       Width of Rectangle
        :param height:      Height of Rectangle
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param keep_pos:    If True, maintain the x- and y-positions. If False, move relative to new level size; default is False
        :param coords_by_center:    If True, interprets given position and size as from center of rectangle; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.keep_pos = keep_pos
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        if self.coords_by_center:
            self._set_attributes('rGr', self.x, self.y, self.width / 2, self.height / 2, self.rotation)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('rGr', self.x + half_w, self.y + half_h, half_w, half_h, self.rotation)
        return super()._to_str(enumeration)


# MOVEABLE OBJECTS #####################################################################################################

class MoveableCircle(_ot.Moveable, _os.Circle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 density: int | float = 1,
                 damping: int | float = 0,
                 attractor: int | float = 0,
                 wheelsprite: bool = False,
                 bullet: bool = False):
        """
        Movable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param density:     Density of circle; make 0 to turn solid; default is 1
        :param damping:     How quickly the object is slowed when no force is applied; default is 0
        :param attractor:   Planet gravity; positive pulls movable objects to it, negative pushes away; default is 0
        :param wheelsprite: Use the wheel sprite instead of the solid circle sprite if True; default is False
        :param bullet:      If True, enables setting to improve high-speed physics; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.density = density
        self.damping = damping
        self.wheelsprite = wheelsprite
        self.attractor = attractor
        self.bullet = bullet

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('mc', self.x, self.y, self.radius, self.density, self.damping)
        return super()._to_str(enumeration)


class MoveableRectangle(_ot.Moveable, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 density: int | float = 1,
                 damping: int | float = -1,
                 rotation: int | float = 0,
                 fix_rotation: bool = False,
                 bullet: bool = False,
                 coords_by_center: bool = False):
        """
        Movable Rectangle
        :param x_pos:           Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:           Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:           Width of Rectangle
        :param height:          Height of Rectangle
        :param density:         Density of rectangle; make 0 to turn solid; default is 1
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param rotation:        Rotation of rectangle; increase to rotate clockwise; default is 0
        :param fix_rotation:    Disable rotation if True; default is False
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.density = density
        self.damping = damping
        self.rotation = rotation
        self.fix_rotation = fix_rotation
        self.bullet = bullet
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        # The extra 0 value likely used to be rotational damping, but it is not read in the import script.
        if self.coords_by_center:
            self._set_attributes('mb', self.x, self.y, self.width / 2, self.height / 2,
                                 self.density, 0, self.rotation, self.damping)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('mb', self.x + half_w, self.y + half_h, half_w, half_h,
                                 self.density, 0, self.rotation, self.damping)
        return super()._to_str(enumeration)


class MoveableTriangle(_ot.Moveable, _os.Triangle):
    def __init__(self,
                 x1: int | float,
                 y1: int | float,
                 x2: int | float,
                 y2: int | float,
                 x3: int | float,
                 y3: int | float,
                 density: int | float = 1,
                 fix_rotation: bool = False,
                 bullet: bool = False):
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
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        """
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.density = density
        self.fix_rotation = fix_rotation
        self.bullet = bullet

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('mt', self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.density)
        return super()._to_str(enumeration)


# SPECIAL OBJECTS ######################################################################################################

class RotatableRectangle(_ot.Moveable, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 rotation: int | float = 0,
                 density: int | float = 1,
                 damping: int | float = 0,
                 bullet: bool = False,
                 coords_by_center: bool = False):
        """
        Rotatable Rectangle
        :param x_pos:       Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:       Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:       Width of Rectangle
        :param height:      Height of Rectangle
        :param rotation:    Rotation of rectangle; increase to rotate clockwise; default is 0
        :param density:     Density of rectangle; default is 1
        :param damping:     How quickly the object is slowed when no force is applied; default is 0
        :param bullet:      If True, enables setting to improve high-speed physics; default is False
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.density = density
        self.damping = damping
        self.bullet = bullet
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        if self.coords_by_center:
            self._set_attributes('rr', self.x, self.y, self.width, self.height,
                                 self.rotation, self.density, self.damping)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('rr', self.x + half_w, self.y + half_h, self.width, self.height,
                                 self.rotation, self.density, self.damping)
        return super()._to_str(enumeration)


class RotatableCircle(_ot.Rotatable, _os.Circle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 motor_speed: int | float = 0,
                 torque: int | float = 100):
        """
        Rotatable Circle
        :param x_pos:       Position of center
        :param y_pos:       Position of center
        :param radius:      Radius of circle
        :param motor_speed: Speed of rotation; default is 0
        :param torque:      Torque of rotation; default is 100
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.motor_speed = motor_speed
        self.torque = torque

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('rc', self.x, self.y, self.radius, self.motor_speed, self.torque)
        return super()._to_str(enumeration)


class SpringyRectangle(_ot.Moveable, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 rotation: int | float = 0,
                 density: int | float = 1,
                 frequency: int | float = 2,
                 damping: int | float = .3,
                 fulcrum_offset: int | float = 0,
                 fulcrum_radius: int | float = 10,
                 bullet: bool = False,
                 coords_by_center: bool = False):
        """
        Rectangle that returns to a resting position of 0 degrees when rotated
        :param x_pos:           Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:           Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:           Width of Rectangle
        :param height:          Height of Rectangle
        :param rotation:        Starting rotation; default is 0. Note that regardless of this value, resting rotation is still 0 degrees.
        :param density:         Density of object; default is 1
        :param frequency:       Frequency of spring; default is 2
        :param damping:         How quickly the object is slowed when no force is applied; default is .3
        :param fulcrum_offset:  Position of fulcrum (point of rotation) relative to rectangle's center; default is 0
        :param fulcrum_radius:  Radius of fulcrum; does not affect rotation; default is 10
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.density = density
        self.frequency = frequency
        self.damping = damping
        self.fulcrum_offset = fulcrum_offset
        self.fulcrum_radius = fulcrum_radius
        self.bullet = bullet
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        if self.coords_by_center:
            self._set_attributes('wr', self.x, self.y, self.width / 2, self.height / 2,
                                 self.rotation, self.density, self.frequency, self.damping,
                                 self.fulcrum_offset, self.fulcrum_radius)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('wr', self.x + half_w, self.y + half_h, half_w, half_h,
                                 self.rotation, self.density, self.frequency, self.damping,
                                 self.fulcrum_offset, self.fulcrum_radius)
        return super()._to_str(enumeration)


class Portal(_os.Other):
    def __init__(self,
                 portal_x: int | float,
                 portal_y: int | float,
                 target_x: int | float,
                 target_y: int | float,
                 appear_at_circle: int = 1,
                 deactivate_at_circle: int = 7,
                 min_touch_time: int | float = 0,
                 start_disabled: bool = False):
        """
        Teleports the player that touches it to a target location.
        :param portal_x:            X coordinate of portal
        :param portal_y:            Y coordinate of portal
        :param target_x:            X coordinate of target location
        :param target_y:            Y coordinate of target location
        :param appear_at_circle:    Circle at which the portal is activated; hidden in-game; default is 1
        :param deactivate_at_circle:Circle (number of collected collectables) after which to deactivate portal; default is 7
        :param min_touch_time:      Minimum touch time required for portal to trigger; default is 0
        :param start_disabled:      If True, Portal starts disabled and must be reactivated by a SpecialConnection to use
        """
        super().__init__()
        self.portal_x = portal_x
        self.portal_y = portal_y
        self.target_x = target_x
        self.target_y = target_y
        self.appear_at_circle = appear_at_circle
        self.deactivate_at_circle = deactivate_at_circle
        self.min_touch_time = min_touch_time
        self.start_disabled = start_disabled

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.start_disabled:
            self._add_modifier("off")

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('portal', self.portal_x, self.portal_y, self.target_x, self.target_y,
                             self.appear_at_circle, self.deactivate_at_circle, self.min_touch_time)
        return super()._to_str(enumeration)


class Dummy(_os.Other):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float):
        """Literally does nothing."""
        super().__init__()
        # Dummy also has an adjustable radius in the level editor, but it does not save its state
        self.x = x_pos
        self.y = y_pos

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('dummy', self.x, self.y)
        return super()._to_str(enumeration)


class ParticleRectangle(_os.Rectangle):
    def __init__(self, x_pos, y_pos, width, height, rotation=0, coords_by_center=False):
        """
        Splits into a bunch of tiny movable circles with high restitution.
        :param x_pos:               Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:               Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:               Width of Rectangle
        :param height:              Height of Rectangle
        :param rotation:            Rotation of rectangle; the game does not import this correctly, and it must be adjusted manually
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        if self.coords_by_center:
            self._set_attributes('partR', self.x, self.y, self.width / 2, self.height / 2, self.rotation)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('partR', self.x + half_w, self.y + half_h, half_w, half_h, self.rotation)
        return super()._to_str(enumeration)


# GENERATORS ###########################################################################################################

class CircleGenerator(_ot.Generator, _ot.Moveable, _os.Circle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 radius: int | float,
                 density: int | float = 1,
                 disappear_after: int | float = 5,
                 wait_between: int | float = 1,
                 init_delay: int | float = 0,
                 damping: int | float = 0,
                 no_fade: bool = False,
                 start_off: bool = False,
                 bullet: bool = False):
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
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.radius = radius
        self.density = density
        self.disappear_after = disappear_after
        self.wait_between = wait_between
        self.init_delay = init_delay
        self.damping = damping
        self.no_fade = no_fade
        self.start_off = start_off
        self.bullet = bullet

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.damping != 0:
            self._add_modifier(f"damping {self.damping}")

    def _to_str(self, enumeration: bool = False) -> str:
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        self._set_attributes('tmc', self.x, self.y, self.radius, self.density,
                             self.disappear_after * 60, self.wait_between * 60, self.init_delay * 60)
        return super()._to_str(enumeration)


class RectangleGenerator(_ot.Generator, _ot.Moveable, _os.Rectangle):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 width: int | float,
                 height: int | float,
                 density: int | float = 1,
                 rotation: int | float = 0,
                 damping: int | float = 0,
                 disappear_after: int | float = 5,
                 wait_between: int | float = 1,
                 init_delay: int | float = 0,
                 fix_rotation: bool = False,
                 no_fade: bool = False,
                 start_off: bool = False,
                 bullet: bool = False,
                 coords_by_center: bool = False):
        """
        Generates movable rectangles at timed intervals.
        :param x_pos:           Position of top-left corner of rectangle (left), or of center if coords_by_center
        :param y_pos:           Position of top-left corner of rectangle (top), or of center if coords_by_center
        :param width:           Width of Rectangle
        :param height:          Height of Rectangle
        :param density:         Density of rectangle; make 0 to turn solid; default is 1
        :param rotation:        Rotation of rectangle; increase to rotate clockwise; default is 0
        :param damping:         How quickly the object is slowed when no force is applied; default is 0
        :param disappear_after: Time (in seconds) that circle exists before disappearing; default is 5
        :param wait_between:    Time (in seconds) between a circle disappearing and a new circle generating; default is 1
        :param init_delay:      Time (in seconds) before the generator begins generating circles; defalut is 0
        :param fix_rotation:    Disable rotation if True; default is False
        :param no_fade:         If True, disables the fading animation; default is False
        :param start_off:       If True, the generator does not start until triggered with a special connection; default is False
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        :param coords_by_center:    If True, interprets given position and size as from center; default is False.
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.density = density
        self.rotation = rotation
        self.damping = damping
        self.disappear_after = disappear_after
        self.wait_between = wait_between
        self.init_delay = init_delay
        self.fix_rotation = fix_rotation
        self.no_fade = no_fade
        self.start_off = start_off
        self.bullet = bullet
        self.coords_by_center = coords_by_center

    def _to_str(self, enumeration: bool = False) -> str:
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        # The extra 0 value likely used to be rotational damping, but it is not read in the import script.
        if self.coords_by_center:
            self._set_attributes('tmb', self.x, self.y, self.width / 2, self.height / 2,
                                 self.density, 0, self.rotation, self.damping,
                                 self.disappear_after * 60, self.wait_between * 60, self.init_delay * 60)
        else:
            half_w = self.width / 2
            half_h = self.height / 2
            self._set_attributes('tmb', self.x + half_w, self.y + half_h, half_w, half_h,
                                 self.density, self.damping, self.rotation, self.damping,
                                 self.disappear_after * 60, self.wait_between * 60, self.init_delay * 60)
        return super()._to_str(enumeration)


class TriangleGenerator(_ot.Generator, _ot.Moveable, _os.Triangle):
    def __init__(self,
                 x1: int | float,
                 y1: int | float,
                 x2: int | float,
                 y2: int | float,
                 x3: int | float,
                 y3: int | float,
                 density: int | float = 1,
                 disappear_after: int | float = 5,
                 wait_between: int | float = 1,
                 init_delay: int | float = 0,
                 fix_rotation: bool = False,
                 no_fade: bool = False,
                 start_off: bool = False,
                 bullet: bool = False):
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
        :param bullet:          If True, enables setting to improve high-speed physics; default is False
        """
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.density = density
        self.disappear_after = disappear_after
        self.wait_between = wait_between
        self.init_delay = init_delay
        self.fix_rotation = fix_rotation
        self.no_fade = no_fade
        self.start_off = start_off
        self.bullet = bullet

    def _to_str(self, enumeration: bool = False) -> str:
        # The timed settings are multiplied by 60, as they are stored in frames, with 60 FPS.
        # The extra 0 values do nothing.
        self._set_attributes('tmt', self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.density, 0, 0,
                             self.disappear_after * 60, self.wait_between * 60, self.init_delay * 60)
        return super()._to_str(enumeration)


# CONNECTIONS ##########################################################################################################

class Glue(_os.Other):
    def __init__(self, obj1, obj2):
        """
        Glues two movable objects together
        :param obj1: reference to obj 1
        :param obj2: reference to obj 2
        """
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('/ GLUE', self.obj1.get_id(), self.obj2.get_id())
        return super()._to_str(enumeration)


class Rope(_os.Connection):
    def __init__(self, obj1, obj2,
                 offset1_x: int | float = 0,
                 offset1_y: int | float = 0,
                 offset2_x: int | float = 0,
                 offset2_y: int | float = 0,
                 max_length: int | float = 0):
        """
        Connect two objects with the ability to move semi-independently. For portals, use the Fixed Distance connection.
        :param obj1:        reference to obj 1
        :param obj2:        reference to obj 2
        :param offset1_x:   offset from obj 1; default is 0
        :param offset1_y:   offset from obj 1; default is 0
        :param offset2_x:   offset from obj 2; default is 0
        :param offset2_y:   offset from obj 2; default is 0
        :param max_length:  maximum length the rope can extend beyond the distance between obj1 & obj2; default is 0
        """
        if isinstance(obj1, Portal) or isinstance(obj2, Portal):
            raise TypeError("To connect a Portal with a Rope, use FixedDistanceConnection(portal, other) instead.")

        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.offset1_x = offset1_x
        self.offset1_y = offset1_y
        self.offset2_x = offset2_x
        self.offset2_y = offset2_y
        self.max_length = max_length

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('r', '', self.offset1_x, self.offset1_y, self.offset2_x, self.offset2_y, self.max_length)
        return super()._to_str(enumeration)


class FixedDistanceConnection(_os.Connection):
    def __init__(self, obj1, obj2,
                 also_move_destination: bool = False):
        """
        Fixed Distance connection. Only used for portals in-game; using on other objects is... funky... (but possible!)
        :param obj1: reference to portal
        :param obj2: reference to other object
        :param also_move_destination: if True, also moves destination of portal; default is False
        """
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.also_move_destination = also_move_destination

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('fd', int(self.also_move_destination))
        return super()._to_str(enumeration)


class DistanceConnection(_os.Connection):
    def __init__(self, obj1, obj2,
                 offset1_x: int | float = 0,
                 offset1_y: int | float = 0,
                 offset2_x: int | float = 0,
                 offset2_y: int | float = 0):
        """
        Works similar to ropes, but the objects are at a fixed distance from each other. This is not available in-game.
        :param obj1:        reference to obj 1
        :param obj2:        reference to obj 2
        :param offset1_x:   offset from obj 1; default is 0
        :param offset1_y:   offset from obj 1; default is 0
        :param offset2_x:   offset from obj 2; default is 0
        :param offset2_y:   offset from obj 2; default is 0
        """
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.offset1_x = offset1_x
        self.offset1_y = offset1_y
        self.offset2_x = offset2_x
        self.offset2_y = offset2_y

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('d', self.offset1_x, self.offset1_y, self.offset2_x, self.offset2_y)
        return super()._to_str(enumeration)


class Pulley(_os.Connection):
    def __init__(self, obj1, obj2,
                 pulley1_x: int | float = 0,
                 pulley1_y: int | float = -100,
                 pulley2_x: int | float = 0,
                 pulley2_y: int | float = -100,
                 offset1_x: int | float = 0,
                 offset1_y: int | float = 0,
                 offset2_x: int | float = 0,
                 offset2_y: int | float = 0,
                 ratio: int | float = 1,
                 unlock_movement: bool = False):
        """
        Connect objects via a pulley system.
        Note that the offsets are unavailable in the editor, and they can be buggy if not set to 0.
        :param obj1:            reference to first object
        :param obj2:            reference to second object
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
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.pulley1_x = pulley1_x
        self.pulley1_y = pulley1_y
        self.pulley2_x = pulley2_x
        self.pulley2_y = pulley2_y
        self.offset1_x = offset1_x
        self.offset1_y = offset1_y
        self.offset2_x = offset2_x
        self.offset2_y = offset2_y
        self.ratio = ratio
        self.unlock_movement = unlock_movement

    def _update_modifiers(self):
        super()._update_modifiers()
        if self.unlock_movement:
            self._add_modifier("p_free_hmovement")

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('/ p_description', self.offset1_x, self.offset1_y, self.offset2_x, self.offset2_y,
                             self.pulley1_x, self.pulley1_y, self.pulley2_x, self.pulley2_y, self.ratio)
        return super()._to_str(enumeration)


class Hinge(_ot.Rotatable, _os.Connection):
    def __init__(self, obj1, obj2,
                 offset_x: int | float = 0,
                 offset_y: int | float = 0,
                 draw_connection_line: bool = False,
                 enable_collisions: bool = False,
                 motor_speed: int | float = 0,
                 torque: int | float = 100):
        """
        Connect two objects rigidly while allowing rotation.
        :param obj1:                    reference to obj 1
        :param obj2:                    reference to obj 2
        :param offset_x:                offset of pivot point from obj 1; default is 0
        :param offset_y:                offset of pivot point from obj 1; default is 0
        :param draw_connection_line:    if True, shows a line between the connected objects; default is False
        :param enable_collisions:       if True, enables connected objects to collide with each other; default is False
        :param motor_speed:             speed of rotation; default is 0
        :param torque:                  torque of rotation; default is 100
        """
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.draw_connection_line = draw_connection_line
        self.enable_collisions = enable_collisions
        self.motor_speed = motor_speed
        self.torque = torque

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('hinge', '', self.offset_x, self.offset_y,
                             int(self.draw_connection_line), int(self.enable_collisions),
                             self.motor_speed, self.torque)
        return super()._to_str(enumeration)


class Slider(_os.Connection):
    def __init__(self, obj1, obj2,
                 offset_x: int | float = 0,
                 offset_y: int | float = 0):
        """
        Connect objects rigidly with the ability to move in a straight line between each other.
        :param obj1:        reference to obj 1
        :param obj2:        reference to obj 2
        :param offset_x:    offset from obj 1; default is 0
        :param offset_y:    offset from obj 1; default is 0
        """
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.offset_x = offset_x
        self.offset_y = offset_y

    def _to_str(self, enumeration: bool = False) -> str:
        # The extra 0 values appear to do nothing, but are initialized around ±1 when created in-game, so idk.
        self._set_attributes('pr', 0, 0, 0, 0, self.offset_x, self.offset_y)
        return super()._to_str(enumeration)


class SpecialConnection(_os.Connection):
    def __init__(self, collectable, target, action, *args):
        """
        Perform an action to a target object upon the collection of a collectable.
        Supported Actions:
            'Disconnect' - disconnects ropes & hinges,
            'Follow' - sets camera to follow object,
            'Reset' - enables & resets timer of generators,
            'Now' - generates one object from a generator,
            'NowIf' - generates an object from a generator if none currently exist,
            'Destroy' - destroys all instances of a generator object,
            'On' - enables generator or portal,
            'Off' - disables generator or portal,
            'Teleport' - teleports player to end point of connected portal,
            'RotationOn' - allows movable rectangles/triangles to rotate,
            'RotationOff' - disables movable rectangles/triangles from rotating,
            'SetSpeed' - sets speed of object in x- and y-direction; requires extra x & y arg,
            'Impulse' - applies a force to an object in x- and y-direction; requires extra x & y arg,
            'Trigger' - collects/triggers the collectable it is connected to,
            'TriggerRandom' - collects/triggers at random one of the collectables it is connected to (if it is only connected to one, it is triggered with a 50%)
        :param collectable: reference to connected special collectable
        :param target:      reference to target object
        :param action:      action to perform on target object
        :param args:        other arguments required for SetSpeed & Impulse
        """
        if not isinstance(collectable, SpecialCollectable) and collectable is not None:
            _warn(f"You are trying to connect a SpecialConnection to a non-SpecialCollectable object. This is not recommended but still technically possible.")

        super().__init__()
        self.obj1 = collectable
        self.obj2 = target
        self.collectable = collectable
        self.target = target
        self.action = action
        self.args = args

    def _to_str(self, enumeration: bool = False) -> str:
        self._set_attributes('spc', f"'{self.action}'", *self.args)
        return super()._to_str(enumeration)


# COLLECTABLES #########################################################################################################

class Collectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
        """
        Collectable circle
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'io' if self.collect_from_object else 'i'
        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment)
        return super()._to_str(enumeration)


class GravityCollectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 grav_dir: int | float = 270,
                 grav_strength: int | float = 1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
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
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

        self.grav_dir = grav_dir
        self.grav_strength = grav_strength

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'im' if self.collect_from_object else 'ig'
        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment, '',
                             self.grav_dir, self.grav_strength)
        return super()._to_str(enumeration)


class SizeCollectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 size: int | float = 1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False,
                 by_player_percent: bool = True):
        """
        Collectable circle that changes player size.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param size:                New radius/size of player; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        :param by_player_percent:   New radius is normally determined by percentage of initial Player radius; if False, size is determined by base unit size instead; default is True
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

        self.size = size
        self.by_player_percent = by_player_percent

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'iso' if self.collect_from_object else 'is'
        new_size = self.size * 32.50 if self.by_player_percent else self.size

        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment, '', new_size)
        return super()._to_str(enumeration)


class DisconnectCollectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
        """
        Collectable circle that disconnects player from all connections.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'irbo' if self.collect_from_object else 'irb'
        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment)
        return super()._to_str(enumeration)


class SpeedCollectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 speed: int | float = 1,
                 density: int | float = -1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
        """
        Collectable circle that changes player speed.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param speed:               New speed of player; default is 1
        :param density:             New density of player; does not appear to work in-game; default is -1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

        self.speed = speed
        self.density = density

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'ipso' if self.collect_from_object else 'ips'
        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment, '', self.speed, self.density)
        return super()._to_str(enumeration)


class SpecialCollectable(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 appear_at_segment: int = 1,
                 part_of_segment: int = 0,
                 zoom: int | float = -1,
                 is_trigger: bool = False,
                 collect_from_object: bool = False,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
        """
        Collectable circle that performs an action on an object connected to it via a special connection.
        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param appear_at_segment:   Segment at which the object first appears; default is 1
        :param part_of_segment:     Number of previously collected collectables after which the object first appears; default is 0
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param is_trigger:          If True, collectable does not increase circle size upon collection; default is False
        :param collect_from_object: If True, changes collectable to only be collected upon collision with a non-player object; default is False
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.appear_at_segment = appear_at_segment
        self.part_of_segment = part_of_segment
        self.zoom = zoom
        self.is_trigger = is_trigger
        self.collect_from_object = collect_from_object
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

    def _to_str(self, enumeration: bool = False) -> str:
        tag = 'ispo' if self.collect_from_object else 'isp'
        self._set_attributes(f"ic '{tag}'", self.x, self.y, self.appear_at_segment)
        return super()._to_str(enumeration)


class InputTrigger(_os.Collectable):
    def __init__(self,
                 x_pos: int | float,
                 y_pos: int | float,
                 input: str = 'left',
                 action: str = 'pressed',
                 zoom: int | float = -1,
                 start_disabled: bool = False,
                 disable_on_trigger: bool = False):
        """

        :param x_pos:               Position of center
        :param y_pos:               Position of center
        :param input:               Which input collectable triggers from:
                                        'left' - activates when left is actioned,
                                        'right' - activates when right is actioned,
                                        'both' - activates when both left and right are actioned,
                                        'every_frame' - activates every frame,
                                        'on_trigger' - activates only when triggered with a SpecialConnection
        :param action:              Which left/right/both causes collectable to trigger:
                                        'pressed' - activates when input is pressed,
                                        'released' - activates when input is released,
                                        'down' - activates every frame that input is held
        :param zoom:                Changes camera zoom upon collection; -1 --> no change, -2 --> full level; default is -1
        :param start_disabled:      If True, collectable starts deactivated and must be reactivated by another trigger to collect; default is False
        :param disable_on_trigger:  If True, collectable deactivates after triggering; default is False
        """
        super().__init__()
        self.x = x_pos
        self.y = y_pos
        self.input = input
        self.action = action
        self.zoom = zoom
        self.start_disabled = start_disabled
        self.disable_on_trigger = disable_on_trigger

    def _to_str(self, enumeration: bool = False) -> str:

        if self.input == 'every_frame':
            trigger_type = 9
        elif self.input == 'on_trigger':
            trigger_type = 10
        else:
            trigger_type = _INPUT_TRIGGER_MAP[self.input, self.action]

        self._set_attributes('ispt', self.x, self.y, trigger_type)
        return super()._to_str(enumeration)
