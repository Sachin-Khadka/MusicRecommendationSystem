from django.urls import path
from .views import * 
from client import views
from client.models import Music, Listenlater, History, Channel, Playlist
from django.db.models import Case, When
from .views import MusicList, MusicDetail, MusicCategory, MusicLanguage, MusicSearch, MusicYear
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('client', HomeView.as_view(), name='client-home'),
    path('music', MusicList.as_view(), name = 'music_list'),
    path('<int:pk>', MusicDetail.as_view(), name = 'music_list'),
    path('category/<str:category>', MusicCategory.as_view(), name='music_category'),
    path('language/<str:lang>', MusicLanguage.as_view(), name='music_language'),
    path('search', MusicSearch.as_view(), name='music_search'),
    path('<slug:slug>', MusicDetail.as_view(), name='music_detail'),
    path('year/<int:year>', MusicYear.as_view(), name='music_year'),
    path('<int:mus_id>/', views.ratingReview, name='ratingreview'),
    path('login/', auth_views.LoginView.as_view(template_name="Login.html"), name = 'login'),
   


   
    path('music_detail/listenlater', views.Listenlater, name='listenlater'),
    path('history/', views.history, name='history'),
    path('c/<str:channel>', views.channel, name='channel'),
    path('upload/', views.upload, name='upload'),
    # path('playlist/', views.playlist, name='playlist'),
    path('recommend/', views.recommend, name='recommend'),
    # path('musics/<int:id>', views.musicpost, name='musicpost'), 
    path('make/', search_function, name='findout'),

]


