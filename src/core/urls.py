
from django.contrib import admin
from django.urls import path
from . import views
from .api import api

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
