import json
from django.shortcuts import render


def read_post(request):
    form_id = request.POST.get('formID')
    form_title = request.POST.get('formTitle')
    json_message = request.POST.get('rawRequest')
    submission_id = request.POST.get('submissionID')
    username = request.POST.get('username')
    pretty = request.POST.get('pretty')

