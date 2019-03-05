# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from actors.choices import *
from actors.querysets import SoftDeletionQuerySet
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(~Q(label=DELETED))
        return SoftDeletionQuerySet(self.model).all()

    def hard_delete(self):
        return self.get_queryset().hard_delete()
