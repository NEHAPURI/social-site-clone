from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from . models import Group, GroupMembers
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from . import models

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group        

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMembers.objects.create(user=self.request.user,group=group)
        except IntegrityError: 
            messages.warning(self.request,'warning already a memeber')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(self.request,*args,**kwargs)        

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership= models.GroupMembers.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMembers.DoesNotExits:
            messages.warning(self.request,'Sorry you are in this group! ')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')
        return super().get(request,*args,**kwargs)    


    
    