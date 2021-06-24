from django.urls import path
from . import views


urlpatterns = [
    # Temporary endpoints to test serializers
    path('backend/', views.backendOverView, name='home'),
    path('backend/books', views.booksList, name='booksList'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook'),
    path('register/', views.register_view, name='register')
]


