# -*- coding: utf-8 -*-

from rest_framework import serializers
from actors.choices import *
from django.db.models import Q
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Actor
from .models import Role
from .models import Synonym
from .models import Wiki
from django.core.exceptions import ObjectDoesNotExist
from .googleknowledgegraph import GoogleKnowledgeGraph

#class SynonymSerializer(serializers.ModelSerializer):
#    synonyms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#    class Meta:
#        model = Actor
#        fields = ('actor_name','synonyms')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('actor_name','locked')
        extra_kwargs = {
            'actor_name': {'validators': []},
        }   
        #validators=[UniqueValidator(queryset=Actor.objects.filter(~Q(label=DELETED)))]
#    def validate(self, validated_data):
#        print("here")
#        if Actor.objects.filter(~Q(label=DELETED),actor_name=validated_data['actor_name']).exists():
#            raise serializers.ValidationError("actor already exists")
##        if num_results>0:
##            raise serializers.ValidationError("actor already exists")
#        return validated_data
    
    def create(self,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
#            actor_name = validated_data.pop('actor_name')
        actor, created = Actor.all_objects.get_or_create(**validated_data)
        if created:
            print("creating actor")
            actor.label = CREATED
            actor.userid = user
            actor.save()
            gkg = GoogleKnowledgeGraph()
            query = actor.actor_name.replace("_"," ")
            print(query.lower())
            wikis = gkg.getUrl(query=query.lower())
            rank=1
            for wiki in wikis:
                Wiki.objects.create(actor=actor,wikilink=wiki,rank=rank,label=CREATED)
                rank+=1
        elif actor.label == DELETED:
            actor = self.update(actor,validated_data)
        return actor
    
    def update(self,instance,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        instance.actor_name = validated_data['actor_name']
        instance.label = EDITED
        instance.userid = user
        instance.save()
        return instance

class ActorMinimalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('actor_name','locked')

class RoleSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start date must be less than end date")
        if data['start_date'] is None and data['end_date'] is not None:
            raise serializers.ValidationError("end date cannot be specified without a start date")
        return data
    class Meta:
        model = Role
        fields = ('role_name','start_date','end_date')
    
    def create(self,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
#            actor_name = validated_data.pop('actor_name')
        if Actor.all_objects.filter(actor_name=validated_data['actor'].actor_name).count()==0:
            role = Actor.all_objects.create(**validated_data)
            created = True
        else:
            role = Actor.all_objects.get(actor_name=validated_data['actor'])
            created = False
        if created:
            role.label = CREATED
            role.userid = user
            role.save()
        elif role.label == DELETED:
            role = self.update(role,validated_data)
        return role
    
    def update(self,instance,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        instance.actor = validated_data['actor']
        instance.label = EDITED
        instance.userid = user
        instance.save()
        return instance

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ('synonym',)
    
    def create(self,validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        synonym, created = Actor.all_objects.get_or_create(**validated_data)
        if created:
            synonym.label = CREATED
            synonym.userid = user
            synonym.save()
        elif synonym.label == DELETED:
            synonym = self.update(synonym,validated_data)
            synonym.label = CREATED
            synonym.save()
        return synonym
    
    def update(self,instance,validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        instance.actor = validated_data['actor']
        instance.label = EDITED
        instance.userid = user
        instance.save()
        return instance
    
#    def destroy(self,instance,validated_data):
#        print("custom synonym delete")
#        user = None
#        request = self.context.get("request")
#        if request and hasattr(request, "user"):
#            user = request.user
#            user = User.objects.get(username=user)
#        instance.actor = validated_data['actor']
#        instance.label = DELETED
#        instance.userid = user
#        instance.save()
#        return instance

class WikiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wiki
        fields = ('wikilink',)

class ActorRoleSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)
    class Meta:
        model = Actor
        fields = ('actor_name', 'roles')
#    def create(self, validated_data):
        

class ActorSynonymSerializer(serializers.ModelSerializer):
    synonyms = SynonymSerializer(many=True)
    class Meta:
        model = Actor
        fields = ('actor_name', 'synonyms')

class ActorWikiSerializer(serializers.ModelSerializer):
    wikis = WikiSerializer(many=True)
    class Meta:
        model = Actor
        fields = ('actor_name', 'wikis')

class ActorDetailSerializer(serializers.ModelSerializer):
    synonyms = SynonymSerializer(many=True)
    roles = RoleSerializer(many=True)
    wikis = WikiSerializer(many=True)
    def validate(self, data):
        if Actor.all_objects.filter(actor_name=data['actor_name']).count()!=0:
            if Actor.all_objects.get(actor_name=data['actor_name']).locked==True:
                raise serializers.ValidationError("cannot update locked actor")
        return data
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(ActorDetailSerializer, self).__init__(many=many, *args, **kwargs)
    class Meta:
        model = Actor
        fields = ('actor_name','roles','synonyms','wikis','locked')
        extra_kwargs = {
            'actor_name': {
                'validators': [],
            }
        }
        
    def create(self, validated_data):
        roles_data = validated_data.pop('roles')
        synonyms_data = validated_data.pop('synonyms')
        wikis_data = validated_data.pop('wikis')
        actor_name = validated_data.pop('actor_name')
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):        #get user
            user = request.user
            if User.objects.filter(username=user).count()==0:   #remove once user management is done
                user = "admin"
            user = User.objects.get(username=user)
        actor, created = Actor.all_objects.get_or_create(actor_name = actor_name)
#        actor_update = actor
#        if Actor.objects.filter(~Q(labeL=DELETED),actor_name=actor_name).exists():
#        actor, created = Actor.objects.get_or_create(**validated_data)   
        if created or actor.label==DELETED:
            actor.label = CREATED
            actor.userid = user
            actor.save()
#        elif actor.label == DELETED:
#            actor.label = CREATED
#            actor.userid = user
#            actor.save()
        for role in roles_data:
#            if Role.objects.filter(actor=actor,role_name=role['role_name'],
#                                   start_date=role['start_date']).exists():
#                role = 
#            else:
#                role = Role.objects.create(actor = actor, role_name = role['role_name'], 
#                                                           start_date = role['start_date'], 
#                                                           end_date = role['end_date'], userid = user,
#                                                           label = CREATED)
            try:
                role_old = Role.all_objects.get(actor=actor,role_name=role['role_name'])
            except ObjectDoesNotExist:
                role = Role.objects.create(actor = actor, role_name = role['role_name'], 
                                                           start_date = role['start_date'], 
                                                           end_date = role['end_date'], userid = user,
                                                           label = CREATED)
                actor.roles.add(role)
            else: 
                if role_old.label == DELETED:
#                    role = Role.objects.create(actor = actor, role_name = role['role_name'], 
#                                                           start_date = role['start_date'], 
#                                                           end_date = role['end_date'], userid = user,
##                                                           label = CREATED)
                    role_old.label = CREATED
                    role_old.end_date = role['end_date']
                    role_old.start_date = role['start_date']
                    role_old.userid = user
                    role_old.save()
                    actor.roles.add(role_old)
                else:
    #                role_id = Role.objects.get(actor=instance,role_name=role['role_name'],
    #                                  start_date=role['start_date'])
                    role_old.end_date = role['end_date']
                    role_old.start_date = role['start_date']
                    role_old.label = EDITED
                    role_old.userid = user
                    role_old.save()
                
        for synonym in synonyms_data:
#            if Synonym.objects.filter(~Q(label=DELETED),actor=actor,synonym=synonym['synonym']):
#                Synonym.objects.create(actor = actor, synonym = synonym['synonym'])
#                actor_update.synonyms.add(synonym)
#            else:
#                synonym = Synonym.objects.create(actor = actor, synonym = synonym['synonym'], 
#                                                                 userid = user,label = CREATED)
#                actor.synonyms.add(synonym)
            try:
                synonym_old = Synonym.all_objects.get(actor=actor,synonym=synonym['synonym'])
            except ObjectDoesNotExist:
                synonym = Synonym.objects.create(actor = actor, synonym = synonym['synonym'], 
                                                                 userid = user,label = CREATED)
                actor.synonyms.add(synonym)
            else:
                if synonym_old.label == DELETED:
#                    synonym = Synonym.objects.create(actor = actor, synonym = synonym['synonym'], 
#                                                                 userid = user,label = CREATED)
                    synonym_old.label = CREATED
                    synonym_old.userid = user
                    synonym_old.save()
                    actor.synonyms.add(synonym_old)
        
        rank = 0
        for wiki in wikis_data:
#            if Wiki.objects.filter(~Q(label=DELETED),actor=actor, wikilink=wiki['wikilink']):
#                wiki = Wiki.objects.create(actor = actor, wikilink = wiki['wikilink'])
#                actor_update.wikis.add(wiki)
#            else:
#                wiki = Wiki.objects.create(actor = actor, wikilink = wiki['wikilink'], 
#                                                           userid = user, rank = rank,label=CREATED)
#                actor.wikis.add(wiki)
            try:
                wiki_old = Wiki.all_objects.get(actor=actor,wikilink=wiki['wikilink'])
            except ObjectDoesNotExist:
                
                rank+=1
                wiki = Wiki.objects.create(actor = actor, wikilink = wiki['wikilink'],
                                                           userid = user, rank = rank,label=CREATED)
                actor.wikis.add(wiki)
            else:
                if wiki_old.label == DELETED:
#                    wiki = Wiki.objects.create(actor = actor, wikilink = wiki['wikilink'], 
#                                                           userid = user, rank = rank,label=CREATED)
                    wiki_old.label = CREATED
                    wiki_old.userid = user
                    wiki_old.save()
                    actor.wikis.add(wiki_old)
                
#        actor_serializer = ActorSerializer(validated_data.get('actor_name'))
#        print(actor_serializer)
#        actor_serializer.save()
        return actor
    
    def update(self, instance, validated_data):
        instance = self.create(validated_data)
#        instance.actor_name = validated_data.get('actor_name',instance.actor_name)
#        instance.save
#        
#        roles = validated_data.get('roles')
#        synonyms = validated_data.get('synonyms')
#        wikis = validated_data.get('wikis')
#        
#        user = None
#        request = self.context.get("request")
#        if request and hasattr(request, "user"):
#            user = request.user
#            user = User.objects.get(username=user)
#            
#        for role in roles:
#            try:
#                role_id = Role.all_objects.get(actor=instance,role_name=role['role_name'],
#                                      start_date=role['start_date'])
#            except ObjectDoesNotExist:
#                Role.objects.create(actor=instance,role_name=role['role_name'],
#                                  start_date=role['start_date'], end_date=role['end_date'],label=CREATED,
#                                  userid=user)
#            else:
#                if  role_id.label == DELETED:
#                    role_id.label = CREATED
#                    role_id.end_date = role['end_date']
#                    role_id.userid = user
#                    role_id.save()
#                else:
#    #                role_id = Role.objects.get(actor=instance,role_name=role['role_name'],
#    #                                  start_date=role['start_date'])
#                    role_id.end_date = role['end_date']
#                    role_id.label = EDITED
#                    role_id.userid = user
#                    role_id.save()
#        
#        for synonym in synonyms:
#            try:
#                synonym_id = Synonym.all_objects.get(actor=instance,synonym=synonym['synonym'])
#            except ObjectDoesNotExist:
#                Synonym.objects.create(actor=instance, synonym=synonym['synonym'],
#                                  label=CREATED,userid=user)
#            else: 
#                if  synonym_id.label == DELETED:
#                    synonym_id.label = CREATED
#                    synonym_id.synonym = synonym['synonym']
#                    synonym_id.userid = user
#                    synonym_id.save()
#                else:
#                    synonym_id = Synonym.objects.get(actor=instance,synonym=synonym['synonym'])
#                    synonym_id.label = EDITED
#                    synonym_id.userid = user
#                    synonym_id.save()
#                
#        for wiki in wikis:
#            try:
#                wiki_id = Wiki.all_objects.get(actor=instance,wikilink=wiki['wikilink'])
#            except ObjectDoesNotExist:
#                Wiki.objects.create(actor=instance,wikilink=wiki['wikilink'], rank=1, label=CREATED,
#                                    userid=user)
#                
#            else:
#                if  wiki_id.label == DELETED:
#                    wiki_id.label = CREATED
#                    wiki_id.wikilink = wiki['wikilink']
#                    wiki_id.rank = 1
#                    wiki_id.userid = user
#                    wiki_id.save()
#                else:
#                    wiki_id = Wiki.objects.get(actor=instance,wikilink=wiki['wikilink'])
#                    wiki_id.rank = 1
#                    wiki_id.label = EDITED
#                    wiki_id.userid = user
#                    wiki_id.save()
                
        return instance
    
#class ActorAllSerializer(serializers.ModelSerializer):
#    actors = ActorDetailSerializer(many = True)
#    class Meta:
#        model = Actor
#        fields = ('actor_name','actors',)




#class ActorDetailRoleSerializer(serializers.ModelSerializer):
#    #roles = RoleSerializer(many=True)
#    class Meta:
#        model = Role
#        fields = ('actor','role_name','start_date','end_date')
#    
#    def update(self, instance, validated_data):
#        actor_data = validated_data.pop('actor_names')
#        
#        instance.role_name = validated_data.get('role_name',instance.role_name)
#        instance.start_date = validated_data.get('start_date',instance.start_date)
#        instance.end_date = validated_data.get('end_date',instance.end_date)
#        
#        roles_list = []
#        
#        for role in roles_data:
#            role, created = Role.objects.get_or_create()

