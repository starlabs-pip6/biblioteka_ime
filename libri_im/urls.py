from django.urls import path
from . import views


urlpatterns = [
    path('api/', views.apiOverView, name='apiOverView'),
    path('api/librat', views.libratList, name='libratList'),
    path('api/librat/<str:pk>/', views.libriSpecifik, name='libriSpecifik')
]


