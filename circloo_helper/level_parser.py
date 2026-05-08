import re
from pyperclip import paste

from .level import Level
from .circloo_objects import *
from .object import Object
from .object_shapes import Connection
from .object_types import Generator

_INPUT_TRIGGER_MAP = {
    0: ('left', 'pressed'),
    1: ('right', 'pressed'),
    2: ('left', 'released'),
    3: ('right', 'released'),
    4: ('both', 'pressed'),
    5: ('both', 'released'),
    6: ('left', 'down'),
    7: ('right', 'down'),
    8: ('both', 'down'),
    9: ('every_frame', None),
    10: ('on_trigger', None)
}


def _add_connections(lvl: Level, obj: Connection, indexes: list[int]):
    for idx in indexes[-2:]:
        if not obj.obj1:
            obj.obj1 = lvl.object_at(idx)
        else:
            obj.obj2 = lvl.object_at(idx)


def _parse_sfx(s: str):
    match = re.fullmatch(r"'([A-Za-z]*)(\d*)'", s)

    if not match:
        return '', None

    group = match.group(1)
    note = match.group(2)

    note = int(note) if note else 0

    return group, note


def parse(level_text: str) -> Level:

    if not level_text.startswith("/\n/ circloO level"):
        raise ValueError("This text does not appear to contain a circloO level.")

    lvl = Level()
    cur_obj: Object | None = None
    connections = []
    skip = 0

    for line in level_text.splitlines():
        try:
            if skip > 0:
                # print("SKIPPED LINE")       # DEBUG
                skip -= 1
                continue
            # print("NEW LINE:", line)        # DEBUG

            split_line = line.split(' ')
            # print(split_line)            # DEBUG

            match split_line[0]:

                case 'levelscriptVersion':
                    # Verify version.
                    if int(split_line[1]) < 10:
                        raise ValueError('circloO_Helper has only been tested with levelscript versions >= 10. '
                                         'Please update your circloO app to the latest version.')
                    if int(split_line[1]) > 10:
                        raise ValueError('circloO_Helper has not been updated to this version yet.')

                case '/':
                    if len(split_line) <= 1:
                        continue
                    match split_line[1]:
                        case 'SKIP':
                            skip = int(split_line[2])
                        case 'LE_DEFAULT_LINE_THICKNESS':
                            lvl.default_line_thickness = float(split_line[2])
                        case 'LE_ARC_DESCRIPTION':
                            cx, cy, sa, ea, rad, crx, cry, _, thickness = split_line[2:11]
                            cur_obj = Arc(float(cx), float(cy),
                                          360 - float(sa), 360 - float(ea),
                                          float(rad),
                                          float(crx), float(cry),
                                          float(thickness))
                        case 'p_description':
                            cur_obj = Pulley(None, None, *map(float, split_line[2:11]))
                        case 'GLUE':
                            cur_obj = Glue(None, None)
                            connections = list(map(int, split_line[2: 4]))

                # LEVEL MODIFIERS.

                case 'totalCircles':
                    lvl.segments = float(split_line[1])
                    lvl.start_full = bool(int(split_line[2]))

                case 'COLORS':
                    lvl.color = int(split_line[1])

                case 'grav':
                    lvl.grav_scale = float(split_line[1])
                    lvl.grav_dir = float(split_line[2])

                case 'recommend_sfx':
                    lvl.recommend_sfx = True

                case 'music':
                    lvl.music = tuple(split_line[-2:])

                case 'followOne':
                    lvl.camera_follow_one_player_only = True

                case 'affectAllPlayersByCollectibles':
                    lvl.affect_all_players_by_collectables = True

                case 'use_legacy_line_drawing':
                    lvl.line_extra_width = split_line[1]

                case 'gravcontrol':
                    lvl.gravcontrol = True

                # OBJECTS.

                case 'c':
                    cur_obj = SolidCircle(*map(float, split_line[1:4]))

                case 'b':
                    cur_obj = SolidRectangle(*map(float, split_line[1:6]), coords_by_center=True)
                    cur_obj.width *= 2
                    cur_obj.height *= 2

                case 't':
                    cur_obj = SolidTriangle(*map(float, split_line[1:7]))

                case 'l_at':
                    cur_obj = Line(*map(float, split_line[1:6]))

                case 'curve':
                    cur_obj = Curve(*map(float, split_line[1:11]))

                case 'gc':
                    cur_obj = GrowingCircle(*map(float, split_line[1:4]))

                case 'rGr':
                    cur_obj = GrowingRectangle(*map(float, split_line[1:6]), coords_by_center=True)
                    cur_obj.width *= 2
                    cur_obj.height *= 2

                case 'mc':
                    cur_obj = MoveableCircle(*map(float, split_line[1:6]))

                case 'mb':
                    x, y, width, height, density, _, rotation, damping = split_line[1:9]
                    cur_obj = MoveableRectangle(float(x), float(y), float(width) * 2, float(height) * 2,
                                                float(density), float(damping), float(rotation),
                                                coords_by_center=True)

                case 'mt':
                    cur_obj = MoveableTriangle(*map(float, split_line[1:8]))

                case 'rr':
                    cur_obj = RotatableRectangle(*map(float, split_line[1:8]), coords_by_center=True)

                case 'rc':
                    cur_obj = RotatableCircle(*map(float, split_line[1:6]))

                case 'wr':
                    cur_obj = SpringyRectangle(*map(float, split_line[1:11]), coords_by_center=True)
                    cur_obj.width *= 2
                    cur_obj.height *= 2

                case 'tmc':
                    x, y, radius, density, disp_after, wait_bw, delay = split_line[1:8]
                    cur_obj = CircleGenerator(float(x), float(y), float(radius), float(density),
                                              float(disp_after) / 60, float(wait_bw) / 60, float(delay) / 60)

                case 'tmb':
                    x, y, width, height, density, _, rotation, damping, disp_after, wait_bw, delay = split_line[1:12]
                    cur_obj = RectangleGenerator(float(x), float(y),
                                                 float(width) * 2, float(height) * 2,
                                                 float(density), float(rotation), float(damping),
                                                 float(disp_after) / 60, float(wait_bw) / 60, float(delay) / 60,
                                                 coords_by_center=True)

                case 'tmt':
                    disp_after, wait_bw, delay = split_line[10:13]
                    cur_obj = TriangleGenerator(*map(float, split_line[1:8]),
                                                float(disp_after) / 60, float(wait_bw) / 60, float(delay) / 60)

                case 'portal':
                    appear, disp, min_time = split_line[5:8]
                    cur_obj = Portal(*map(float, split_line[1:5]), int(appear), int(disp), float(min_time))

                case 'y':
                    restitution = split_line[6] if len(split_line) > 6 else 0
                    cur_obj = Player(*map(float, split_line[1:6]), restitution, bullet=False)

                case 'dummy':
                    cur_obj = Dummy(*map(float, split_line[1:3]))

                case 'partR':
                    cur_obj = ParticleRectangle(*map(float, split_line[1:6]), coords_by_center=True)
                    cur_obj.width *= 2
                    cur_obj.height *= 2

                case 'ispt':
                    x, y, trigger_type = split_line[1:4]
                    inp, action = _INPUT_TRIGGER_MAP[int(trigger_type)]
                    cur_obj = InputTrigger(float(x), float(y), inp, action)

                # COLLECTABLES.

                case 'ic':
                    match split_line[1]:
                        case "'i'":
                            x, y, appear = split_line[2:5]
                            cur_obj = Collectable(float(x), float(y), int(appear))
                        case "'io'":
                            x, y, appear = split_line[2:5]
                            cur_obj = Collectable(float(x), float(y), int(appear), collect_from_object=True)
                        case "'ig'":
                            x, y, appear, _, direction, strength = split_line[2:8]
                            cur_obj = GravityCollectable(float(x), float(y), int(appear), float(direction), float(strength))
                        case "'im'":
                            x, y, appear, _, direction, strength = split_line[2:8]
                            cur_obj = GravityCollectable(float(x), float(y), int(appear), float(direction), float(strength),
                                                         collect_from_object=True)
                        case "'is'":
                            x, y, appear, _, size = split_line[2:7]
                            cur_obj = SizeCollectable(float(x), float(y), int(appear), float(size), by_player_percent=False)
                        case "'iso'":
                            x, y, appear, _, size = split_line[2:7]
                            cur_obj = SizeCollectable(float(x), float(y), int(appear), float(size), by_player_percent=False,
                                                      collect_from_object=True)
                        case "'irb'":
                            x, y, appear = split_line[2:5]
                            cur_obj = DisconnectCollectable(float(x), float(y), int(appear))
                        case "'irbo'":
                            x, y, appear = split_line[2:5]
                            cur_obj = DisconnectCollectable(float(x), float(y), int(appear), collect_from_object=True)
                        case "'ips'":
                            x, y, appear, _, speed, density = split_line[2:8]
                            cur_obj = SpeedCollectable(float(x), float(y), int(appear), float(speed), float(density))
                        case "'ipso'":
                            x, y, appear, _, speed, density = split_line[2:8]
                            cur_obj = SpeedCollectable(float(x), float(y), int(appear), float(speed), float(density),
                                                       collect_from_object=True)
                        case "'isp'":
                            x, y, appear = split_line[2:5]
                            cur_obj = SpecialCollectable(float(x), float(y), int(appear))
                        case "'ispo'":
                            x, y, appear = split_line[2:5]
                            cur_obj = SpecialCollectable(float(x), float(y), int(appear), collect_from_object=True)

                # CONNECTIONS.

                case 'r':
                    cur_obj = Rope(None, None, *map(float, split_line[2:7]))

                case 'hinge':
                    x, y, draw, coll, speed, torque = split_line[2:8]
                    cur_obj = Hinge(None, None,
                                    float(x), float(y),
                                    bool(int(draw)), bool(int(coll)),
                                    float(speed), float(torque))

                case 'pr':
                    cur_obj = Slider(None, None, *map(float, split_line[5:7]))

                case 'fd':
                    cur_obj = FixedDistanceConnection(None, None, bool(int(split_line[1])))

                case 'd':
                    cur_obj = DistanceConnection(None, None, *map(float, split_line[1:5]))

                case 'spc':
                    action, *args = split_line[1:]
                    args = map(float, args)
                    action = action.replace("'", '')
                    cur_obj = SpecialConnection(None, None, action, *args)

                # OBJECT MODIFIERS.

                case 'attr':
                    cur_obj.attractor = float(split_line[1])

                case 'wheelsprite':
                    cur_obj.wheelsprite = True

                case 'iGrow':
                    cur_obj.part_of_segment = int(split_line[1])

                case 'zoomFactor':
                    cur_obj.zoom = float(split_line[1])

                case 'trigger':
                    cur_obj.is_trigger = True

                case 'off':
                    if isinstance(cur_obj, Generator):
                        cur_obj.start_off = True
                    else:
                        # portal or collectable
                        cur_obj.start_disabled = True

                case 'ott':
                    cur_obj.disable_on_trigger = True

                case 'sfx':
                    if split_line[1] == "'none'":
                        ### NOTE: this gets rid of any volume/pitch info. very much edge-case, but notable
                        cur_obj.mute()
                    else:
                        group, note = _parse_sfx(split_line[1])
                        if len(split_line) >= 5:
                            volume, pitch, play = split_line[2:5]
                        else:
                            volume, pitch, play = 1, 1, -1
                        cur_obj.set_sound(group, note, float(volume), float(pitch), int(play))

                case 'fixrot':
                    cur_obj.fix_rotation = True

                case 'noanim':
                    cur_obj.no_fade = True

                case 'samePosition':
                    cur_obj.keep_pos = True

                case 'bullet':
                    cur_obj.bullet = True

                case 'damping':
                    cur_obj.damping = float(split_line[1])

                case 'p_free_hmovement':
                    cur_obj.unlock_movement = True

                case '>':
                    connections.append(int(split_line[1]))

                case '<':
                    if cur_obj:
                        lvl.add(cur_obj)
                        if len(connections) > 0:
                            _add_connections(lvl, cur_obj, connections)
                    connections.clear()
                    cur_obj = None

        except Exception as e:
            warnings.warn(f"One or more objects could not be parsed: {e}")

    return lvl


def read_clipboard() -> Level:
    lvl = parse(paste())
    return lvl


def read_file(path: str) -> Level:
    with open(path, 'r') as f:
        lvl = parse(f.read())
    return lvl
