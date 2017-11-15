import re
import mutagen

from mutagen.id3 import Encoding, TIT2, TRCK

class TagInspector(object):
	supported_formats = ['mp3', 'mp4']
	track_pat = re.compile('(\d+)/(\d+)')

	def __init__(self, path):
		self.path = path
		self.file = mutagen.File(self.path)
		self.format = type(self.file).__name__.lower()

		if self.format not in self.supported_formats:
			raise RuntimeError(f"Unsupported format '{self.format}'.")

	def __getattr__(self, key):
		if key == 'name':
			if self.format == 'mp3':
				return self.file.tags.get('TIT2').text[0]
			elif self.format == 'mp4':
				return self.file.tags.get('©nam')[0]
		elif key == 'track_info':
			if self.format == 'mp3':
				m = self.track_pat.match(self.file.tags.get('TRCK').text[0])
				i, n = [int(m.groups()[i]) for i in range(2)]
				return (i, n)
			elif self.format == 'mp4':
				return self.file.tags.get('trkn')[0]

		raise AttributeError(f"Invalid key '{key}'.")

	def __setattr__(self, key, value):
		if key == 'name' and self.name == value:
			return
		if key == 'track_info' and self.track_info == value:
			return

		super().__setattr__(key, value)

		if key == 'name':
			if self.format == 'mp3':
				self.file.tags['TIT2'] = TIT2(encoding=Encoding.UTF16, text=value)
			elif self.format == 'mp4':
				self.file.tags['©nam'] = [value]

			self.file.save()
		elif key == 'track_info':
			if self.format == 'mp3':
				track_str = '{}/{}'.format(*value)
				self.file.tags['TRCK'] = TRCK(encoding=Encoding.UTF16,
					text=track_str)
			elif self.format == 'mp4':
				self.file.tags['trkn'] = [value]

			self.file.save()

	def __repr__(self):
		return f"'{self.path}'"
