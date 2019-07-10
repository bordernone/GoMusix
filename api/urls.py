# api/urls.py
from django.urls import path, re_path
from .views import api, getToken, refreshToken, userSongsDetail, songsDetailsBasic, songsThumbnail, playSong, signup, recoverAccount

urlpatterns = [
    path('', userSongsDetail, name='api'),
    path('token/', getToken, name='getToken'),
    path('refresh/', refreshToken, name='refreshToken'),
    path('songs/basic/', songsDetailsBasic, name='songsDetailsBasic'),
    path('songs/thumbnail/', songsThumbnail, name='songsThumbnail'),
    path('songs/play/', playSong, name='playSong'),
    path('signup/', signup, name='signup'),
    path('recover/', recoverAccount, name='recover'),
]