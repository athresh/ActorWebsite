from actors.choices import *
from django.db import models
class SoftDeletionQuerySet(models.QuerySet):
    def delete(self,user):
        return super(SoftDeletionQuerySet, self).update(label=DELETED,userid=user)

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(label=DELETED)

    def dead(self):
        return self.exclude(deleted_at=None)