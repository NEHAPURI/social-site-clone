from django.contrib import admin
from . import models

# inline class allow to use admin interface to edit in the parent model itself 
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMembers

    
admin.site.register(models.Group)