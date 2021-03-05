from django.urls import path

from . import views
from .views import MyPicture,getMovies,searchMovie,createMovies,deleteMovie
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^getpictures/', MyPicture.as_view()),
    url(r'^getpictures/', views.getMovies, name="db"),
    url(r'^searchPictures/', views.searchMovie, name="search"),
    url(r'^createPictures/', views.createMovies, name="create"),
    url(r'^deletePictures/', views.deleteMovie, name="create"),
    # url(r'^add/', views.add, name="db"),
    

]