from django.contrib import admin
from .models import Actor,Role,Synonym,Wiki
# Register your models here.

admin.site.register(Actor)
admin.site.register(Role)
admin.site.register(Synonym)
admin.site.register(Wiki)