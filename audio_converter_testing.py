from mido import MidiFile, tick2second
import circloo_helper as ch
from circloo_helper.circloo_objects import *


NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_number_to_name(note):
    octave = (note // 12) - 1
    return f"{NOTE_NAMES[note % 12]}{octave}"


def midi_to_circloo(filename, start_x=1500, start_y=1500):
    midi = MidiFile(filename)
    lvl = ch.Level(start_full=True, grav_scale=0, segments=500)

    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000  # default: 120 BPM

    x = start_x
    y = start_y

    continuous_x = continuous_y = 500   # for triggers that stay on a while

    for track_num, track in enumerate(midi.tracks):

        cbls = {}   # 'note_name' = cbl

        print(f"\n=== Track {track_num}: {track.name} ===")

        active_notes = {}  # note -> start_time_seconds

        current_ticks = 0
        current_seconds = 0.0

        for msg in track:
            # GET DATA #################################################################################################

            # Advance time
            delta_seconds = tick2second(
                msg.time,
                ticks_per_beat,
                tempo
            )

            current_ticks += msg.time
            current_seconds += delta_seconds

            # Tempo changes affect subsequent messages
            if msg.type == "set_tempo":
                tempo = msg.tempo
                continue

            # Note start
            if msg.type == "note_on" and msg.velocity > 0:
                active_notes[msg.note] = current_seconds

            # Note end
            elif msg.type == "note_off" or (
                    msg.type == "note_on" and msg.velocity == 0
            ):
                if msg.note in active_notes:

                    note_name = note_number_to_name(msg.note)
                    note_value = msg.note
                    start_time = active_notes.pop(msg.note)
                    duration = current_seconds - start_time

                    print(
                        f"{note_name:4s} | {note_value} | "
                        f"start={start_time:8.3f}s | "
                        f"duration={duration:8.3f}s"
                    )

                    ####################################################################################################

                    if duration > 1:
                        sound = Collectable.Sound('piano', note_value - 36, pitch=2)
                        cbl = InputTrigger(1450, 1450, 'every_frame', start_disabled=True)
                        cbl.sound = sound

                        on_t = SpecialCollectable(continuous_x, continuous_y, is_trigger=True, collect_from_object=True, disable_on_trigger=True)
                        on_t.mute()
                        on_g = CircleGenerator(continuous_x, continuous_y, 10, 0, .05, 9999, start_time, no_fade=True)
                        on_s = SpecialConnection(on_t, cbl, 'Reactivate')

                        off_t = SpecialCollectable(continuous_x + 50, continuous_y, is_trigger=True, collect_from_object=True, disable_on_trigger=True)
                        off_t.mute()
                        off_g = CircleGenerator(continuous_x + 50, continuous_y, 10, 0, .05, 9999, start_time + duration, no_fade=True)
                        off_s = SpecialConnection(off_t, cbl, 'Deactivate')

                        continuous_y += 50

                        for obj in [cbl, on_t, on_g, on_s, off_t, off_g, off_s]:
                            lvl.add(obj)

                        continue

                    # Add a collectable to the level if not already.
                    keys = cbls.keys()
                    if note_name not in keys:
                        sound = Collectable.Sound('piano', note_value - 36, pitch=2)
                        cbl = Collectable(x + len(keys) * 50, y, is_trigger=True, collect_from_object=True)
                        cbl.sound = sound
                        cbls[note_name] = cbl

                    cbl = cbls[note_name]
                    gen_x = cbl.x
                    gen_y = cbl.y
                    # gen = CircleGenerator(gen_x, gen_y, 10, 0, duration, 9999, start_time, no_fade=True)
                    gen = CircleGenerator(gen_x, gen_y, 10, 0, .05, 9999, start_time, no_fade=True)
                    lvl.add(gen)

        for cbl in cbls.values():
            lvl.add(cbl)
        lvl.add(ch.Text(track.name, SolidRectangle(x + len(cbls) * 50, y - 10, 5, 5)))
        y += 50

    print(lvl.to_clipboard())
    lvl.to_file('stereo_madness.txt')





if __name__ == "__main__":
    midi_to_circloo("8-Bitten 3.mid")
