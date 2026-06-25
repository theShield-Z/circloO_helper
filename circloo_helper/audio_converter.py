"""
TODO: add support for track params (allow users to set pitch, volume, instrument, etc. of each track as a dict)
    especially necessary for percussion tracks
"""
from mido import MidiFile, tick2second

from .object import CustomObject
from .circloo_objects import Collectable, InputTrigger, SpecialCollectable, CircleGenerator, SpecialConnection, SolidRectangle
from .text import Text


_NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
               'F#', 'G', 'G#', 'A', 'A#', 'B']

_DRUM_MAP = {35: ('drum', 1, 1, 1),     # Acoustic Bass Drum
             36: ('drum', 5, 1, 1),     # Bass Drum 1
             38: ('drum', 0, 1, 1),     # Acoustic Snare
             40: ('drum', 2, 1, 1),     # Electric Snare
             42: ('house', 10, 2, 1),   # Closed Hi-Hat
             44: ('house', 18, 2, 2),   # Pedal Hi-Hat
             46: ('drum', 9, 1, 1),     # Open Hi-Hat
             49: ('drum', 3, 1, 1),     # Crash 1
             51: ('house', 18, 1, 1),   # Ride 1
             45: ('drum', 7, .8, 1),    # Low Tom
             47: ('drum', 7, .9, 1),    # Low-Mid Tom
             48: ('drum', 7, 1.1, 1),   # Hi-Mid Tom
             50: ('drum', 7, 1.3, 1),   # High Tom
             39: ('drum', 4, 1, 1),     # Hand Clap
             54: ('drum', 3, 3, 1),     # Tambourine
             56: ('house', 21, 1, 1),   # Cowbell
             57: ('drum', 3, 1, 1),     # Crash 2
             52: ('house', 18, 1, 1)}   # China


class CHMIDI(CustomObject):
    """circloO Helper MIDI"""

    def __init__(self,
                 filepath: str,
                 start_x: int | float = 1500,
                 start_y: int | float = 1500,
                 min_duration: int | float = 1,
                 long_start_x: int | float | None = None,
                 long_start_y: int | float | None = None,
                 pitch: int | float = 1,
                 volume: int | float = 1,
                 labels: bool = True,
                 track_params: dict = None):
        """
        Converts a .mid MIDI song into circloO Objects
        :param filepath:        Path to midi file
        :param start_x:         X-position of top-left corner; default is 1500 (center of level)
        :param start_y:         Y-position of top-left corner; default is 1500 (center of level)
        :param min_duration:    The minimum necessary duration of a note (in seconds) before a long/lasting trigger is
                                    used instead of a simple trigger; use a large number to disable; default is 1
        :param long_start_x:    X-position of the top-left corner of long/lasting trigger section.
                                    If None, it will be placed to the left of the main body of the system;
                                    default is None
        :param long_start_y:    Y-position of the top-left corner of long/lasting trigger section.
                                    If None, it will use start_y; default is None
        :param pitch:           Default pitch of all trigger sounds if none is provided in params; default is 1
        :param volume:          Default volume of all trigger sounds if none is provided in params; default is 1
        :param labels:          If True, tracks are labeled in-game with their names; default is True
        :param track_params:    Dictionary of track sound overrides. See documentation for syntax.
        """
        super().__init__()
        self.filepath = filepath
        self.start_x = start_x
        self.start_y = start_y
        self.min_duration = min_duration
        self.long_start_x = long_start_x if long_start_x is not None else start_x - 100
        self.long_start_y = long_start_y if long_start_y is not None else start_y
        self.pitch = pitch
        self.volume = volume
        self.labels = labels
        self.track_params = {} if track_params is None else track_params

    def build_objs(self):
        super().build_objs()
        midi = MidiFile(self.filepath)

        ticks_per_beat = midi.ticks_per_beat
        tempo = 500000  # default: 120 BPM

        # Collectable coordinates.
        x = self.start_x
        y = self.start_y
        long_x = self.long_start_x
        long_y = self.long_start_y

        for track_num, track in enumerate(midi.tracks):
            # print(f"Track {track_num}: {track.name}")    # debug

            cbls = {}  # note_name -> cbl

            track_presets = self.track_params.get(track_num, {})
            pitch = track_presets.get('pitch', self.pitch)
            volume = track_presets.get('volume', self.volume)
            note_overrides = track_presets.get('note_overrides')

            active_notes = {}  # note -> start_time_seconds

            current_ticks = 0
            current_seconds = 0.0

            for msg in track:

                # GET MIDI DATA ########################################################################################

                # Advance time.
                delta_seconds = tick2second(
                    msg.time,
                    ticks_per_beat,
                    tempo
                )

                current_ticks += msg.time
                current_seconds += delta_seconds

                # Tempo changes affect subsequent messages.
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                    continue

                # Note start.
                if msg.type == "note_on" and msg.velocity > 0:
                    active_notes[msg.note] = current_seconds

                # Note end.
                elif msg.type == "note_off" or (
                        msg.type == "note_on" and msg.velocity == 0
                ):
                    if msg.note in active_notes:

                        note_name = self._note_number_to_name(msg.note)
                        note_value = msg.note
                        start_time = active_notes.pop(msg.note)     # Removes note from active_notes
                        duration = current_seconds - start_time

                        # CONVERT TO CIRCLOO ###########################################################################

                        # Create the sound.

                        sound = None

                        if note_overrides is not None and note_overrides.get(note_value) is not None:
                            # Use sound profile provided in self.track_params
                            group, value, pitch, volume = note_overrides[note_value]
                            sound = Collectable.Sound(group, value, volume, pitch)

                        if sound is None:
                            if hasattr(msg, "channel") and msg.channel == 9:
                                # Standard percussion channel; use sounds from _DRUM_MAP.
                                drum_sound = _DRUM_MAP.get(note_value)

                                if drum_sound is not None:
                                    group, value, pitch, volume = drum_sound
                                    sound = Collectable.Sound(group, value, volume, pitch)
                                else:
                                    sound = Collectable.Sound()

                            else:
                                # Use a piano sound with self.volume and self.pitch.
                                #   In-game note numeration is offset by 36 from midi representation.
                                sound = Collectable.Sound('piano', note_value - 36, volume, pitch)
                                while sound.note < 0:
                                    # Ensure sound is not negative.
                                    sound.pitch /= 2
                                    sound.note += 12

                        if duration > self.min_duration:
                            # Replay the sound every frame when the note is sustained for a while.

                            cbl = InputTrigger(long_x - 50, long_y, 'every_frame', start_disabled=True)
                            cbl.sound = sound

                            on_t = SpecialCollectable(long_x, long_y, is_trigger=True,
                                                      collect_from_object=True, disable_on_trigger=True)
                            on_t.mute()
                            on_g = CircleGenerator(long_x, long_y, 10, 0,
                                                   .05, 9999, start_time,
                                                   no_fade=True)
                            on_s = SpecialConnection(on_t, cbl, 'Reactivate')

                            off_t = SpecialCollectable(long_x + 50, long_y, is_trigger=True,
                                                       collect_from_object=True, disable_on_trigger=True)
                            off_t.mute()
                            off_g = CircleGenerator(long_x + 50, long_y, 10, 0,
                                                    .05, 9999,
                                                    start_time + duration, no_fade=True)
                            off_s = SpecialConnection(off_t, cbl, 'Deactivate')

                            long_y += 50

                            self._obj_cache.extend([cbl, on_t, on_g, on_s, off_t, off_g, off_s])

                            continue

                        # Add a collectable to the level if not already.
                        keys = cbls.keys()
                        if note_name not in keys:
                            cbl = Collectable(x + len(keys) * 50, y, is_trigger=True, collect_from_object=True)
                            cbl.sound = sound
                            cbls[note_name] = cbl

                        cbl = cbls[note_name]
                        gen = CircleGenerator(cbl.x, cbl.y, 10, 0, .05, 9999, start_time, no_fade=True)
                        self._obj_cache.append(gen)

            self._obj_cache.extend(cbls.values())

            if self.labels:
                # Label each track.
                label = Text(track.name, SolidRectangle(x + len(cbls) * 50, y - 10, 5, 5))
                self._obj_cache.extend(label.build_objs())

            y += 50

        return self._obj_cache

    @staticmethod
    def _note_number_to_name(note):
        octave = (note // 12) - 1
        return f"{_NOTE_NAMES[note % 12]}{octave}"
