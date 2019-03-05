# -*- coding: utf-8 -*-

from django.urls import path,re_path, include
from django.conf.urls import url
from actors import views

urlpatterns = [
                path('',views.ActorList.as_view()),
                path('<str:pk>/roles/',views.ActorAllRoleDetail.as_view()),
                path('<str:pk>/synonyms/',views.ActorAllSynonymDetail.as_view()),
                path('<str:pk>/wikis/',views.ActorAllWikiDetail.as_view()),
                path('<str:pk>/',views.ActorDetail.as_view()),
#                url(r'^<str:actor>/roles/<str:role_name>/([0-9]{4})/([0-9]{2})/([0-9]+)/$',views.ActorRoleDetail.as_view()),
#                re_path(r'^<str:actor>/roles/<str:role_name>/(?P<date>\d{4}-\d{2}-\d{2})/$',views.ActorRoleDetail.as_view()),
                path('<str:actor>/roles/<str:role_name>/<str:start_date>/',views.ActorRoleDetail.as_view()),
                path('<str:actor>/synonyms/<str:synonym>/',views.ActorSynonymDetail.as_view()),
                path('<str:actor>/wikis/<str:wikilink>/',views.ActorWikiDetail.as_view()),
                
        ]