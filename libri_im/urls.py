from collections import namedtuple
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CommentEditView,CommentDeleteView,BookCreateView,EventCreateView, BookListView, BookDetailView, BookDeleteView, EditBook, ProfilePageView, EditProfile, BookDV,AddCommentDislike,AddCommentLike,CommentReplyView,AddChildCommentDislike,AddChildCommentLike,ProfileDetailView, send_friend_request


urlpatterns = [

    path('', views.home1,name="home1"),
    path('profile/', views.ProfilePageViewDetails,name="profile1"),
    path('login/', views.login_view, name="login1"),
   path('register/', views.RegistationView.as_view(), name='register1'),
    path('discover/',views.discover1, name="discover1"),
    path('backend/home/',
         BookListView.as_view(template_name="backend1/admin_home1.html"), name="admin_home1"),
    path('backend/book/<int:pk>/', BookDetailView.as_view(
        template_name="backend1/book_detail1.html"), name='book_detail1'),
      path('backend/book1/update1/<int:pk>/',
         EditBook.as_view(template_name="backend1/book_update1.html"), name='book_update1'),
      path('backend/book1/create1/',
         BookCreateView.as_view(template_name="backend1/book_create1.html"), name='create1'),
          path('backend/book/delete/<int:pk>/',
         BookDeleteView.as_view(template_name="backend1/delete1.html"), name='delete1'),

    path('', views.home1, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.RegistationView.as_view(), name='register'),
    path('shfleto/', views.shfleto_view, name='shfleto'),
    path('profile/view/', views.ProfilePageViewDetails, name="profile_page_view"),
    path('libri/<str:isbn>', BookDV.as_view(), name='book-detail'),
    path('user/survey', views.userSurvey, name='survey'),
    path('events', views.eventsView, name='events'),





    #Comment likes and dislikes and replies
    path('libri/<str:isbn>/comment/<int:pk>/reply', CommentReplyView.as_view(), name="comment-reply"), 
    path('libri/<str:isbn>/comment/<int:pk>/like', AddCommentLike.as_view(), name="comment-like"), 
    path('libri/<str:isbn>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name="comment-dislike"), 
    path('libri/<str:isbn>/comment/<int:pk>/childlike', AddChildCommentLike.as_view(), name="child-comment-like"), 
    path('libri/<str:isbn>/comment/<int:pk>/childdislike', AddChildCommentDislike.as_view(), name="child-comment-dislike"), 
    path('libri/<str:isbn>/comment/commentdelete/<int:pk>/', CommentDeleteView.as_view(), name="comment-delete"),
    path('libri/<str:isbn>/comment/commentedit/<int:pk>/', CommentEditView.as_view(), name="comment-edit"),

     #friend system
    path('find/friends/', views.findFriends, name="findFriends"),
    path('profile/view/<int:pk>', ProfileDetailView.as_view(), name="profile-view"),
    path('friend_request/',views.send_friend_request,name="friend-request"),
    # password reset - write your email to send you a link
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="password_reset/password_reset.html"),
         name="reset_password"),
     #message that tells you that an email is sent to you
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset/password_reset_sent.html"),
         name="password_reset_done"),
     #write your new password and confirm it
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset/password_reset_form.html"),
         name="password_reset_confirm"),
     #your password is change, now login with a new password
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset/password_reset_done.html"),
         name="password_reset_complete"),

    path('activate/<uidb64>/<token>',
         views.VerificationView.as_view(), name='activate'),

     #admin_home
    path('backend/home/',
         BookListView.as_view(template_name="backend/admin_home.html"), name="admin_home"),
     #create a book - admin_home
    path('backend/book/create/',
         BookCreateView.as_view(template_name="backend/book_create.html"), name='create'),
     #update a book - admin_home
    path('backend/book/update/<int:pk>/',
         EditBook.as_view(template_name="backend/book_update.html"), name='book_update'),
     #view details of a book - admin_home
    path('backend/book/<int:pk>/', BookDetailView.as_view(
        template_name="backend/book_detail.html"), name='book_detail'),
     #delete a book - admin_home
    path('backend/book/delete/<int:pk>/',
         BookDeleteView.as_view(template_name="backend/delete.html"), name='delete'),
     path('backend/event/create/',
         EventCreateView.as_view(template_name="backend1/create_event.html"), name='createEvent'),     
     
    path('profile/', ProfilePageView.as_view(template_name="libri_im/profile_page.html"),
         name="profile_page"),
    path('profile/update/', EditProfile.as_view(
        template_name="libri_im/profile_page_update.html"), name='profile_page_update'),
    path('profile/password', views.MyPasswordChangeView.as_view(
        template_name="registration/change-password.html"), name="change-password"),

    path('profile/view', views.ProfilePageViewDetails, name="profile_page_view"),


    # POST DATA URLS
    path('postdata/wtr', views.wantToReadPost, name='post_wtr'),
    path('postdata/reading', views.ReadingPost, name='post_reading'),
    path('postdata/read', views.ReadPost, name='post_read'),
    path('postdata/progress', views.progressPost, name='post_progress'),
    path('postdata/selectbook', views.selectBookPost, name='post_selectBook'),
    path('postdata/friendrequest', views.friendRequestPost, name='post_friendrequest'),
    path('postdata/category', views.categoryPost, name='post_category'),
    path('postdata/events', views.post_addevent, name='post_addevent'),
    
     
    # GET DATA URLS
    path('getdata/wtr', views.getdataWtr, name="get_wtr"),
    path('getdata/reading', views.getdataReading, name="get_reading"),
    path('getdata/read', views.getdataRead, name="get_read"),
    path('getdata/progress', views.getdataProgress, name="get_progress"),
    path('getdata/selectbook', views.getdataSelectBook, name="get_selectBook"),
    path('getdata/friendRequest', views.getdataFriendRequest, name="get_friendrequest"),
    path('getdata/searched', views.getSearched, name="get_searched"),
    path('getdata/category', views.getCategory, name="get_category"),
    path('getdata/events', views.getEvents, name="get_events"),

]
