from django.urls import path, include
from . import views

urlpatterns = [
    path('startups/', views.startups, name="startups"),
    path('startup/<int:pk>/<str:slug>', views.StartupView.as_view(), name="startup"),
    path('startups/<int:pk>/create', views.StartupCreateView.as_view(), name="startupcreate"),
    path('editstartup/<int:pk>',
       views.StartupUpdateView.as_view(), name="startupupdate"),
    path('deletestartup/<int:pk>',
       views.StartupDeleteView.as_view(), name="startupdelete"),
    path('startups/<str:username>/usersstartups', views.StartupUserView.as_view(), name="userstartup"),
    path('searchstar', views.SearchStartupResultsView.as_view(), name="searchstar"),



    path('team/<int:pk>', views.teamview, name="team"),
    path('team/create', views.TeamCreateView.as_view(), name="teamcreate"),
    path('team/<int:pk>/', views.TeamUpdateView.as_view(), name="teamupdate"),
    path('teamupdate/<int:pk>',
       views.TeamUpdateView.as_view(), name="teamupdate"),
    path('deleteteam/<int:pk>',
       views.TeamDeleteView.as_view(), name="teamdelete"),
    path('startups/<str:username>/usersstartups', views.TeamUserView.as_view(), name="userteam"),








    path('startup-owerview/', views.ApiOwerView, name="api-all"),
    path('startup-detail/<str:pk>/', views.startupDetail, name="api-detail"),
    path('startup-list/', views.startupslist, name='api-list'),
    path('startup-create/', views.startupCreate, name='api-create'),
    path('startup-update/<str:pk>', views.startupUpdate, name='api-update'),
    path('startup-delete/<str:pk>', views.startupDelete, name='api-delete'),

] 