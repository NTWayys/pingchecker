"""pingChecker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('server/', views.index, name='index'),
    path('server/view/<str:domain>/', views.getDomain),
    path('server/routes/', views.getRoutes),
    path('server/list/', views.getServers),
    path('server/add/', views.addServer),
    path('server/<int:id>/', views.updateServers),
    path('server/<int:id>/update/', views.updateServers),
    path('server/<int:id>/delete/', views.updateServers),

]