import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from amsforms.models import JotformParameters, CognitoParameters
from . import processor


@csrf_exempt
def JotformWebhook(request):
    if request.method == 'POST':
        raw_request = request.POST['rawRequest']
        username = request.POST['username']
        jotform_form_id = request.POST['formID']

        jotform_parameters = None
        if jotform_form_id:
            jotform_parameters = JotformParameters.objects.filter(FormID=jotform_form_id, Username=username).first()

        if jotform_parameters:
            payload = json.loads(raw_request)
            processor.convert_form_to_ams_object(payload, form_definition=jotform_parameters.FormDefinition)
        return HttpResponse(200, content_type='application/json')


@csrf_exempt
def CognitoWebhook(request):
    if request.method == 'POST':
        raw_request = json.loads(request.body)
        form_id = raw_request['Form']['Id']
        internal_name = raw_request['Form']['InternalName']
        name = raw_request['Form']['Name']

        cognito_parameters = None
        if form_id and internal_name and name:
            cognito_parameters = CognitoParameters.objects.filter(FormID=form_id, InternalName=internal_name, Name=name).first()

        if cognito_parameters:
            processor.convert_form_to_ams_object(raw_request['PersonalInformation'], form_definition=cognito_parameters.FormDefinition)
        return HttpResponse(200, content_type='application/json')



