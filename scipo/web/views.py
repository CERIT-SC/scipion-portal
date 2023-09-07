from django.shortcuts import render
from django.http import HttpResponse
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse

from .api import kubectl, helmctl
from .api.datahub import Datahub


def oidc_callback(request):
    return HttpResponse("Hello, world. You're at the portal index.")

#@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

def privacy_policy(request):
    return render(request, "privacy-policy.html")

def terms_of_use(request):
    return render(request, "terms-of-use.html")

@login_required(login_url="/oidc/authenticate/")
def instance_list(request):
    # OIDC token received from authentication
    oidc_token = request.session.get('oidc_access_token')

    kube_all_instances = kubectl.list_all()
    charts, error = helmctl.list()

    return render(request, "instance-list.html",
        context = {
            'kube_all_instances': kube_all_instances,
            'charts': charts,
            'error': error,
            'token': oidc_token
        })

#@login_required(login_url="/oidc/authenticate/")
def project_list(request):
    # OIDC token received from authentication
    oidc_token = request.session.get('oidc_access_token')

    data_spaces, error = Datahub.list_spaces(oidc_token)

    spaces = list()
    if not error:
        for space_id in data_spaces['spaces']:
            space_data, e = Datahub.get_space(oidc_token, space_id)

            spaces.append({
                'name': '' if e else space_data['name'],
                'space_id': space_data['spaceId']
            })

    site_labels = {
        'header': 'Projects',
        'create_space_btn': 'Project Space',
        'table_header': 'Project Spaces',
        'site_icon': 'fa-hammer'
    }

    return render(request, "space-list.html",
        context = {
            'site_labels': site_labels,
            'available_spaces': spaces,
            'info': "null",
        })

#@login_required(login_url="/oidc/authenticate/")
def dataset_list(request):
    # OIDC token received from authentication
    oidc_token = request.session.get('oidc_access_token')

    data_spaces, error = Datahub.list_spaces(oidc_token)

    spaces = list()
    if not error:
        for space_id in data_spaces['spaces']:
            space_data, e = Datahub.get_space(oidc_token, space_id)

            spaces.append({
                'name': '' if e else space_data['name'],
                'space_id': space_data['spaceId']
            })

    site_labels = {
        'header': 'Datasets',
        'create_space_btn': 'Dataset Space',
        'table_header': 'Dataset Spaces',
        'site_icon': 'fa-database'
    }

    return render(request, "space-list.html",
        context = {
            'site_labels': site_labels,
            'available_spaces': spaces,
            'info': "null",
        })

@login_required(login_url="/oidc/authenticate/")
def create_namespace(request):
    kubectl.create_namespace("frantaflinta")
    return dataset_list(request)

@login_required()
def api_spaces(request):
    result = """
    {"total": 4, "totalNotFiltered": 55, "rows": [{"space_id": "vf08945d3", "name": "5203B", "project": "BALKAN", "subject": "WICK11550 John", "subject__space_id": "s90e46f7f", "subject__birth_date": "1991-01-01", "date": "2022-06-17", "subject__personal_ID": "9101010000", "subject_intials": "J.W.1991", "subject__gender": "F", "subject__handedness": "ns", "subject_age": 31, "comment": "ich", "quality_check": "NOT_OK", "number_of_sessions": 1, "checked": "un"}, {"space_id": "v127bc1ed", "name": "5204B", "project": "BALKAN", "subject": "WICK11550 John", "subject__space_id": "s90e46f7f", "subject__birth_date": "1991-01-01", "date": "2022-06-17", "subject__personal_ID": "9101010000", "subject_intials": "J.W.1991", "subject__gender": "F", "subject__handedness": "ns", "subject_age": 31, "comment": "", "quality_check": "NOT_OK", "number_of_sessions": 1, "checked": "un"}, {"space_id": "v98c295c2", "name": "test123", "project": "test", "subject": "WICK11550 John", "subject__space_id": "s90e46f7f", "subject__birth_date": "1991-01-01", "date": "2022-05-18", "subject__personal_ID": "9101010000", "subject_intials": "J.W.1991", "subject__gender": "F", "subject__handedness": "ns", "subject_age": 31, "comment": "aaa", "quality_check": "NOT_OK", "number_of_sessions": 1, "checked": "un"}, {"space_id": "vce5aec8d", "name": "763A", "project": "HealthBrainAge (HBA)", "subject": "WICK11550 John", "subject__space_id": "s90e46f7f", "subject__birth_date": "1991-01-01", "date": "2021-08-13", "subject__personal_ID": "9101010000", "subject_intials": "J.W.1991", "subject__gender": "F", "subject__handedness": "ns", "subject_age": 30, "comment": "", "quality_check": "NOT_OK", "number_of_sessions": 1, "checked": "un"}]}
    """
    return JsonResponse(result)
