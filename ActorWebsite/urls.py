"""ActorWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from actors import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('actors/',include('actors.urls')),
    path('upload/',views.ActorRoleSynonymWikiList.as_view()),
    path('download/',views.Download.as_view()),
    path('actorRoles/',views.ActorAllRoleList.as_view()),
    path('actorSynonyms/',views.ActorAllSynonymList.as_view()),
    path('actorWikilinks/',views.ActorAllWikiList.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('auth/obtain_token/', obtain_jwt_token),
    path('auth/refresh_token/', refresh_jwt_token),
#    path('actorSynonyms/(?P<synonym>)/', views.ActorSynonymDetail.as_view()),
]
