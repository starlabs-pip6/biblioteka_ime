from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import BookCreateView, BookListView,BookDetailView,BookDeleteView, BookUpdateView


urlpatterns = [
    # Temporary endpoints to test serializers
   


    
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    #password reset
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_done.html"), 
        name="password_reset_complete"),

    #Create

    path('backend/', views.backendOverView, name='backendView'),
    path('backend/books', views.booksList, name='booksList'),
    path('backend/books/<str:pk>/', views.specificBook, name='specificBook'),

    path('backend/home/', BookListView.as_view(template_name="backend/admin_home.html"), name="admin_home"),
    path('backend/book/create/', BookCreateView.as_view(template_name="backend/book_create.html"), name='create'),  
    path('backend/book/update/<int:pk>/', BookUpdateView.as_view(template_name="backend/book_update.html"), name='book_update'),
    path('backend/book/<int:pk>/', BookDetailView.as_view(template_name="backend/book_detail.html"), name='book_detail'),  
    path('backend/book/delete/<int:pk>/',BookDeleteView.as_view(template_name="backend/delete.html"),name='delete'),
]


