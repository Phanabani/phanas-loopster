__all__ = ["beats_to_samples"]


def beats_to_samples(
    beat_string: str,
    bpm: float,
    beats_per_bar: int = 4,
    sample_rate: int = 48000,
    ppq: int = 96,
):
    beat_string_split = beat_string.split(":")
    if not (1 <= len(beat_string_split) <= 3):
        raise ValueError("beat_string must look like 1:1:0 (bar:beat:ticks)")
    bars = int(beat_string_split[0]) - 1
    beats = 0
    ticks = 0
    if len(beat_string_split) >= 2:
        beats = int(beat_string_split[1]) - 1
    if len(beat_string_split) == 3:
        ticks = int(beat_string_split[2])

    total_beats = ticks / ppq + beats + bars * beats_per_bar
    return round(total_beats * 60 / bpm * sample_rate)


if __name__ == "__main__":
    beat_string = input("Beat string: ")
    bpm = float(input("BPM: "))
    beats_per_bar = int(input("Beats per bar (4): ") or "4")
    sample_rate = int(input("Sample rate (48000): ") or "48000")
    ppq = int(input("PPQ (96): ") or "96")
    print(beats_to_samples(beat_string, bpm, beats_per_bar, sample_rate, ppq))
