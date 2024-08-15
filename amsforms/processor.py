from django.db.models import QuerySet
from .models import FormDefinition, AMSType, AMSObjectType, AMSObjectValue, AMSObjectValueDefault, FormToAMSValueMapping

from epic import processor as epic_processor
import logging
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.DEBUG, filename=f'{ROOT_DIR}/../logs/status.log')


def get_ams_type(form_definition: FormDefinition) -> AMSType:
    return AMSType.objects.filter(Account=form_definition.Account).first()


def get_ams_object_type(ams_type: AMSType, form_definition: FormDefinition) -> AMSObjectType:
    return AMSObjectType.objects.filter(AMSType=ams_type, FormDefinition=form_definition).first()


def get_ams_object_values(ams_object_type: AMSObjectType) -> QuerySet:
    return AMSObjectValue.objects.filter(AMSObjectType=ams_object_type).all()


def get_ams_object_value_defaults(ams_object_type: AMSObjectType) -> QuerySet:
    return AMSObjectValueDefault.objects.filter(AMSObjectType=ams_object_type).all()


def set_default_value(ams_object, ams_value_default: AMSObjectValueDefault):
    setattr(ams_object, ams_value_default.AMSObjectValue.AMSField, ams_value_default.DefaultValue)
    return ams_object


def convert_form_to_ams_object(raw_request: dict, form_definition: FormDefinition) -> str:
    ams_type = get_ams_type(form_definition)
    ams_object_type = get_ams_object_type(ams_type, form_definition)
    results = None
    if ams_object_type.AMSType.AMS == 'EPIC':
        results = epic_processor.convert_form_and_post_to_ams(raw_request, ams_object_type)
    return results
