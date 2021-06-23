from django.urls import path
from . import views


urlpatterns = [
    # Temporary endpoints to test serializers
    path('backend/', views.backendOverView, name='apiOverView'),
    path('backend/books', views.booksList, name='booksList'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook')
]


