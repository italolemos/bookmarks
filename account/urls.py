from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # post views
    path('home/', views.create_book, name='index'),
    path('create_book/', views.BookCreateView.as_view(), name='create_book'),
    path('books/', views.books, name='books'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('', views.dashboard, name='dashboard'),
    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),

]
