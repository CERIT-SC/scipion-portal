from django.shortcuts import render
from django.http import HttpResponse
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

def oidc_callback(request):
    return HttpResponse("Hello, world. You're at the portal index.")

#@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

def instance_list(request):
    return render(request, "instance-list.html")
