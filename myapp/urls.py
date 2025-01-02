"""Transumdocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.login),
    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register),
    path('admin_home',views.admin_home),
    # path('user_home',views.user_home),
    path('admin_manage_user',views.admin_manage_users),
    path('admin_block_user/<int:id>',views.admin_block_user),
    path('admin_unblock_user/<int:id>',views.admin_unblock_user),
    path('user_view_profile',views.user_view_profile),
    path('user_feedback',views.user_feedback),
    path('admin_view_feedbacks',views.admin_view_feedback),
    path('user_complaints',views.user_complaints),
    path('admin_view_complaints',views.admin_view_complaints),
    path('admin_complaint_reply/<int:id>',views.admin_complaint_reply),
    path('user_change_password',views.user_change_password),
    path('user_files',views.user_files),
    path('user_history',views.user_history),
    path('user_header',views.user_header),
    path('otp_for_registration/',views.otp_for_registration),
    path("otp_for_registration_post/",views.otp_for_registration_post),
    path('otp_for_forgot_password',views.otp_for_forgot_password),
    path('forgot_password/',views.forgot_password),
    path("otp_post_forgot/",views.otp_post_forgot),
    path('change_password_on_forgot_password',views.change_password_on_forgot_password),
    path('otp_entering_page',views.otp_entering_page),
    path('user_home',views.process_file),


]
