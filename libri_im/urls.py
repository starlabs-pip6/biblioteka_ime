from collections import namedtuple
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import BookCreateView, BookListView, BookDetailView, BookDeleteView, EditBook, ProfilePageView, EditProfile


urlpatterns = [

    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegistationView.as_view(), name='register'),
    path('shfleto/', views.shfleto_view, name='shfleto'),
    path('profile/view/', views.ProfilePageViewDetails, name="profile_page_view"),

    # password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="password_reset/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset/password_reset_done.html"),
         name="password_reset_complete"),

    path('activate/<uidb64>/<token>',
         views.VerificationView.as_view(), name='activate'),

    # Create
    # Temporary endpoints to test serializers
    path('backend/', views.backendOverView, name='backendView'),
    path('backend/books', views.booksList, name='booksList'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook'),

    path('backend/home/',
         BookListView.as_view(template_name="backend/admin_home.html"), name="admin_home"),
    path('backend/book/create/',
         BookCreateView.as_view(template_name="backend/book_create.html"), name='create'),
    path('backend/book/update/<int:pk>/',
         EditBook.as_view(template_name="backend/book_update.html"), name='book_update'),
    path('backend/book/<int:pk>/', BookDetailView.as_view(
        template_name="backend/book_detail.html"), name='book_detail'),
    path('backend/book/delete/<int:pk>/',
         BookDeleteView.as_view(template_name="backend/delete.html"), name='delete'),

    path('profile/', ProfilePageView.as_view(template_name="libri_im/profile_page.html"),
         name="profile_page"),
    path('profile/update/', EditProfile.as_view(
        template_name="libri_im/profile_page_update.html"), name='profile_page_update'),
    path('profile/password', views.MyPasswordChangeView.as_view(
        template_name="registration/change-password.html"), name="change-password"),


]
