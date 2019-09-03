# Lens Tagger

This tool is a simple frontend to help you EXIF tag your manual lenses. It is
inspired by [NameThatLens](https://www.jazzycamel.photography/NameThatLens), a
GUI designed to do this.

## Usage
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

Next, invoke the tool like this:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 cli.py --lens helios44 file1.RW2 file2.JPG
```
