from django.db import models
#from django.db.models import When
from django.contrib.auth.models import User
from actors.choices import *
from actors.managers import SoftDeletionManager
# Create your models here.

class SoftDeletionModel(models.Model):
    label = models.IntegerField(null=False, default = 1, choices=LABEL_CHOICES)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        print(self.label)
        self.label = 4
        self.save()
        print("after save")
        print(self.label)

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()
    
    def _on_delete(self,user):
        for relation in self._meta._relation_tree:
            on_delete = getattr(relation.remote_field, 'on_delete', models.DO_NOTHING)
            print(relation.remote_field)
            if on_delete in [None, models.DO_NOTHING]:
                print(relation.remote_field)
                continue
      
#          snapshot_kwargs = {}
      
#          if issubclass(relation.model, SoftDeleteModel):
#            snapshot_kwargs['snapshot_id'] = self.snapshot_id
      
            filter = {relation.name: self}
#          related_queryset = relation.model.objects.filter(**filter)
            
            if on_delete == models.CASCADE:
                relation.model.objects.filter(**filter).delete(user)
#          elif on_delete == models.SET_NULL:
#            for r in related_queryset.all():
              # We'll define SnapshotRecord later in this post
#              SnapshotRecord.objects.get_or_create(
#                snapshot=self.snapshot,
#                record_id=r.pk,
#                foreign_key='{}:{}'.format(relation.name, self.pk))
#            related_queryset.update(**{relation.name: None})
#          elif on_delete == models.PROTECT:
#            if related_queryset.count() > 0:
#              raise ProtectedError()
#          else:
#              raise(NotImplementedError())

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
    def getMinValue(self):
        return self.min_value
    def getMaxValue(self):
        return self.max_value

class Actor(SoftDeletionModel):
    userid = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True)
    actor_name = models.CharField(max_length=100, primary_key=True, default = ' ')
    locked = models.BooleanField(default=False,blank=True)
#    DELETED = 'DLT'
#    EDITED = 'EDT'
#    CREATED = 'CRT'
#    SYSTEM = 'SYS'
#    LABEL_CHOICES = (
#        (DELETED,"deleted"),
#        (EDITED,"edited"),
#        (CREATED,"created"),
#        (SYSTEM,"system")
#        )
    #label = models.IntegerField(null=False, default = 1, choices=LABEL_CHOICES)
    class Meta:
        ordering = ('actor_name',)
    def __str__(self):
        return self.actor_name

class Role(SoftDeletionModel):
    userid = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True)
    actor = models.ForeignKey(Actor, related_name = 'roles', on_delete = models.CASCADE)
    role_name = models.CharField(max_length=100, null=False)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
#    DELETED = 'DLT'
#    EDITED = 'EDT'
#    CREATED = 'CRT'
#    SYSTEM = 'SYS'
#    LABEL_CHOICES = (
#        (DELETED,"deleted"),
#        (EDITED,"edited"),
#        (CREATED,"created"),
#        (SYSTEM,"system")
#        )
#    label = models.IntegerField(null=False, default = 1, choices=LABEL_CHOICES)
    class Meta:
        unique_together = ('actor', 'role_name')
        ordering = ('actor','role_name',)
    
    def __str__(self):
        return str(self.actor) + '-' + self.role_name
        
class Synonym(SoftDeletionModel):
    userid = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True)
    actor = models.ForeignKey(Actor, related_name = 'synonyms', on_delete = models.CASCADE)
    synonym = models.CharField(max_length=100, null=False)
#    DELETED = 'DLT'
#    EDITED = 'EDT'
#    CREATED = 'CRT'
#    SYSTEM = 'SYS'
#    LABEL_CHOICES = (
#        (DELETED,"deleted"),
#        (EDITED,"edited"),
#        (CREATED,"created"),
#        (SYSTEM,"system")
#        )
    #label = models.IntegerField(null=False, default = 1, choices=LABEL_CHOICES)
    class Meta:
        unique_together = ('actor', 'synonym')
        ordering = ('actor','synonym',)
        
class Wiki(SoftDeletionModel):
    userid = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True)
    actor = models.ForeignKey(Actor, related_name = 'wikis', on_delete = models.CASCADE)
    wikilink = models.CharField(max_length=500, null=False)
    rank = models.IntegerField()
#    DELETED = 'DLT'
#    EDITED = 'EDT'
#    CREATED = 'CRT'
#    SYSTEM = 'SYS'
#    LABEL_CHOICES = (
#        (DELETED,"deleted"),
#        (EDITED,"edited"),
#        (CREATED,"created"),
#        (SYSTEM,"system")
#        )
#    label = models.IntegerField(null=False, default = 1, choices=LABEL_CHOICES)
    class Meta:
        unique_together = ('actor', 'wikilink')
        ordering = ('actor','rank')
        

#class SoftDeletionManager(models.Manager):
#    def __init__(self, *args, **kwargs):
#        self.alive_only = kwargs.pop('alive_only', True)
#        super(SoftDeletionManager, self).__init__(*args, **kwargs)
#
#    def get_queryset(self):
#        if self.alive_only:
#            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
#        return SoftDeletionQuerySet(self.model)
#
#    def hard_delete(self):
#        return self.get_queryset().hard_delete()
#    
#class SoftDeletionModel(models.Model):
#    deleted_at = models.DateTimeField(blank=True, null=True)
#
#    objects = SoftDeletionManager()
#    all_objects = SoftDeletionManager(alive_only=False)
#
#    class Meta:
#        abstract = True
#
#    def delete(self):
#        self.deleted_at = timezone.now()
#        self.save()
#
#    def hard_delete(self):
#        super(SoftDeletionModel, self).delete()

