from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import apiKeys
from .utils import verifyToken
from dashboard.models import UserSong
from GoMusix.settings import MUSICFILES_DIR
from dashboard.utils import getTitle, getArtist, getThumbnail, getMimeType
import uuid
import json
import os

# Create your views here.
def api(request):
    return HttpResponse('Hello APi')

@csrf_exempt
def getToken(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # check if token exists. if so, delete it.
                query = apiKeys.objects.all().filter(username=username)
                if query.count() != 0:
                    query.delete()

                # generate new api token
                apiToken = uuid.uuid4().hex
                apiRefreshToken = uuid.uuid4().hex
                newApiAccess = apiKeys(username=username, apiToken=apiToken, apiRefreshToken=apiRefreshToken)
                newApiAccess.save()
                return JsonResponse({'apiToken':apiToken, 'apiRefreshToken':apiRefreshToken})
            else:
                return JsonResponse({'error':'incorrect username or password'})
        else:
            return JsonResponse({'error':'no username and password defined'})
    else:
        return JsonResponse({'error':'request must be POST'})

@csrf_exempt
def refreshToken(request):
    if request.method == 'POST':
        if 'refreshtoken' in request.POST and 'username' in request.POST:
            refreshToken = request.POST['refreshtoken']
            username = request.POST['username']

            # check if token exists.
            query = apiKeys.objects.all().filter(username=username, apiRefreshToken=refreshToken)
            if query.count() == 0:
                return JsonResponse({'error':'no token found'})
            else:
                #create new api token
                newToken = uuid.uuid4().hex
                thisToken = apiKeys.objects.all().filter(username=username, apiRefreshToken=refreshToken)[0]
                thisToken.apiToken = newToken
                thisToken.save()
                return JsonResponse({'apiToken':thisToken.apiToken})
        else:
            return JsonResponse({'error':'no refreshtoken or username sent'})
    else:
        return JsonResponse({'error':'request must be POST'})

@csrf_exempt
def userSongsDetail(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'token' in request.POST:
            username = request.POST['username']
            token = request.POST['token']
            if verifyToken(username, token) == True:
                allSongs = list(UserSong.objects.all().filter(username=username).values())
                return JsonResponse(allSongs, safe=False)
            else:
                return JsonResponse({'error':'incorrect token'})
        else:
            return JsonResponse({'error':'no username or token sent'})
    else:
        return JsonResponse({'error': 'request must be POST'})

#display songs (title, artist, sn)
@csrf_exempt
def songsDetailsBasic(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'token' in request.POST:
            username = request.POST['username']
            token = request.POST['token']
            if verifyToken(username, token) == True:
                allSongs = UserSong.objects.all().filter(username=username)
                
                songsList = []
                temp = []
                for song in allSongs:
                    temp = {
                        "sn": song.sn,
                        "title": getTitle(song.sn),
                        "artist": getArtist(song.sn),
                    }
                    temp = json.loads(json.dumps(temp))
                    songsList.append(temp)
                return JsonResponse(songsList, safe=False)
            else:
                return JsonResponse({'error':'incorrect token'})
        else:
            return JsonResponse({'error':'no username or token sent'})
    else:
        return JsonResponse({'error': 'request must be POST'})

@csrf_exempt
def songsThumbnail(request):
    if 'username' in request.GET and 'token' in request.GET and 'sn' in request.GET:
        username = request.GET['username']
        token = request.GET['token']
        sn = request.GET['sn']
        if verifyToken(username, token) == True:
            song = UserSong.objects.all().filter(username=username,sn=sn)
            if song.count() == 1:
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
                genericImg = 'static/dashboard/images/default-thumbnail.png'
                openFile = open(genericImg, 'rb')
                response = HttpResponse()
                response.write(openFile.read())
                response['Content-type'] = 'image/jpeg'
                return response
        else:
            return Http404
    else:
        return Http404

@csrf_exempt
def playSong(request):
    if 'username' in request.GET and 'token' in request.GET and 'sn' in request.GET:
        username = request.GET['username']
        token = request.GET['token']
        sn = request.GET['sn']
        if verifyToken(username, token) == True:
            song = UserSong.objects.all().filter(username=username,sn=sn)
            if song.count() == 1:
                mimetype = getMimeType(sn)

                fileName = sn + '.tmp'
                completePath = MUSICFILES_DIR + fileName

                openFile = open(completePath, 'rb')

                response = HttpResponse()
                response.write(openFile.read())
                response['Accept-Ranges'] = 'bytes'
                response['Content-type'] = mimetype
                response['Content-length'] = os.path.getsize(completePath)

                # response is ready. Update number of times this music has been played before returning response
                thisSong = UserSong.objects.all().filter(username=username, sn=sn)[0]
                thisSong.timesplayed = thisSong.timesplayed + 1
                thisSong.save()

                #return response
                return response
            else:
                return Http404
        else:
            return Http404
    else:
        return Http404