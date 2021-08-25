"""webmark2 URL Configuration

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
import os
from qleader.views import (compare_detail, result_receiver, detail, delete_result,
                           home, leaderboard, invoke_leaderboard, get_token,
                           change_publicity, get_leaderboard_distances,
                           download_result, profile, modify_info, modify_profile,
                           user_logout, get_fci_values)
from django.urls import path, include, re_path
# from django.contrib import admin


ROOT_DIR = os.getenv("ROOT_DIR")
urlpatterns = [
    path(ROOT_DIR + 'api/<int:result_id>/', detail),
    path(ROOT_DIR + 'api/<int:result_id>/delete/', delete_result),
    path(ROOT_DIR + 'api/<int:result_id>/change_publicity/', change_publicity),
    path(ROOT_DIR + 'api/<int:result_id>/download/<str:type>/', download_result),
    path(ROOT_DIR + 'api/<int:result_id>/modify_info/', modify_info),
    path(ROOT_DIR + 'api/distances/', get_leaderboard_distances),
    path(ROOT_DIR + 'api/fci/<str:basis_set>/', get_fci_values),
    path(ROOT_DIR + 'api/', result_receiver),
    path(ROOT_DIR + 'leaderboard/', leaderboard),
    path(ROOT_DIR + 'leaderboard/<str:criterion>/', invoke_leaderboard, name='invoke_leaderboard'),
    path(ROOT_DIR + 'api/compare/', compare_detail),
    re_path(ROOT_DIR + '', include('social_django.urls', namespace='social')),
    path(ROOT_DIR + 'auth/logout/', user_logout),
    re_path(ROOT_DIR + 'auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(ROOT_DIR + 'user/<int:user_id>/', profile),
    path(ROOT_DIR + 'user/<int:user_id>/modify_profile/', modify_profile),
    path(ROOT_DIR + 'get-token/', get_token),
    # path(ROOT_DIR + 'admin/', admin.site.urls),
    path(ROOT_DIR + '', home),
]
