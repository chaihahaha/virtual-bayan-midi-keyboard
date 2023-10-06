midiccto_note = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}

def midicc_code_to_note_name(midi_cc):
    pitch = midi_cc % 12
    octave = (midi_cc // 12)
    return f"{midiccto_note[pitch]}{octave}"


if __name__=="__main__":
    print(midicc_code_to_note_name(24))  # Output: C2
    print(midicc_code_to_note_name(25))  # Output: C#2
