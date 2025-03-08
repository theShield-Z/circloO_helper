from .level import Level as _L
import circloo_helper.objects as _o


class Mechanism:
    def __init__(self, objs, start_id):
        """Group of objects that perform a specific function.
        :param objs: List of Objects in the mechanism
        :param start_id: Starting id to write the object to. This should usually be used with Level.get_len"""
        self.objs = objs
        self.start_id = start_id

    def add_to(self, level: _L):
        for obj in self.objs:
            level.add(obj)


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
        rope = _o.PortalRope(start_id + 1, start_id, also_move_destination=True)
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
            generator = _o.BallGenerator(start_x + 50 * i, y_pos, 20, density=0,
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
        objs.append(_o.BallGenerator(start_x - 75, y_pos, 20, density=0, disappear_after=.1, wait_between=9999))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id + 6 * length + 2, 'Off'))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id, 'Deactivate'))
        objs.append(_o.SpecialConnection(start_id + 6 * length + 1, start_id + 1, 'NowIf'))

        super().__init__(objs, start_id)

