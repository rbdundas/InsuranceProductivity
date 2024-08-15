from datetime import datetime
from epic_sdk_scripts_rbdundas.models.Policy import Policy
from epic_sdk_scripts_rbdundas import xml_utilities, epic_sdk

import epic.processor
from amsforms.models import AMSObjectType, AMSObjectValueDefault, FormToAMSValueMapping
from amsforms import processor
from epic import processor as epic_processor


def set_policy_defaults(policy: Policy):
    return policy


# Change these to Lookups
def get_policy_type_code(policy_type: str) -> str:
    if policy_type == 'Business Owners Policy':
        return 'BOP'


def get_line_type_code(policy_type_code: str) -> str:
    if policy_type_code == 'BOP':
        return 'PROP'


def create_ams_object(ams_object: Policy, converted_values: dict, ams_object_type: AMSObjectType):
    policy = ams_object
    mappings = FormToAMSValueMapping.objects.filter(AMSObjectType=ams_object_type).all()
    ams_value_defaults = AMSObjectValueDefault.objects.filter(AMSObjectType__AMSObjectType='Policy').all()

    # policy.PremiumPayableTypeCode = converted_values['PremiumPayableTypeCode']
    # if policy.PremiumPayableTypeCode == 'CA':
    #     policy.IssuingCompanyLookupCode = 'TBDCO1'
    #     policy.PremiumPayableLookupCode = converted_values['BillingCompany']
    # else:
    #     policy.IssuingCompanyLookupCode = converted_values['IssuingCompany']
    #     policy.PremiumPayableLookupCode = converted_values['WholesaleBroker']

    agency_code = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='AgencyCode').first()
    branch_code = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='BranchCode').first()
    department_code = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='DepartmentCode').first()
    profit_center = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='ProfitCenterCode').first()
    description = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='Description').first()
    status_code = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='StatusCode').first()
    policy_number = ams_value_defaults.filter(AMSObjectType__AMSObjectType='Policy', AMSObjectValue__AMSField='PolicyNumber').first()

    policy.AgencyCode = agency_code.DefaultValue
    policy.BranchCode = branch_code.DefaultValue
    policy.DepartmentCode = department_code.DefaultValue
    policy.ProfitCenterCode = profit_center.DefaultValue
    policy.Description = description.DefaultValue
    policy.StatusCode = status_code.DefaultValue
    policy.PolicyNumber = policy_number.DefaultValue

    policy_type = mappings.filter(AMSObjectValue__AMSField='PolicyType').first()
    account_name = mappings.filter(AMSObjectValue__AMSField='AccountName').first()

    effective_date_field = mappings.filter(AMSObjectValue__AMSField='EffectiveDate').first()
    expiration_date_field = mappings.filter(AMSObjectValue__AMSField='EffectiveDate').first()

    effective_date_value = next(epic_processor.get_value_from_nested_dict(converted_values, effective_date_field.FormField))
    expiration_date_value = next(epic_processor.get_value_from_nested_dict(converted_values, expiration_date_field.FormField))

    effective_date = f'{effective_date_value['year']}-{effective_date_value['month']}-{effective_date_value['day']}'
    expiration_date = f'{expiration_date_value['year']}-{expiration_date_value['month']}-{expiration_date_value['day']}'

    policy.EffectiveDate = effective_date
    policy.ExpirationDate = expiration_date

    policy_type = next(epic_processor.get_value_from_nested_dict(converted_values, policy_type.FormField))
    policy_type_code = get_policy_type_code(policy_type)
    policy.PolicyTypeCode = policy_type_code
    policy.LineTypeCode = policy_type_code

    client_name = next(epic_processor.get_value_from_nested_dict(converted_values, account_name.FormField))
    search_criteria = {'ClientID': str(202121)}
    sdk = epic_processor.get_epic_sdk(account=ams_object_type.AMSType.Account)
    results = sdk.get_object('Client', search_criteria)
    if results:
        client_result = xml_utilities.convert_xml_to_dict(results)
        clients = client_result['Envelope']['Body']['Get_ClientResponse']['Get_ClientResult']['Clients']
        if isinstance(clients, dict):
            client = clients['Client']
        elif isinstance(clients, list):
            client = clients[0]
        else:
            client = None
        client_id = next(epic_processor.get_value_from_nested_dict(client, 'ClientID'))
        policy.AccountID = client_id
        policy.IssuingLocationCode = client['AccountValue']['Address']['StateOrProvinceCode']

    policy = set_policy_defaults(policy)
    return policy

