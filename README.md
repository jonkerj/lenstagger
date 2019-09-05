# Lens Tagger

This tool is a simple frontend to help you Exif tag your manual lenses. It is
inspired by [NameThatLens](https://www.jazzycamel.photography/NameThatLens), a
GUI designed to do this.

## NameThatLens
Don't get me wrong, NameThatLens is a cool tool; I have used it with joy. Over
time, I think it could be better.

* I switch lenses a lot, which complicates my workflow. I have to open a image
  gallery which previews the raw files, note lens types with file names, and
  click around in he tool. I believe I can build a tool that does all of this.
* It lacks fine grained control over which Exif tags it exactly manipulates. For
  instance, I'd like `Lens` to be filled with both make and model, not just
  model.
* When I switched to Mac, the tool simply refused to work. Of course, the author
  could/should fix that, but the link pointing to the community forum is dead
  and the tool does not look very actively maintained.
* I'd like to be able to poke around and fix things myself. NameThatLens is
  closed source.

## Configuration
Create or edit the file named `lenses.yaml`. It should contain a list of maps,
where each map should have the keys `key` and `exif`. The former is used to
reference the lens upon tool invocation, and the latter a map containing the
arguments for [Exiftool](https://sno.phy.queensu.ca/~phil/exiftool/). 

Please be advised that [PyExiftool](https://github.com/smarnach/pyexiftool/)
calls `exiftool` with `-n` (no print conversion), and does not pass warnings.
For example: instead of writing `LensInfo: 28mm f/2.8`, you should write
`LensInfo: 28 28 2.8 2.8`.

A full example:
```yaml
---
- key: helios44
  exif:
    Lens: Zenit Helios 44-2
    LensType: Zenit Helios 44-2
    LensMake: Zenit
    LensModel: Helios 44-2
    LensInfo: 58 58 2.0 2.0
    FocalLength: 58
    FocalLengthIn35mmFormat: 116
    LensSerialNumber: '83090316'
- key: vivitar28
  exif:
    Lens: Vivitar 28mm 1:2.8 Auto Wide-Angle
    LensType: Vivitar 28mm 1:2.8 Auto Wide-Angle
    LensMake: Vivitar
    LensModel: 28mm 1:2.8 Auto Wide-Angle
    LensInfo: 28 28 2.8 2.8
    FocalLength: 28
    FocalLengthIn35mmFormat: 56
    LensSerialNumber: '28832266'
...
```

Next, prepare the tool like this:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

To run the GUI (currently only tested on MacOS), you need to build the app:

```bash
$ ./gen-iconset.sh
$ python setup.py py2app
```

## Usage
There are two ways to use LensTagger: CLI and GUI. The CLI is pretty
straightforward:

```bash
$ python3 cli.py --lens helios44 file1.RW2 file2.JPG
```

The GUI is meant to be invoked using your OS "Open With" menu in its file
browser. Just point the "Open With" dialog to either `openwith.sh` (Linux) or
to the built `LensTagger.app` (MacOs).

```bash
$ ./openwith.sh --lenses lenses.yaml file1.RW2 file2.JPG
```

The wrapper script `openwith.sh` takes care the venv-python is used.

## To Do
1. But exiftool into some thread to make GUI responsive during tagging
1. Find a way to permanently put Lens Tagger in OSX 'Open With' menu
1. Package the app
