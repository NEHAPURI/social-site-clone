from django.db import models
from django.utils.text import slugify # to remove underscore and -
import misaka # Transforms sequences of characters into HTML entities. http://misaka.61924.nl/
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()  # custom template tag

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User, through='Groupmembers')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #self.description_html= misaka.html(self.description) 
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})    
            
    class Meta():
        ordering = ['name']

class GroupMembers(models.Model):
    group = models.ForeignKey(Group,models.DO_NOTHING, related_name='memberships')
    user = models.ForeignKey(User,models.DO_NOTHING,related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta():
        unique_together = ('group','user')    


    

