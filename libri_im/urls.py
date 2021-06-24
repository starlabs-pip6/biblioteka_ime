from django.urls import path
from . import views


urlpatterns = [
    # Temporary endpoints to test serializers
    path('backend/', views.backendOverView, name='backendView'),
    path('backend/books', views.booksList, name='booksList'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook'),


    path('', views.home_view, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),


]


