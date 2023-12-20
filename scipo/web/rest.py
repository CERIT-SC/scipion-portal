import json
import logging
import secrets

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from .api import kubectl, helmctl, datahubctl
from .api.helm import Helmctl


logger = logging.getLogger('django')

@login_required(login_url="/oidc/authenticate/")
def api_spaces(request):
    if   request.method == "GET":
        spaces = api_spaces_get(request)
        j = json.loads(json.dumps(spaces))
        return JsonResponse(j, safe=False)
    else:
        return HttpResponse(status=405) # 405 Method Not Allowed

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

    data_spaces = datahubctl.list_spaces(oidc_token)

    spaces = list()
    if data_spaces:
        for space_id in data_spaces['spaces']:
            space_data = datahubctl.get_space(oidc_token, space_id)

            try:
                provider_id = list(space_data['providers'].keys())[0]

                provider_data = datahubctl.get_provider(oidc_token, provider_id)

                entry = {
                    'name': '' if not space_data else space_data['name'],
                    'space_id': space_data['spaceId'],
                    'provider_url': provider_data['domain']
                }
                spaces.append(entry)
            except:
                logger.warning(f"Space with ID {space_id} does not contain any provider or other data are missing.")

    return spaces

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
        chart["link"]           = instance_info.get("link", "")
        chart["health"]         = instance_info.get("health", "")
        chart["friendly_phase"] = instance_info.get("friendly_phase", "")
    return JsonResponse(j, safe=False)

def api_instances_post(request, name):
    # Extract parameters from the request and save
    instance_name = request.POST.get('instance_name')

    # Get Space IDs from their names
    dataset_space_name = request.POST.get('od_dataset_space_name')
    project_space_name = request.POST.get('od_project_space_name')
    for space in api_spaces_get(request):
        if dataset_space_name == space['name']:
            dataset_space_id = space['space_id']
            dataset_space_provider_url = space['provider_url']
        if project_space_name == space['name']:
            project_space_id = space['space_id']
            project_space_provider_url = space['provider_url']

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
        'od.dataset.host':         dataset_space_provider_url,
        'od.dataset.token':        request.POST.get('od_dataset_token'),
        'od.dataset.spaceId':      dataset_space_id,
        'od.dataset.spaceIdShort': dataset_space_id[0:8],
        'od.project.host':         project_space_provider_url,
        'od.project.token':        request.POST.get('od_project_token'),
        'od.project.spaceId':      project_space_id,
        'od.project.spaceIdShort': project_space_id[0:8]
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
