# dashboard/urls.py
from django.urls import path, re_path
from homepage.views import homePageView
from .views import dashboard, uploadMusic, playMusic, displayThumbnail, deleteSong

urlpatterns = [
    path('', homePageView, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/upload/', uploadMusic, name='uploadMusic'),
    path('dashboard/delete/', deleteSong, name='deleteSong'),
    re_path(r'^dashboard/play/(?P<sn>[0-9]+)/$', playMusic, name='playMusic'),
    re_path(r'^dashboard/thumbnail/(?P<sn>[0-9]+)/$', displayThumbnail, name='displayThumbnail'),
]