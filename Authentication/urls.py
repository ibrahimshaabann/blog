from django.urls import path
from Authentication.views import register, login


urlpatterns = [
    path('Authentication/register', register, name ='UserRegister' ),
    path('Authentication/login', login, name= "UserLogin")
]