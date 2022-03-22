from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', login,name='login'),
    path('home', home,name='home'),
    path('encrypt/', show_encryption,name='encrypt'),
    path('decrypt/',show_decryption,name='decrypt'),
]
