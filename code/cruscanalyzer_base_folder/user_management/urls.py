from django.urls import path
from user_management import views

app_name = 'user_management'

urlpatterns = [
    path('registration', views.CreateUserView.as_view(), name='user-register'),
    path('login', views.LoginUserView.as_view(), name='user-login'),
    path('logout', views.LogoutUserView.as_view(), name='user-logout'),
    path('profile', views.ProfileView.as_view(), name='user'),
    path('profile/update', views.UpdateUserView.as_view(), name='user-update'),
    path('profile/update', views.UpdateUserView.as_view(), name='user-update'),
    path('profile/delete', views.DeleteUserView.as_view(), name='delete-user')
]
