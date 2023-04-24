from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('unews', views.unews, name="unews"),
    path('search/', views.SearchResultsView.as_view(), name="search")

]

