from amsforms.models import AMSObjectType, FormToAMSValueMapping, AMSObjectValueDefault
from epic_sdk_scripts_rbdundas.models.Opportunity import Opportunity
from amsforms import processor
from epic import processor as epic_processor
from epic_sdk_scripts_rbdundas.epic_sdk import xml_utilities


def set_opportunity_defaults(opportunity: Opportunity):
    return opportunity


def create_ams_object(ams_object: Opportunity, converted_values: dict, ams_object_type: AMSObjectType) -> Opportunity:
    opportunity = ams_object
    opportunity = set_opportunity_defaults(opportunity)
    mappings = FormToAMSValueMapping.objects.filter(AMSObjectType=ams_object_type).all()
    ams_value_defaults = AMSObjectValueDefault.objects.filter(AMSObjectType__AMSObjectType='Opportunity').all()

    stage = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Opportunity', AMSObjectValue__AMSField='Stage').first()
    stage_group = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Opportunity', AMSObjectValue__AMSField='StageGroup').first()
    stage_weight = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Opportunity', AMSObjectValue__AMSField='StageWeight').first()
    owner_type = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Opportunity', AMSObjectValue__AMSField='OwnerType').first()
    owner_lookup_code = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Opportunity', AMSObjectValue__AMSField='OwnerLookupCode').first()
    premium_field = mappings.filter(AMSObjectValue__AMSField='Premium').first()

    detail_value = opportunity.DetailValue
    detail_value.Stage = stage.DefaultValue
    detail_value.StageGroup = stage_group.DefaultValue
    detail_value.StageWeight = stage_weight.DefaultValue
    detail_value.OwnerType = owner_type.DefaultValue
    detail_value.OwnerLookupCode = owner_lookup_code.DefaultValue
    detail_value.Premium = next(epic_processor.get_value_from_nested_dict(converted_values, premium_field.FormField))
    comments = ''
    comment_mappings = mappings.filter(AMSObjectValue__AMSField='Comments').all()
    for mapping in comment_mappings:
        field = next(epic_processor.get_value_from_nested_dict(converted_values, mapping.FormField))
        comments += field + '\r\n'
    detail_value.Comments = comments
    opportunity.DetailValue = detail_value

    year = next(epic_processor.get_value_from_nested_dict(converted_values, 'year'))
    month = next(epic_processor.get_value_from_nested_dict(converted_values, 'month'))
    day = next(epic_processor.get_value_from_nested_dict(converted_values, 'day'))
    targeted_close_date = f'{year}-{month}-{day}'
    opportunity.TargetedCloseDate = targeted_close_date

    client_name = epic_processor.get_value_from_nested_dict(converted_values, 'clientName')
    search_criteria = {'ClientName': next(client_name)}
    sdk = epic_processor.get_epic_sdk(account=ams_object_type.AMSType.Account)
    results = sdk.get_object('Client', search_criteria)
    client_id = None
    if results:
        client = xml_utilities.convert_xml_to_dict(results)
        client_id = epic_processor.get_value_from_nested_dict(client, 'ClientID')
    opportunity.ClientID = next(client_id)
    return opportunity
