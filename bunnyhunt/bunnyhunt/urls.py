from django.contrib import admin
from django.urls import path

from bunnyapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('game/', views.game, name='game'),
]
