from django.urls import path
from .views import register, login, logout_user, profile, edit_status



app_name = 'users'

urlpatterns = [
    path('login/', login,  name='login'),
    path('register/', register,  name='register'),
    path('profile/', profile, name='profile'),
    path('delete_patient/<int:status>/', edit_status, name='delete_patient'),
    path('logout/', logout_user,  name='logout'),
]
