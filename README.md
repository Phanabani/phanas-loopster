# Phana's Loopster

[![release](https://img.shields.io/github/v/release/phanabani/phanas-loopster)](https://github.com/phanabani/phanas-loopster/releases)
[![license](https://img.shields.io/github/license/phanabani/phanas-loopster)](LICENSE)

A small Python program that helps you easily loop music for RPG Maker.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Developers](#developers)
- [License](#license)

## Install

### Prerequisites

- [Python 3.9+](https://www.python.org) 
- (Optional) [Poetry](https://python-poetry.org/docs/#installation) – dependency manager

### Install Phana's Loopster

To get started, clone the repo.

```shell
git clone https://github.com/phanabani/phanas-loopster.git
cd phanas-loopster
```

## Usage

In the top level directory, simply run Phana's Loopster as a Python module to
view a help message listing all available arguments.

```shell
python -m phanas_loopster
```

### Example usage:

```shell
python -m phanas_loopster \  # on Windows you might need to use ^ instead of \ to do line breaks
"C:\Users\Phana\Music\mySong.wav" "C:\Users\Phana\Music\mySong.ogg" 120 "17:01" \
--title "My Song" --artist Phanabani --album "My Album" --year 2022
```

### Beat string

The "17:01" is what I call a beat string (for lack of a better term). The beat
string is a string representing bars:beats:ticks, and ticks and beats may be
omitted. In the example, "17:01" means "the song ends at bar 17, beat 1",
so 16 full bars of music.

Ticks are tied to the PPQ / tick division (parts-per-quarter[-note]). A common
PPQ is 96, so you'll have 96 ticks per beat.

This beat string is used to tell Phana's Loopster how long your song is WITHOUT
the tail (which includes reverb, delays, release times and all that). Just tell
us how long your song is, and we'll handle the looping for you!

### Technical details

We achieve looping like this:

1. Calculate how long the song's outro tail is
2. Copy a piece of the beginning of the song to match the duration of the outro tail
3. Move this intro to the end, mixing on top of the outro tail
4. Write metadata tags called LOOPSTART and LOOPLENGTH to tell other programs to skip the intro that doesn't include the outro tail

Essentially, we want the outro tail to overlap the intro, but only after we 
hear the intro once without it. This is how we achieve that! Hopefully, Phana's
Loopster makes this super easy so you don't have to do lots of math and tedious
entering of metadata.

## Developers

### Installation

Follow the installation steps in [install](#install) and use Poetry to 
install the development dependencies:

```shell
poetry install --no-root
```

## License

[MIT © Phanabani.](LICENSE)
