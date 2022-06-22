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

- [Poetry](https://python-poetry.org/docs/#installation) – dependency manager
- (Optional) pyenv – Python version manager
    - [pyenv](https://github.com/pyenv/pyenv) (Linux, Mac)
    - [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows)

### Install Phana's Loopster

To get started, clone the repo.

```shell
git clone https://github.com/phanabani/phanas-loopster.git
cd phanas-loopster
```

Install the dependencies with Poetry. Phana's Loopster requires Python 3.9.6+.

```shell
poetry install --no-root --no-dev
```

## Usage

In the top level directory, simply run Phana's Loopster as a Python module with Poetry.

```shell
poetry run python -m phanas_loopster
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
