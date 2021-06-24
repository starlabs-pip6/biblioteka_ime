from django.urls import path
from . import views


urlpatterns = [
    # Temporary endpoints to test serializers
    path('backend/', views.backendOverView, name=''),
    path('backend/books', views.booksList, name='home'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook'),
    path('register/', views.register_view, name='register')
]


