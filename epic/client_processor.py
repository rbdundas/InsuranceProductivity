from amsforms.models import AMSObjectType, AMSObjectValueDefault
from epic_sdk_scripts_rbdundas.models.Client import Client
from epic import processor as epic_processor


def create_ams_object(client: Client, converted_values: dict, ams_object_type: AMSObjectType) -> Client:

    ams_value_defaults = AMSObjectValueDefault.objects.filter(AMSObjectType=ams_object_type).all()
    default_agency = ams_value_defaults.filter(AMSObjectValue__AMSField='AgencyCode').first()
    default_branch = ams_value_defaults.filter(AMSObjectValue__AMSField='BranchCode').first()
    structure_item = client.AccountValue.AgencyStructureItem()
    structure_item.AgencyCode = default_agency.DefaultValue
    structure_item.BranchCode = default_branch.DefaultValue
    client.AccountValue.Structure = [structure_item]

    client_type = next(epic_processor.get_value_from_nested_dict(converted_values, 'clienttype'))

    if client_type == 'Personal':
        client.IsPersonal = 'true'
        client.FormatOption.OptionName = 'Individual'
        client.FormatOption.Value = '0'
        client.AccountName = client.PrimaryContactFirst + ' ' + client.PrimaryContactLast
    elif client_type == 'Commercial':
        client.IsCommercial = 'true'
        client.AccountName = client.AccountName.strip().upper()[:100]
        client.BusinessName = client.AccountName.strip().upper()[:100]
        client.FormatOption.OptionName = 'Business'
        client.FormatOption.Value = '1'

    client.AccountValue.AccountEmail = client.PrimaryContactEmail
    client.AccountValue.Number = client.PrimaryContactNumber
    client.AccountValue.NumberType = client.PrimaryContactNumberType

    return client
