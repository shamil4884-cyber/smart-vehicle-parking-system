"""
URL configuration for smart_parking_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from parking_app import views

urlpatterns = [
    path('sys-admin/', admin.site.urls), # Rename standard admin so it doesn't conflict with our dashboard url admin/
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('mall/', views.mall_dashboard, name='mall_dashboard'),
    
    path('user-mange/', views.user_mange, name='user_mange'),
    path('mange-malls/', views.mange_malls, name='mange_malls'),
    
    path('post-complaint/', views.post_complaint, name='post_complaint'),
    path('forward-complaint/<int:complaint_id>/', views.forward_complaint, name='forward_complaint'),
    path('post-reply/<int:complaint_id>/', views.post_reply, name='post_reply'),
    path('api/chatbot/', views.chatbot_response, name='chatbot'),
]
