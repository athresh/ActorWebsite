from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from actors.choices import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import Http404
import operator
import datetime
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Actor
from .models import Role
from .models import Synonym
from .models import Wiki
from .serializers import ActorSerializer
from .serializers import ActorDetailSerializer
from .serializers import ActorRoleSerializer
from .serializers import ActorSynonymSerializer
from .serializers import ActorWikiSerializer
from .serializers import RoleSerializer
from .serializers import SynonymSerializer
from .serializers import WikiSerializer
from .serializers import ActorMinimalDetailSerializer
#from .serializers import ActorAllSerializer
# Create your views here.

class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        return obj

# actors/
class ActorList(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    def get(self,request,**kwargs):
        actors = Actor.objects.filter(locked=False)
        serializer = ActorSerializer(actors,many=True)
        #actor_list = Actor.objects.all()
        return Response({'data':serializer.data})
        #return render(request,'actor list.html',{'actor_list': actor_list})
    
# actors/<actor_name>/
class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = None
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        instance._on_delete(user)
        return super(ActorDetail, self).destroy(request,*args,**kwargs)

# upload/
class ActorRoleSynonymWikiList(generics.ListCreateAPIView):
    serializer_class = ActorDetailSerializer
    def get_queryset(self):
        return Actor.objects.filter(~Q(label=DELETED))
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(ActorRoleSynonymWikiList, self).get_serializer(*args, **kwargs)
    
# actorRoles/
class ActorAllRoleList(generics.ListCreateAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorRoleSerializer
    def get_queryset(self):
        return Actor.objects.filter(~Q(label=DELETED))

# actorSynonyms/
class ActorAllSynonymList(generics.ListCreateAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorSynonymSerializer
 
# actorWikilinks/
class ActorAllWikiList(generics.ListCreateAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorWikiSerializer

# actors/<str:pk>/roles/
class ActorAllRoleDetail(generics.RetrieveAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorRoleSerializer

# actors/<str:pk>/synonyms/
class ActorAllSynonymDetail(generics.RetrieveAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorSynonymSerializer
#    def get_queryset(self):
#        print("all syn qs")
#        return Actor.objects.all()

# actors/<str:pk>/wikis/
class ActorAllWikiDetail(generics.RetrieveAPIView):
    #lookup_field = 'actor'
    queryset = Actor.objects.all()
    serializer_class = ActorWikiSerializer
    
# actors/<str:pk>/roles/<str:role_name/
class ActorRoleDetail(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_fields = ('actor','role_name')
    
# actors/<str:pk>/synonyms/<int:pk>/
class ActorSynonymDetail(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Synonym.objects.all()
    serializer_class = SynonymSerializer    
    lookup_fields = ('actor','synonym')
#    def destroy(self, request, *args, **kwargs):
#        print("custom view destroy")
#        user = None
##        request = self.context.get("request")
#        if request and hasattr(request, "user"):
#            user = request.user
#            user = User.objects.get(username=user)
#        
##        instance = self.get_object()
##        instance.user = user
##        instance.label = DELETED
##        instance.save()
#        return Response("Success")
       #return super(ActorSynonymDetail, self).update(request, *args, **kwargs)
 
# actors/<str:pk>/wikis/<int:pk>/
class ActorWikiDetail(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Wiki.objects.all()
    serializer_class = WikiSerializer
    lookup_fields = ('actor','wikilink')

# lockactor/<str:pk>/
class LockActor(generics.RetrieveUpdateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorMinimalDetailSerializer

# download/
class Download(generics.ListAPIView):
    serializer_class = ActorDetailSerializer
    def get_queryset(self):
        return Actor.objects.filter(~Q(label=DELETED)&Q(locked=True))
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(Download, self).get_serializer(*args, **kwargs)