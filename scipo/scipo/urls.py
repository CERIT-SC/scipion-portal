"""scipo URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instance-list/', views.instance_list, name='instance-list'),
    path('project-list/', views.project_list, name='project-list'),
    path('dataset-list/', views.dataset_list, name='dataset-list'),

    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-use/', views.terms_of_use, name='terms-of-use'),

    # API
    path('api/spaces.json', views.api_spaces, name='api_spaces'),

    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    #path('oidc-callback/', views.oidc_callback, name='oidc-callback'),

    path('__debug__/', include('debug_toolbar.urls')),
]
