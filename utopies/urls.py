from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.utopies, name="utopies"),
    path('tags/coding', views.coding, name="coding"),
    path('about', views.about, name="about"),
    path('tags/neirone', views.neirone, name="neirone"),
    path('tags/design', views.design, name="design"),
    path('tags/marketing', views.marketing, name="marketing"),

    path('utopiacreate', views.UtopiaCreateView.as_view(), name="utopiaform"),
    path('utopia/<int:pk>-<str:slug>', views.UtopiaView.as_view(), name="utopia"),
    path('<int:pk>/update', views.UtopiaUpdateView.as_view(), name="update"),
    path('user-agreement', views.useragreement, name="user-agreement"),
    path('private-policy', views.privatypolicy, name="privaty-policy"),
    path('<int:pk>/delete', views.UtopiaDeleteView.as_view(), name="delete"),
    path('<str:username>/utopies',
         views.UserUtopiesListView.as_view(), name="user-utopies"),
    path('tag/<str:slug>', views.UtopiaTaggit, name='tagutopies'),

    path('comment/<str:slug>', views.AddUtopiaComment.as_view(), name="comment"),
    path('updatecomment/<int:pk>',
         views.UtopiaEditComment.as_view(), name="updatecomment"),
    path('deletecomment/<int:pk>',
         views.UtopiaDeleteComment.as_view(), name="deletecomment"),

    path('utopia/<int:pk>/like', views.like_view, name='utopialike'),


]
