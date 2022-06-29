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

Example usage:

```shell
python -m phanas_loopster \
"C:\Users\Phana\Music\mySong.wav" "C:\Users\Phana\Music\mySong.ogg" 120 "17:01" \
--title "My Song" --artist Phanabani --album "My Album" --year 2022
```

## Developers

### Installation

Follow the installation steps in [install](#install) and use Poetry to 
install the development dependencies:

```shell
poetry install --no-root
```

## License

[MIT © Phanabani.](LICENSE)
