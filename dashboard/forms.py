from django import forms
import mutagen
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from mutagen.oggflac import OggFLAC
from mutagen.oggopus import OggOpus
from mutagen.oggspeex import OggSpeex
from mutagen.oggtheora import OggTheora

class UploadFileForm(forms.Form):
	file = forms.FileField()

	def clean(self):
		file = self.cleaned_data.get('file', False)
		acceptedMime = ['audio/mpeg', 'audio/mpeg3', 'audio/x-mpeg-3', 'audio/ogg', 'application/ogg', 'audio/x-ogg', 'application/x-ogg', 'video/ogg', 'audio/wav', 'audio/x-wav', 'audio/wave', 'audio/x-pn-wav']
		type = "none"
		if file:
			if file._size > 10*1024*1024:
				raise forms.ValidationError(file.name + ': File too large. Max Limit: 10MB')
			elif not file.content_type in acceptedMime:
				raise forms.ValidationError(file.name + ': It is not a mp3, ogg, or wav file')

			try:
				OggVorbis(file.temporary_file_path())
				type = 'OGG'
			except:
				pass

			try:
				OggFLAC(file.temporary_file_path())
				type = 'OGG'
			except:
				pass

			try:
				OggOpus(file.temporary_file_path())
				type = 'OGG'
			except:
				pass

			try:
				OggSpeex(file.temporary_file_path())
				type = 'OGG'
			except:
				pass

			try:
				OggTheora(file.temporary_file_path())
				type = 'OGG'
			except:
				pass

			try:
				MP3(file.temporary_file_path())
				type = 'MP3'
			except:
				pass

			try:
				WavPack(file.temporary_file_path())
				type = 'WAV'
			except:
				pass

			if not type in ['OGG', 'MP3', 'WAV']:
				raise forms.ValidationError(file.name + ': Unsupported file type')

			return file
		else:
			raise forms.ValidationError(file.name + ': File cannot be opened')