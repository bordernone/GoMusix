from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import escape
from django.utils.encoding import smart_str
from GoMusix.settings import MUSICFILES_DIR
from .utils import handle_uploaded_file, getTitle, getMimeType, getArtist, getThumbnail, isSongValid, createHtmlList, ownsFile
from .models import UserSong
from django.conf import settings
from mimetypes import MimeTypes
import urllib
import logging
import os
import json

#logger for logging errors
logger = logging.getLogger(__name__)

# Create your views here.
def dashboard(request):
	if request.user.is_authenticated:
		username = request.user.username
		songsTitle = []
		songsArtist = []
		songsSn = []
		userSongs = UserSong.objects.filter(username=username).order_by("-sn")
		sn = 0
		for eachRow in userSongs:
			sn = eachRow.sn 
			songsSn.append(sn)
			songsTitle.append(getTitle(sn))
			songsArtist.append(getArtist(sn))

		songsDetail = zip(songsSn, songsTitle, songsArtist)
		args = {'title':'My music | GoMusix', 'songs':songsDetail}

		return render(request, 'dashboard.html', args)
	else:
		return redirect('/')

def uploadMusic(request):
	if request.user.is_authenticated:
		username = request.user.username
		if request.method == 'POST':
			allMessages = [] #This is for debugging purposes
			showToUsers = [] #Only contains messages that should be displayed to the user except success messages
			for count, file in enumerate(request.FILES.getlist("file")):
				# This name would be displayed to the user. 
				trimmedFileName = (file.name[:10] + '..') if len(file.name) > 10 else file.name
				if isSongValid(file)==True:
					# if there's no data in database, make sn = 1
					query = UserSong.objects
					if query.count() == 0:
						sn = 1
					else:
						query = UserSong.objects.all().order_by('-sn')[0]
						sn = int(query.sn) + 1

					# saving file in the correction location
					saveFile = handle_uploaded_file(file, sn)
					
					# if saving was successful
					if (saveFile == True):
						contentType = file.content_type #file mimetype
						originalname = file.name # file's original name
						try:
							insertQuery = UserSong(sn=sn, username=username, mimetype=contentType, originalname=originalname)
							insertQuery.save()
							allMessages.append(file.name+': Success') #Not displayed to users
						except Exception as e:
							if settings.DEBUG:
								allMessages.append(e)
							else:
								logger.error(e)
								showToUsers.append(trimmedFileName + ': Cannot save in the database')
					else:
						if settings.DEBUG:
							allMessages.append(escape(saveFile))
						else:
							logger.error(saveFile)
							showToUsers.append('Something went wrong')
				else:
					allMessages.append(file.name + ': ' + isSongValid(file))
					showToUsers.append(trimmedFileName + ': ' + isSongValid(file))

			userFrieldlyMessages = createHtmlList(showToUsers)
			return HttpResponse(userFrieldlyMessages)
		else:
			if settings.DEBUG:
				return HttpResponse('Method must be POST')
			else:
				return Http404
	else:
		if settings.DEBUG:	
			return HttpResponse('You are not logged in')
		else:
			return Http404

def playMusic(request, sn):
	if request.user.is_authenticated:
		username = request.user.username
		if sn is None:
			if settings.DEBUG:
				return HttpResponse('No SN set')
			else:
				return Http404

		#retrieving the requested song
		querySong = UserSong.objects.all().filter(username=username,sn=sn)
		if querySong.count() == 1:
			mimetype = getMimeType(sn)

			fileName = sn + '.tmp'
			completePath = MUSICFILES_DIR + fileName

			openFile = open(completePath, 'rb')

			response = HttpResponse()
			response.write(openFile.read())
			response['Content-type'] = mimetype
			response['Content-length'] = os.path.getsize(completePath)
			return response
		else:
			if settings.DEBUG:
				return HttpResponse('No such file assosciated with this user')
			else:
				return Http404
	else:
		if settings.DEBUG:
			return HttpResponse('You are not logged in')
		else:
			return Http404

def displayThumbnail(request, sn):
	if request.user.is_authenticated:
		username = request.user.username
		if sn is None:
			if settings.DEBUG:
				return HttpResponse('No SN set')
			else:
				return Http404

		querySong = UserSong.objects.all().filter(sn=sn, username=username)
		if querySong.count() == 1:
			imgData = getThumbnail(sn)
			if imgData != 'No Thumbnail':
				response = HttpResponse(imgData)
				response['Content-type'] = 'image/jpeg'
			else:
				genericImg = 'static/dashboard/images/default-thumbnail.png'
				openFile = open(genericImg, 'rb')
				response = HttpResponse()
				response.write(openFile.read())
				response['Content-type'] = 'image/jpeg'
			return response
		else:
			if settings.DEBUG:
				return HttpResponse('No such file assosciated with this user')
			else:
				return Http404

	else:
		if settings.DEBUG:
			return HttpResponse('Not logged in')
		else:
			return Http404

def deleteSong(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			username = request.user.username
			if 'sn' not in request.POST:
				return Http404 if not settings.DEBUG else HttpResponse('No sn set')
			else:
				sn = request.POST['sn']

				#check if user owns the file
				userOwnsFile = ownsFile(sn, username)
				#deleting files
				if userOwnsFile == True:
					fileName = sn+'.tmp'
					filePath = MUSICFILES_DIR + fileName
					if os.path.exists(filePath):
						try:
							os.remove(filePath)
						except OSError as e:
							logger.error('Deletion failed(' + username + '): ' + e.strerror)
							return HttpResponse('File deletion failed: '+ e.strerror) if settings.DEBUG else Http404

						#deleting the record for this file
						thisSong = UserSong.objects.get(sn=sn, username=username)
						thisSong.delete()
						return HttpResponse('success')
					else:
						return HttpResponse('File not found') if settings.DEBUG else Http404
				else:
					return HttpResponse('Permission denied') if settings.DEBUG else Http404
				
		else:
			return Http404 if not settings.DEBUG else HttpResponse('Method must be post')
	else:
		if settings.DEBUG:
			return HttpResponse('You are not logged in')
		else:
			return Http404