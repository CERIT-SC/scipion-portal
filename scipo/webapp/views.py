from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def oidc_callback(request):
    return HttpResponse("Hello, world. You're at the portal index.")
