from setuptools import setup

APP = ['openwith.py']
APP_NAME = 'LensTagger'
DATA_FILES = ['lenses.yaml']
VERSION = '0.1.0'

OPTIONS = {
	'argv_emulation': True,
	'iconfile': 'LensTagger.icns',
	'packages': ['wx',],
	'plist': {
		'CFBundleName': APP_NAME,
		'CFBundleDisplayName': APP_NAME,
		'CFBundleGetInfoString': 'Tagging manual lenses',
		'CFBundleIdentifier': 'nl.efgh.lenstagger',
		'CFBundleVersion': VERSION,
		'CFBundleShortVersionString': VERSION,
	},
}

setup(
	name=APP_NAME,
	app=APP,
	data_files=DATA_FILES,
	options={'py2app': OPTIONS},
	setup_requires=['pyapp'],
)
