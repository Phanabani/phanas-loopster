from __future__ import annotations

__all__ = [
    "AudioFileError",
    "get_total_samples",
    "get_streams_data",
    "make_looping_ogg",
    "main",
]

import argparse
import json
import logging
import math
from pathlib import Path
import sys
from typing import Any

from phanas_loopster.beats_to_samples import beats_to_samples
from phanas_loopster.common.misc import pathstr
from phanas_loopster.common.subprocess import run

logger = logging.getLogger("phanas_loopster")


class AudioFileError(Exception):
    pass


def get_streams_data(file: Path) -> list[dict[str, Any]]:
    proc = run(
        "ffprobe",
        ("-i", pathstr(file)),
        ("-v", "quiet"),
        ("-of", "json"),
        "-show_streams",
    )
    json_ = json.loads(proc.stdout)
    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug(f"Stream data: {json_}")
    return json_["streams"]


def get_total_samples(file: Path):
    streams = get_streams_data(file)
    if len(streams) != 1:
        raise AudioFileError(
            f"Expected a file with 1 audio stream, found {len(streams)} streams"
        )
    stream = streams[0]
    try:
        sample_rate = int(stream["sample_rate"])
        duration = float(stream["duration"])
    except KeyError as e:
        raise AudioFileError(f"File missing required metadata: {e}")

    return math.floor(duration * sample_rate)


def copy_intro_to_end_filter(
    intro_duration: int, body_duration: int, tail_duration: int
) -> tuple[str, str]:
    return (
        f"-filter_complex",
        f"[0]atrim=start_sample={intro_duration}:end_sample={intro_duration+tail_duration}"
        f", adelay=delays={intro_duration+body_duration}S:all=1"
        f"[delayed]"
        f"; [0][delayed]amix=normalize=0",
    )


def make_looping_ogg(
    input_file: Path,
    output_file: Path,
    intro_duration: int,
    body_duration: int,
    tail_duration: int,
    *,
    quality: int = 7,
    title: str | None = None,
    artist: str | None = None,
    album: str | None = None,
    year: str | None = None,
):
    extra_metadata = []
    if title:
        extra_metadata.append(("-metadata", f"TITLE={title}"))
    if artist:
        extra_metadata.append(("-metadata", f"ARTIST={artist}"))
    if album:
        extra_metadata.append(("-metadata", f"ALBUM={album}"))
    if year:
        extra_metadata.append(("-metadata", f"DATE={year}"))

    run(
        "ffmpeg",
        "-y",
        ("-i", pathstr(input_file)),
        ("-q:a", str(quality)),
        copy_intro_to_end_filter(intro_duration, body_duration, tail_duration),
        ("-metadata", f"LOOPSTART={tail_duration+intro_duration}"),
        ("-metadata", f"LOOPLENGTH={body_duration}"),
        *extra_metadata,
        pathstr(output_file),
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "A small Python program that helps you easily loop music for RPG Maker."
        )
    )
    parser.add_argument("input_file", type=Path, help="Input wav file")
    parser.add_argument("output_file", type=Path, help="Outputted looped ogg file")
    parser.add_argument("bpm", type=float, help="BPM of the track")
    parser.add_argument(
        "-s",
        "--loop-start",
        "--start",
        default="1",
        help=(
            "A string indicating the start of the loop (excluding intro) "
            '(bars:beats:ticks, e.g. "3:1:0" for 2 bars, or just "3:1" or "3") '
            '[default="1"]'
        ),
    )
    parser.add_argument(
        "-e",
        "--loop-end",
        "--end",
        help=(
            "A string indicating the end of the loop (excluding effect/envelope "
            'tails) (bars:beats:ticks, e.g. "9:1:0" for 8 bars, or just "9:1" '
            'or "9")'
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display debug info",
    )
    parser.add_argument(
        "-b",
        "--beats-per-bar",
        type=int,
        default=4,
        help="Beats per bar (beat signature numerator) [default=4]",
    )
    parser.add_argument(
        "-r",
        "--samplerate",
        type=int,
        default=48000,
        help="Sample rate [default=48000]",
    )
    parser.add_argument(
        "--ppq",
        "--tickdiv",
        type=int,
        default=96,
        help="PPQ (parts per quarter note), also known as tick division [default=96]",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=7,
        help=(
            "OGG quality (between -1 and 10 -- "
            "https://trac.ffmpeg.org/wiki/TheoraVorbisEncodingGuide) [default=7]"
        ),
    )

    metadata_group = parser.add_argument_group("Metadata", "Optional metadata")
    metadata_group.add_argument("--title", help="Song title")
    metadata_group.add_argument("--artist", help="Artist who wrote the song")
    metadata_group.add_argument("--album", help="Album name")
    metadata_group.add_argument("--year", help="Creation date (year)")

    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])

    if args.verbose:
        logger.setLevel("DEBUG")

    input_file: Path = args.input_file
    output_file: Path = args.output_file

    loop_start: str = args.loop_start
    loop_end: str = args.loop_end
    bpm: float = args.bpm
    beats_per_bar: int = args.beats_per_bar
    sample_rate: int = args.samplerate
    ppq: int = args.ppq
    quality: int = args.quality

    # Metadata
    title: str | None = args.title
    artist: str | None = args.artist
    album: str | None = args.album
    year: str | None = args.year

    # Create the new file
    loop_start_sample = beats_to_samples(
        loop_start, bpm, beats_per_bar, sample_rate, ppq
    )
    loop_end_sample = beats_to_samples(loop_end, bpm, beats_per_bar, sample_rate, ppq)
    audio_length = get_total_samples(input_file)
    tail_length = audio_length - loop_end_sample
    make_looping_ogg(
        input_file,
        output_file,
        intro_duration=loop_start_sample,
        body_duration=loop_end_sample - loop_start_sample,
        tail_duration=tail_length,
        quality=quality,
        title=title,
        artist=artist,
        album=album,
        year=year,
    )
