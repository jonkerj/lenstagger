#!/usr/bin/env python

import argparse
import yaml
import exiftool

with open('lenses.yaml', 'rb') as fh:
	lenses = yaml.load(fh, Loader=yaml.Loader)

parser = argparse.ArgumentParser()
parser.add_argument('--lens', help='Select lens', choices=[l['key'] for l in lenses], required=True)
parser.add_argument('files', nargs='+', help='Files to operate on')
args = parser.parse_args()

exif = {}
for lens in lenses:
	if lens['key'] == args.lens:
		exif = lens['exif']
		break

cmd = [f'-{key}={value}'.encode('ascii') for key, value in exif.items()]

with exiftool.ExifTool() as et:
	for filename in args.files:
		command = cmd + [exiftool.fsencode(filename)]
		print(command)
		r = et.execute(*command)
		print(r)
