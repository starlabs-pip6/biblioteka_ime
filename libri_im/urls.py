from collections import namedtuple
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CommentEditView,CommentDeleteView,BookCreateView, BookListView, BookDetailView, BookDeleteView, EditBook, ProfilePageView, EditProfile, BookDV,AddCommentDislike,AddCommentLike,CommentReplyView,AddChildCommentDislike,AddChildCommentLike,ProfileDetailView, send_friend_request


urlpatterns = [

    path('team6/', views.home_view, name='home'),
    path('team6/login/', views.login_view, name='login'),
    path('team6/logout/', views.logout_view, name='logout'),
    path('team6/register/', views.RegistationView.as_view(), name='register'),
    path('team6/shfleto/', views.shfleto_view, name='shfleto'),
    path('team6/profile/view/', views.ProfilePageViewDetails, name="profile_page_view"),
    path('team6/libri/<str:isbn>', BookDV.as_view(), name='book-detail'),
    path('team6/user/survey', views.userSurvey, name='survey'),
    path('team6/events', views.eventsView, name='events'),



    path('team6/home1/', views.home1,name="home1"),
    path('team6/home1/profile', views.ProfilePageViewDetails,name="profile1"),
    path('team6/login1/', views.login_view, name="login1"),
   path('team6/register1/', views.RegistationView.as_view(), name='register1'),
    path('team6/discover1/',views.discover1, name="discover1"),
    path('team6/backend1/home1/',
         BookListView.as_view(template_name="backend1/admin_home1.html"), name="admin_home1"),
    path('team6/backend1/book1/<int:pk>/', BookDetailView.as_view(
        template_name="backend1/book_detail1.html"), name='book_detail1'),
      path('team6/backend1/book1/update1/<int:pk>/',
         EditBook.as_view(template_name="backend1/book_update1.html"), name='book_update1'),
      path('team6/backend1/book1/create1/',
         BookCreateView.as_view(template_name="backend1/book_create1.html"), name='create1'),
          path('team6/backend1/book1/delete1/<int:pk>/',
         BookDeleteView.as_view(template_name="backend1/delete1.html"), name='delete1'),

    #Comment likes and dislikes and replies
    path('team6/libri/<str:isbn>/comment/<int:pk>/reply', CommentReplyView.as_view(), name="comment-reply"), 
    path('team6/libri/<str:isbn>/comment/<int:pk>/like', AddCommentLike.as_view(), name="comment-like"), 
    path('team6/libri/<str:isbn>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name="comment-dislike"), 
    path('team6/libri/<str:isbn>/comment/<int:pk>/childlike', AddChildCommentLike.as_view(), name="child-comment-like"), 
    path('team6/libri/<str:isbn>/comment/<int:pk>/childdislike', AddChildCommentDislike.as_view(), name="child-comment-dislike"), 
    path('team6/libri/<str:isbn>/comment/commentdelete/<int:pk>/', CommentDeleteView.as_view(), name="comment-delete"),
    path('team6/libri/<str:isbn>/comment/commentedit/<int:pk>/', CommentEditView.as_view(), name="comment-edit"),

     #friend system
    path('team6/find/friends/', views.findFriends, name="findFriends"),
    path('team6/profile/view/<int:pk>', ProfileDetailView.as_view(), name="profile-view"),
    path('team6/friend_request/',views.send_friend_request,name="friend-request"),
    # password reset - write your email to send you a link
    path('team6/reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="password_reset/password_reset.html"),
         name="reset_password"),
     #message that tells you that an email is sent to you
    path('team6/reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset/password_reset_sent.html"),
         name="password_reset_done"),
     #write your new password and confirm it
    path('team6/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset/password_reset_form.html"),
         name="password_reset_confirm"),
     #your password is change, now login with a new password
    path('team6/reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset/password_reset_done.html"),
         name="password_reset_complete"),

    path('team6/activate/<uidb64>/<token>',
         views.VerificationView.as_view(), name='activate'),

     #admin_home
    path('team6/backend/home/',
         BookListView.as_view(template_name="backend/admin_home.html"), name="admin_home"),
     #create a book - admin_home
    path('team6/backend/book/create/',
         BookCreateView.as_view(template_name="backend/book_create.html"), name='create'),
     #update a book - admin_home
    path('team6/backend/book/update/<int:pk>/',
         EditBook.as_view(template_name="backend/book_update.html"), name='book_update'),
     #view details of a book - admin_home
    path('team6/backend/book/<int:pk>/', BookDetailView.as_view(
        template_name="backend/book_detail.html"), name='book_detail'),
     #delete a book - admin_home
    path('team6/backend/book/delete/<int:pk>/',
         BookDeleteView.as_view(template_name="backend/delete.html"), name='delete'),
     
    path('team6/profile/', ProfilePageView.as_view(template_name="libri_im/profile_page.html"),
         name="profile_page"),
    path('team6/profile/update/', EditProfile.as_view(
        template_name="libri_im/profile_page_update.html"), name='profile_page_update'),
    path('team6/profile/password', views.MyPasswordChangeView.as_view(
        template_name="registration/change-password.html"), name="change-password"),

    path('team6/profile/view', views.ProfilePageViewDetails, name="profile_page_view"),


    # POST DATA URLS
    path('team6/postdata/wtr', views.wantToReadPost, name='post_wtr'),
    path('team6/postdata/reading', views.ReadingPost, name='post_reading'),
    path('team6/postdata/read', views.ReadPost, name='post_read'),
    path('team6/postdata/progress', views.progressPost, name='post_progress'),
    path('team6/postdata/selectbook', views.selectBookPost, name='post_selectBook'),
    path('team6/postdata/friendrequest', views.friendRequestPost, name='post_friendrequest'),
    path('team6/postdata/category', views.categoryPost, name='post_category'),
    path('team6/postdata/events', views.post_addevent, name='post_addevent'),
    
     
    # GET DATA URLS
    path('team6/getdata/wtr', views.getdataWtr, name="get_wtr"),
    path('team6/getdata/reading', views.getdataReading, name="get_reading"),
    path('team6/getdata/read', views.getdataRead, name="get_read"),
    path('team6/getdata/progress', views.getdataProgress, name="get_progress"),
    path('team6/getdata/selectbook', views.getdataSelectBook, name="get_selectBook"),
    path('team6/getdata/friendRequest', views.getdataFriendRequest, name="get_friendrequest"),
    path('team6/getdata/searched', views.getSearched, name="get_searched"),
    path('team6/getdata/category', views.getCategory, name="get_category"),
    path('team6/getdata/events', views.getEvents, name="get_events"),

]
