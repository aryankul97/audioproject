from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createaudio/', createaudio),
    path('deleteaudio/', deleteaudio),
    path('updateaudio/', updateaudio),
    path('getaudio/', getaudio),
]
