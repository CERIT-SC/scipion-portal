
import logging

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import InstancesForm
from .utils import scipo_render
from .rest import api_instances, api_spaces_get


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
    space_names = [item['name'] for item in api_spaces_get(request)]

    # POST
    if request.method == "POST":
        form = InstancesForm(
            space_names,
            space_names,
            request.POST
        )

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
        form = InstancesForm(
            space_names,
            space_names
        )

    # GET
    return scipo_render(request, "instances.html",
        context = {
            'form': form,
        })

@login_required(login_url="/oidc/authenticate/")
def instances_delete(request, name):
    request.method = "DELETE"
    response = api_instances(request, name)
    if response.status_code == 200:
        logger.info("Instance deletion was successful.")
        messages.success(request, "Instance deletion was successful.")
        return HttpResponseRedirect("/instances")

    logger.error("Instance deletion failed.")
    messages.error(request, "Instance deletion failed.")
    return HttpResponseRedirect("/instances")

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
