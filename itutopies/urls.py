from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.itutopies, name="itutopies"),
    path('itopia/<int:pk>-<str:slug>', views.ITUtopiaView.as_view(), name="itopia"),
    path('<int:pk>/updateit', views.ItopiaUpdateView.as_view(), name="updateit"),
    path('<int:pk>/deleteit', views.ItopiaDeleteView.as_view(), name="deleteit"),
    path('itutopiaform', views.ITUtopiaCreateView.as_view(), name="itutopiaform"),
    path('tag/<str:slug>', views.ITUtopiaTaggit, name='tagit'),
    path('<str:username>/itutopies', views.UserITUtopiesListView.as_view(), name="user-itutopies"),
    path('search/', views.SearchResultsViewIT.as_view(), name="searchit"),
    path('searchit/', views.itsearch, name="itsearch"),
    path('itcomment/<str:slug>', views.AddITUtopiaComment.as_view(), name="itcomment"),
    path('updateitcomment/<int:pk>', views.ITUtopiaEditComment.as_view(), name="updateitcomment"),
    path('deleteitcomment/<int:pk>', views.ITUtopiaDeleteComment.as_view(), name="deleteitcomment"),
    path('itopia/<int:pk>/like', views.itlike_view, name='itopialike'),

]
