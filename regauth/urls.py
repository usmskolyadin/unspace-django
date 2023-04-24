from django.urls import path, include, re_path
from . import views
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as authViews
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('register/', views.regauth, name="register"),
    path('auth/', auth_views.LoginView.as_view(template_name='regauth/auth.html'), name='auth'),
    path('logout/', authViews.LogoutView.as_view(next_page='auth'), name='logout'),
    path('profile/', views.profile, name="profile"),
    path('editprofile/', views.userform, name="editprofile"),
    path('profile/<str:slug>', views.GetProfile.as_view(), name="account"),
    path('images/addimage', views.ImageCreateView.as_view(), name="imagesform"),
    path('tag/<str:slug>', views.ProfileTaggit, name='profiletag'),
    path('profiles', views.SearchProfileResultsView.as_view(), name='profiles'),
    path('updateimage/<int:pk>', views.ImageUpdateView.as_view(), name="updateimage"),
    path('deletedelete/<int:pk>', views.ImageDeleteView.as_view(), name="deleteimage"),
    path('raiting/<int:pk>/plus', views.like_view, name='raiting'),
    path('password-reset/', 
         PasswordResetView.as_view(
            template_name='regauth/password_reset.html',
            html_email_template_name='regauth/password_reset_email.html'
        ),
        name='password-reset'
    ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='regauth/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='regauth/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='regauth/password_reset_complete.html'),name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
