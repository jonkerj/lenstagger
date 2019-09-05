import argparse
import logging
import os
import time
import exiftool
import yaml
import wx

logging.basicConfig(
	format="%(asctime)s %(levelname)s: %(message)s",
	level=logging.DEBUG,
	datefmt="%H:%M:%S",
	filename='/tmp/lenstagger.log',
	filemode='a',
)
logger = logging.getLogger('lenstagger')

class OpenWith(wx.Frame):
	def __init__(self, parent, files, config):
		logger.debug('Init app')
		wx.Frame.__init__(self, parent, title='Lens Tagger', size=(200,-1))
		self.files = files
		self.config = config

		logger.debug(f'files={",".join(self.files)}')
		logger.debug(f'lenses={",".join([l["key"] for l in self.config["lenses"]])}')

		self.txt = wx.StaticText(self, label=f'Select the lens to tag {len(self.files)} file with')
		self.choose = wx.Choice(self, choices=[l['key'] for l in self.config['lenses']])
		self.button = wx.Button(self, wx.ID_OK, 'OK')
		self.progress = wx.Gauge(self, range=len(files)-1, style=wx.GA_HORIZONTAL, size=(200,-1))
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		for element in [self.txt, self.choose, self.button, self.progress]:
			self.sizer.Add(element, wx.EXPAND)
		self.SetSizer(self.sizer)

		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show()

		self.Bind(wx.EVT_BUTTON, self.ok, self.button)
		logger.debug('Done init')
	
	def ok(self, event):
		logger.debug('OK clicked')
		self.bc = wx.BusyCursor()
		self.choose.Enable(False)
		self.button.Enable(False)

		chosen = self.choose.GetString(self.choose.GetSelection())
		exif = {}
		for lens in self.config['lenses']:
			if lens['key'] == chosen:
				exif = lens['exif']
				break
		exifcommand = [f'-{key}={value}'.encode('ascii') for key, value in exif.items()]
		logger.debug(f'PATH={os.environ["PATH"]}')
		logger.debug('opening exiftool')
		with exiftool.ExifTool(self.config['exiftool']) as et:
			logger.debug('enumerating files')
			for i, fn in enumerate(self.files):
				logger.debug(f'working on {fn}')
				self.txt.SetLabel(f'Tagging {os.path.basename(fn)}')
				r = et.execute(*(exifcommand + [exiftool.fsencode(fn)]))
				self.progress.SetValue(i)

		logger.debug('done')
		self.txt.SetLabel('All done, quit now')
		self.Bind(wx.EVT_BUTTON, self.quit, self.button)
		self.button.SetLabel('Quit')
		self.button.Enable(True)
		del self.bc
	
	def quit(self, event):
		self.Close()

if __name__ == '__main__':
	config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lenses.yaml')

	parser = argparse.ArgumentParser()
	parser.add_argument('--lenses', dest='lenses', help='YAML files containing lenses', default=config)
	parser.add_argument('files', nargs='*', help='Files to operate on')
	args = parser.parse_args()

	logger.debug(f'opening configfile {args.lenses}')
	with open(args.lenses, 'rb') as fh:
		config = yaml.load(fh, Loader=yaml.Loader)

	logger.debug('making app')
	app = wx.App(False)
	logger.debug('making OpenWith')
	frame = OpenWith(None, args.files, config)
	logger.debug('Entering mainloop')
	logger.debug('return from mainloop')
	app.MainLoop()
