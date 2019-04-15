import os.path
from GoMusix.settings import MUSICFILES_DIR
from .models import UserSong
import json
import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
from mutagen.oggflac import OggFLAC
from mutagen.oggopus import OggOpus
from mutagen.oggspeex import OggSpeex
from mutagen.oggtheora import OggTheora
from django.conf import settings
import logging


#logger for logging errors
logger = logging.getLogger(__name__)


# songs path
songsPath = MUSICFILES_DIR
# from django's docs
def handle_uploaded_file(f, name):
	ext = '.tmp'
	name = str(name)
	try:
		destination = open(songsPath+name+'%s'%(ext), 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		return True
	except Exception as e:
		return e

def getTitle(sn):
	filePath = MUSICFILES_DIR+str(sn)+'.tmp'
	if isAMusicFile(filePath) != True:
		return 'Unknown filename'

	try:
		audio = EasyID3(filePath)
	except:
		audio = mutagen.File(filePath, easy=True)

	if audio is None:
		return getOriginalName(sn)

	if 'title' not in audio:
		if getOriginalName(sn) != False:
			audio['title'] = getOriginalName(sn)
			return getOriginalName(sn)
		else:
			return 'Unknown filename'
	else:
		return audio['title'][0]

def getOriginalName(sn):
	nameQuery = UserSong.objects.all().filter(sn=sn)
	if nameQuery.count() == 1:
		return nameQuery[0].originalname
	else:
		return False

def getArtist(sn):
	filePath = MUSICFILES_DIR+str(sn)+'.tmp'
	if isAMusicFile(filePath) != True:
		return 'Unknown artist'
		
	try:
		audio = EasyID3(filePath)
	except:
		audio = mutagen.File(filePath, easy=True)

	if audio is None:
		return 'Unknown artist'

	if 'artist' not in audio:
		return 'Unknown artist'
	else:
		return audio['artist'][0]

def getMimeType(sn):
	getMime = UserSong.objects.all().filter(sn=sn)
	if getMime.count() == 1:
		return getMime[0].mimetype
	else:
		return 'Unknown mimetype'

def getThumbnail(sn):
	filePath = MUSICFILES_DIR+str(sn)+'.tmp'
	if isAMusicFile(filePath) != True:
		return 'No Thumbnail'
		
	try:
		audio = ID3(filePath)
	except:
		audio = mutagen.File(filePath)

	if audio is None:
		return 'No Thumbnail'
		
	try:
		apicData = audio.getall("APIC")[0].data
		return apicData
	except:
		return 'No Thumbnail'

def isSongValid(file):
	acceptedMime = ['audio/mp3', 'audio/mpeg', 'audio/mpeg3', 'audio/x-mpeg-3', 'audio/ogg', 'application/ogg', 'audio/x-ogg', 'application/x-ogg', 'video/ogg', 'audio/wav', 'audio/x-wav', 'audio/wave', 'audio/x-pn-wav']
	type = "none"
	if file:
		if file._size > 10*1024*1024:
			return ('File too large. Max Limit: 10MB')
		elif not file.content_type in acceptedMime:
			if settings.DEBUG:
				return ('MIMETYPE: ' + file.content_type + ' Not a mp3, ogg, or wav file')
			else:
				logger.error('MIMETYPE: ' + file.content_type + ' Not a mp3, ogg, or wav file')
				return ('It is not a mp3, ogg, or wav file')

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
			return ('Unsupported file type')

		return True
	else:
		return ('File cannot be opened')

def isAMusicFile(filePath):
	type = "none"
	try:
		OggVorbis(filePath)
		type = 'OGG'
	except:
		pass

	try:
		OggFLAC(filePath)
		type = 'OGG'
	except:
		pass

	try:
		OggOpus(filePath)
		type = 'OGG'
	except:
		pass

	try:
		OggSpeex(filePath)
		type = 'OGG'
	except:
		pass

	try:
		OggTheora(filePath)
		type = 'OGG'
	except:
		pass

	try:
		MP3(filePath)
		type = 'MP3'
	except:
		pass

	try:
		WavPack(filePath)
		type = 'WAV'
	except:
		pass

	if not type in ['OGG', 'MP3', 'WAV']:
		return False

	return True

def createHtmlList(array):
	toReturn = ''
	for messages in array:
		toReturn = toReturn + messages + '<br />'
	return toReturn

def ownsFile(sn, username):
	songQuery = UserSong.objects.all().filter(sn=sn, username=username)
	if songQuery.count() == 1:
		return True
	else:
		return False