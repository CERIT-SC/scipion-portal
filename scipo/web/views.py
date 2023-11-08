import json
import logging
import secrets

from django.shortcuts import render
from django.http import HttpResponse
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib import messages

from .forms import InstancesForm
from .utils import scipo_render

from .api import kubectl, helmctl
from .api.datahub import Datahub
from .api.helm import Helmctl


logger = logging.getLogger('django')

def oidc_callback(request):
    return HttpResponse("Hello, world. You're at the portal index.")

#@login_required(login_url="/login/")
def index(request):
    return scipo_render(request, "index.html")

def privacy_policy(request):
    return scipo_render(request, "privacy-policy.html")

def terms_of_use(request):
    return scipo_render(request, "terms-of-use.html")

@login_required(login_url="/oidc/authenticate/")
def instances(request):
    if request.method == "POST":
        form = InstancesForm(request.POST)

        if form.is_valid():
            response = api_instances(request)
            if response.status_code == 200:
                logger.info("Instance was successfully created.")
                messages.success(request, "Instance was successfully created.")
            else:
                logger.error("Creating the instance failed.")
                messages.error(request, "Creating the instance failed.")

            return HttpResponseRedirect("/instances")
    else:
        form = InstancesForm()

    return scipo_render(request, "instances.html",
        context = {
            'form': form,
        })

@login_required(login_url="/oidc/authenticate/")
def projects(request):
    site_labels = {
        'header': 'Projects',
        'create_space_btn': 'Project Space',
        'table_header': 'Project Spaces',
        'site_icon': 'fa-hammer'
    }

    return scipo_render(request, "spaces.html",
        context = {
            'site_labels': site_labels
        })

@login_required(login_url="/oidc/authenticate/")
def datasets(request):
    site_labels = {
        'header': 'Datasets',
        'create_space_btn': 'Dataset Space',
        'table_header': 'Dataset Spaces',
        'site_icon': 'fa-database'
    }

    return scipo_render(request, "spaces.html",
        context = {
            'site_labels': site_labels
        })
