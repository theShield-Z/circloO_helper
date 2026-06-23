from mido import MidiFile, tick2second


NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_number_to_name(note):
    octave = (note // 12) - 1
    return f"{NOTE_NAMES[note % 12]}{octave}"


def print_midi(filename):
    midi = MidiFile(filename)

    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000  # default: 120 BPM

    for track_num, track in enumerate(midi.tracks):

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

            ############################################################################################################




if __name__ == "__main__":
    print_midi("Stereo_Madness (1).mid")
