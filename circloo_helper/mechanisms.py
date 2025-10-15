"""Mechanisms are deprecated in favor of ObjectGroups"""

from .level import Level as _Level
import circloo_helper.objects as _o


class Mechanism:
    def __init__(self, objs, start_id):
        """Group of objects that perform a specific function.
        :param objs: List of Objects in the mechanism
        :param start_id: Starting id to write the object to. This should usually be used with Level.get_len"""
        self.objs = objs
        self.start_id = start_id

    def add_to(self, level: _Level):
        level.add(self.objs)


class LeftRightDetector(Mechanism):
    def __init__(self, x_pos, y_pos, start_id):
        spring = _o.SpringyRectangle(x_pos, y_pos, 5, 50, density=1, damping=0, frequency=20)
        player = _o.Player(x_pos, y_pos + 50, speed=10, density=.1)
        hinge1 = _o.Hinge(start_id, start_id + 1)
        hinge2 = _o.Hinge(start_id + 1, start_id)
        objs = [spring, player, hinge1, hinge2]
        super().__init__(objs, start_id)


class PauseDetector(Mechanism):
    def __init__(self, x_pos, y_pos, start_id):
        player = _o.Player(x_pos, y_pos, bullet=False)
        main_portal = _o.Portal(x_pos, y_pos, x_pos + 22, y_pos)
        rope = _o.FixedDistanceConnection(start_id + 1, start_id, also_move_destination=True)
        reset1 = _o.Portal(x_pos + 100, y_pos - 30, x_pos, y_pos)
        reset2 = _o.Portal(x_pos + 100, y_pos + 30, x_pos, y_pos)
        box1 = _o.Rectangle(x_pos - 45, y_pos - .5, 5, 37.5)
        box2 = _o.Rectangle(x_pos + 45, y_pos - .5, 5, 37.5)
        box3 = _o.Rectangle(x_pos + 135, y_pos - .5, 5, 37.5)
        box4 = _o.Rectangle(x_pos + 45, y_pos - 43, 95, 5)
        box5 = _o.Rectangle(x_pos + 45, y_pos + 42, 95, 5)

        objs = [player, main_portal, rope, reset1, reset2, box1, box2, box3, box4, box5]
        super().__init__(objs, start_id)


class RingCounter(Mechanism):
    def __init__(self, start_x, y_pos, length, start_id):
        objs = []

        # Create Generators & triggers
        for i in range(length):
            # id = 2 * i + 0
            trigger = _o.SpecialCollectable(start_x + 50 * i, y_pos, is_trigger=True, collect_from_object=True)
            # id = 2 * i + 1
            generator = _o.CircleGenerator(start_x + 50 * i, y_pos, 20, density=0,
                                           disappear_after=0, wait_between=9999, no_fade=True, start_off=True)

            objs.append(trigger)
            objs.append(generator)

        # Create Primary Connections
        for j in range(length):
            if j < length - 1:
                destroy = _o.SpecialConnection(start_id + 2 * j, start_id + 2 * j + 1, 'Destroy')
                deactivate = _o.SpecialConnection(start_id + 2 * j, start_id + 2 * j + 2, 'Deactivate')
                nowif = _o.SpecialConnection(start_id + 2 * j, start_id + 2 * j + 3, 'NowIf')
            else:
                destroy = _o.SpecialConnection(start_id + 2 * j, start_id + 2 * j + 1, 'Destroy')
                deactivate = _o.SpecialConnection(start_id + 2 * j, start_id, 'Deactivate')
                nowif = _o.SpecialConnection(start_id + 2 * j, start_id + 1, 'NowIf')

            objs.append(destroy)
            objs.append(deactivate)
            objs.append(nowif)

        # Create input
        objs.append(_o.SpecialCollectable(start_x + 50 * length + 25, y_pos, is_trigger=True, collect_from_object=True))
        for k in range(length):
            reactivate = _o.SpecialConnection(start_id + 5 * length, start_id + 2 * k, 'Reactivate')
            objs.append(reactivate)

        # Create Initializer
        objs.append(_o.SpecialCollectable(start_x - 75, y_pos, is_trigger=True, collect_from_object=True))
        objs.append(_o.CircleGenerator(start_x - 75, y_pos, 20, density=0, disappear_after=.1, wait_between=9999))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id + 6 * length + 2, 'Off'))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id, 'Deactivate'))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id + 1, 'NowIf'))

        super().__init__(objs, start_id)


class FlipFlop(Mechanism):
    def __init__(self, x_pos, y_pos, in_x, in_y, start_id):
        left_trigger = _o.SpecialCollectable(x_pos-12, y_pos-12, is_trigger=True, collect_from_object=True)
        right_trigger = _o.SpecialCollectable(x_pos+13, y_pos+13, is_trigger=True, collect_from_object=True)
        left_gen = _o.CircleGenerator(x_pos - 12, y_pos - 12, 10, 0, 0, 9999, no_fade=True)
        right_gen = _o.CircleGenerator(x_pos + 13, y_pos + 13, 10, 0, 0, 9999, start_off=True, no_fade=True)
        in_trigger = _o.SpecialCollectable(in_x, in_y, is_trigger=True, collect_from_object=True)

        dest_1 = _o.SpecialConnection(start_id, start_id+3, 'Destroy')
        dest_2 = _o.SpecialConnection(start_id+1, start_id+2, 'Destroy')
        now_1 = _o.SpecialConnection(start_id, start_id+2, 'NowIf')
        now_2 = _o.SpecialConnection(start_id+1, start_id+3, 'NowIf')
        in_1 = _o.SpecialConnection(start_id+4, start_id+2, 'NowIf')
        in_2 = _o.SpecialConnection(start_id+4, start_id+3, 'NowIf')

        left_trigger.mute()
        right_trigger.mute()
        in_trigger.mute()

        objs = [left_trigger, right_trigger, left_gen, right_gen, in_trigger, dest_1, dest_2, now_1, now_2, in_1, in_2]
        super().__init__(objs, start_id)


class Sweeper(Mechanism):
    def __init__(self, x_pos, y_pos, start_id, speed=1):
        mover = _o.MoveableRectangle(x_pos, x_pos, 15, 15, density=.01, fix_rotation=True)
        solid = _o.Rectangle(x_pos-30, y_pos, 5, 5)
        generator = _o.RectangleGenerator(x_pos-50, y_pos, 5, 5, density=50, disappear_after=.02, wait_between=0, fix_rotation=True)
        rope = _o.Rope(start_id+1, start_id+2, max_length=-speed)
        hinge = _o.Hinge(start_id, start_id+2)

        objs = [mover, solid, generator, rope, hinge]
        super().__init__(objs, start_id)
