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

from .api import kubectl, helmctl
from .api.datahub import Datahub
from .api.helm import Helmctl


logger = logging.getLogger('django')

@login_required(login_url="/oidc/authenticate/")
def api_spaces(request):
    if   request.method == "GET":    return api_spaces_get(request)
    else:
        HttpResponse(status=405) # 405 Method Not Allowed

@login_required(login_url="/oidc/authenticate/")
def api_instances(request, name = None):
    if   request.method == "GET":    return api_instances_get(request, name)
    elif request.method == "POST":   return api_instances_post(request, name)
    elif request.method == "DELETE": return api_instances_delete(request, name)
    else:
        return HttpResponse(status=405) # 405 Method Not Allowed

def api_spaces_get(request):
    # OIDC token received from authentication
    oidc_token = request.session.get('oidc_access_token')

    data_spaces = Datahub.list_spaces(oidc_token)

    spaces = list()
    if data_spaces:
        for space_id in data_spaces['spaces']:
            space_data = Datahub.get_space(oidc_token, space_id)

            spaces.append({
                'name': '' if not space_data else space_data['name'],
                'space_id': space_data['spaceId']
            })

    j = json.loads(json.dumps(spaces))
    return JsonResponse(j, safe=False)

def api_instances_get(request, name):
    # Get info about apps from the helm
    charts = helmctl.list()

    if not charts:
        return HttpResponse(status=500)

    # Add additional info from the Scipion's controller
    j = json.loads(charts)
    for chart in j:
        instance_info = kubectl.get_instance_info(chart["name"])
        if not instance_info:
            continue

        instance_info = json.loads(instance_info)
        chart["link"] = instance_info["link"]
        chart["health"] = instance_info["health"]
    return JsonResponse(j, safe=False)

def api_instances_post(request, name):
    # Extract parameters from the request and save
    instance_name = request.POST.get('instance_name')

    helm_vars = {
        'instance.releaseChannel': 'dev',
        'instance.prefix': 'scipo',
        'instance.microk8s': 'false',
        'instance.mincpu': '2',
        'instance.maxcpu': '8',
        'instance.minram': '2048Mi',
        'instance.maxram': '8192Mi',
        'instance.keepVolumes': 'true',
        'vnc.useVncClient': 'false',
        'vnc.vncPassword': secrets.token_hex(16),
        'od.dataset.host':         request.POST.get('od_dataset_host'),
        'od.dataset.token':        request.POST.get('od_dataset_token'),
        'od.dataset.spaceId':      request.POST.get('od_dataset_space_id'),
        'od.dataset.spaceIdShort': request.POST.get('od_dataset_space_id', '')[0:8],
        'od.project.host':         request.POST.get('od_project_host'),
        'od.project.token':        request.POST.get('od_project_token'),
        'od.project.spaceId':      request.POST.get('od_project_space_id'),
        'od.project.spaceIdShort': request.POST.get('od_project_space_id', '')[0:8]
    }

    # Validate the params
    if not instance_name:
        return False
    for k, v in helm_vars.items():
        if not v:
            return False

    # Build the Helm command
    helm_cmd_builder = Helmctl.CommandBuilder(instance_name)
    for k, v in helm_vars.items():
        helm_cmd_builder.add_variable(k, v)

    # Install the Helm chart
    if not helmctl.install(helm_cmd_builder):
        return HttpResponse(status=500)

    return HttpResponse(status=200)

def api_instances_delete(request, name):
    if not helmctl.uninstall(name):
        return HttpResponse(status=500)

    return HttpResponse(status=200)
