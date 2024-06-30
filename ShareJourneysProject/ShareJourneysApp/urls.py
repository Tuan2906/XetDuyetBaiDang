"""
URL configuration for QuanLyKhoaHoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from ShareJourneysApp import views
from .views import *
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register('users', views.UserViewSet, basename='users')
route.register('posts', views.PostViewSet, basename='posts')
route.register('comments', views.CommentViewSet, basename='commentdda')
route.register('reports', views.ReportViewSet, basename='report')
route.register('local',views.LocalViewSet,basename='local')
route.register('picture',views.PictureViewSet,basename='pictures')
route.register('transports',views.TransportationViewSet,basename='transports')
route.register('tags',views.TagViewSet,basename='tags')


urlpatterns = [
    path('', include(route.urls)),
    path('api/send/mail', SendEmail.as_view(), name='Trang Chu'),
    path('changePassword/', ChangePasswordView.as_view(), name='changePassword'),
    path('resetPassword/', PasswordResetView.as_view(), name='resetPassword'),
    path('xetduyet/', views.xet_duyet, name='xetduyet'),
]
