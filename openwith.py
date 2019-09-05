import argparse
import os
import time
import exiftool
import yaml
import wx

class OpenWith(wx.Frame):
	def __init__(self, parent, files, lenses):
		wx.Frame.__init__(self, parent, title='Lens Tagger', size=(200,-1))
		self.files = files
		self.lenses = lenses

		self.txt = wx.StaticText(self, label=f'Select the lens to tag {len(self.files)} file with')
		self.choose = wx.Choice(self, choices=[l['key'] for l in self.lenses])
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
	
	def ok(self, event):
		self.bc = wx.BusyCursor()
		self.choose.Enable(False)
		self.button.Enable(False)

		chosen = self.choose.GetString(self.choose.GetSelection())
		exif = {}
		for lens in lenses:
			if lens['key'] == chosen:
				exif = lens['exif']
				break
		exifcommand = [f'-{key}={value}'.encode('ascii') for key, value in exif.items()]
		with exiftool.ExifTool() as et:
			for i, fn in enumerate(self.files):
				self.txt.SetLabel(f'Tagging {os.path.basename(fn)}')
				r = et.execute(*(exifcommand + [exiftool.fsencode(fn)]))
				self.progress.SetValue(i)

		self.txt.SetLabel('All done, quit now')
		self.Bind(wx.EVT_BUTTON, self.quit, self.button)
		self.button.SetLabel('Quit')
		self.button.Enable(True)
		del self.bc
	
	def quit(self, event):
		self.Close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--lenses', dest='lenses', help='YAML files containing lenses', required=True)
	parser.add_argument('files', nargs='*', help='Files to operate on')
	args = parser.parse_args()

	with open(args.lenses, 'rb') as fh:
		lenses = yaml.load(fh, Loader=yaml.Loader)

	app = wx.App(False)
	frame = OpenWith(None, args.files, lenses)
	app.MainLoop()
