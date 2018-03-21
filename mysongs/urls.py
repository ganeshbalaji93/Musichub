from django.urls import path
from .import views


urlpatterns = [
    
    path('topratedsong', views.topratedsong, name='Topratedsong'),
    path('topviewedsong', views.topviewedsong, name='Topviewedsongs'),
    path('songsview/songdetails/<int:song_id>', views.songdetails, name='Songdetail'),
    path('songsview/<int:album_id>', views.songsview, name='Songs'),
    path('albumdetails', views.albumdetails, name='Album'),
    path('createnewsong', views.createnewsong, name='CreateSongs'),
    path('createnewalbum', views.createnewalbum, name='CreateAlbum'),

]