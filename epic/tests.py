from django.test import TestCase
import json

import epic.processor
from core.models import Account
from amsforms.models import AMSType, AMSObjectType, FormDefinition, AMSObjectValue, AMSObjectValueDefault, FormToAMSValueMapping
from core.models import EpicSDKConfiguration
from epic import processor as epic_processor
from amsforms import processor as ams_processor
from amsforms.models import CognitoParameters, JotformParameters


class ClientFormTestCase(TestCase):

    def setUp(self):

        account = Account.objects.create(Name='Test Company')
        sdk_settings = EpicSDKConfiguration.objects.create(
            Account=account,
            Token='crgtjNMl/eiGjEvAQmlpHu2HpnY7CCWHXHD9ltHxlxE=',
            Database='PROFE37_PANO_DEMO',
            Host='de017sdk.appliedonline.net',
            EndpointURL='https://de017sdk.appliedonline.net/EpicSDK/EpicSDK.svc',
            UserCode='RDUNDAS'
        )
        ams_type = AMSType.objects.create(Account=account, AMS='EPIC')
        form_definitions = FormDefinition.objects.create(Account=account, FormTitle='Client Form')
        ams_object_type = AMSObjectType.objects.create(AMSType=ams_type,
                                                       FormDefinition=form_definitions,
                                                       AMSObjectType='Client')
        account_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountName', Required=True)
        first_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactFirst', Required=True)
        last_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactLast', Required=True)
        email = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactEmail', Required=True)
        number = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactNumber', Required=True)
        number_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactNumberType', Required=True)
        client_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ClientType', Required=True)
        street1 = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Street1', Required=True)
        street2 = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Street2', Required=False)
        city = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='City', Required=True)
        state = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='StateOrProvinceCode', Required=True)
        zip = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ZipOrPostalCode', Required=True)
        agency_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AgencyCode', Required=True)
        branch_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='BranchCode', Required=True)
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=agency_code, DefaultValue='PIA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=branch_code, DefaultValue='AFF')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=first_name, FormField='first')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=last_name, FormField='last')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=street1, FormField='addr_line1')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=street2, FormField='addr_line2')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=city, FormField='city')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=state, FormField='state')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=zip, FormField='postal')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=email, FormField='email')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=number, FormField='full')

    def test_client_creations(self):
        raw_request = {'slug': 'submit/241516645642053',
                       'jsExecutionTracker': 'build-date-1717365173338=>init-started:1717365173599=>validator-called:1717365173603=>validator-mounted-true:1717365173603=>init-complete:1717365173605=>interval-complete:1717365194604=>onsubmit-fired:1717365214427=>submit-validation-passed:1717365214434',
                       'submitSource': 'form', 'buildDate': '1717365173338', 'q8_clientType': 'Personal',
                       'q9_companyName': '', 'q5_name': {'first': 'John', 'last': 'Smith'},
                       'q3_email': 'john@example.com',
                       'q7_phoneNumber': {'full': '(559) 492-9647'},
                       'q6_address': {'addr_line1': '111 Pine Street', 'addr_line2': '', 'city': 'San Francisco',
                                      'state': 'CA', 'postal': '94111'}, 'timeToSubmit': '20', 'preview': 'true',
                       'validatedNewRequiredFieldIDs': '{"new":1}', 'path': '/submit/241516645642053'}
        ams_object_type = AMSObjectType.objects.filter(AMSObjectType='Client').first()
        ams_object = epic_processor.convert_form_and_post_to_ams(raw_request, ams_object_type)
        self.assertIsNotNone(ams_object)

    def test_raw_request_conversion(self):
        raw_request = {'slug': 'submit/241516645642053',
                       'jsExecutionTracker': 'build-date-1717365173338=>init-started:1717365173599=>validator-called:1717365173603=>validator-mounted-true:1717365173603=>init-complete:1717365173605=>interval-complete:1717365194604=>onsubmit-fired:1717365214427=>submit-validation-passed:1717365214434',
                       'submitSource': 'form', 'buildDate': '1717365173338', 'q8_clientType': 'Personal',
                       'q9_companyName': '', 'q5_name': {'first': 'John', 'last': 'Smith'},
                       'q3_email': 'john@example.com',
                       'q7_phoneNumber': {'full': '(111) 111-1111'},
                       'q6_address': {'addr_line1': '111 Pine Street', 'addr_line2': '', 'city': 'San Francisco',
                                      'state': 'CA', 'postal': '94111'}, 'timeToSubmit': '20', 'preview': 'true',
                       'validatedNewRequiredFieldIDs': '{"new":1}', 'path': '/submit/241516645642053'}
        converted = epic.processor.convert_form_to_dict(dict_to_process=raw_request)
        self.assertIsNotNone(converted)


class ActivityFormTestCase(TestCase):

    def setUp(self):
        account = Account.objects.create(Name='Test Company')
        sdk_settings = EpicSDKConfiguration.objects.create(
            Account=account,
            Token='crgtjNMl/eiGjEvAQmlpHu2HpnY7CCWHXHD9ltHxlxE=',
            Database='PROFE37_PANO_DEMO',
            Host='de017sdk.appliedonline.net',
            EndpointURL='https://de017sdk.appliedonline.net/EpicSDK/EpicSDK.svc',
            UserCode='RDUNDAS'
        )
        ams_type = AMSType.objects.create(Account=account, AMS='EPIC')
        form_definitions = FormDefinition.objects.create(Account=account, FormTitle='Activity Form')
        ams_object_type = AMSObjectType.objects.create(AMSType=ams_type,
                                                       FormDefinition=form_definitions,
                                                       AMSObjectType='Activity')
        who_owner_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='WhoOwnerCode', Required=True)
        account_type_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountTypeCode', Required=True)
        associated_to_id = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AssociatedToID', Required=True)
        associated_to_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AssociatedToType', Required=True)
        note_text = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='NoteText', Required=True)
        contact_via = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ContactVia', Required=True)
        contact_number_email = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ContactNumberEmail', Required=True)
        contact_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ContactName', Required=True)
        account_id = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountID', Required=True)
        account_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountType', Required=True)
        priority = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Priority', Required=True)
        agency_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AgencyCode', Required=True)
        branch_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='BranchCode', Required=True)
        activity_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ActivityCode', Required=True)

        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=who_owner_code, DefaultValue='DUNRO1')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=account_type_code, DefaultValue='CUST')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=account_id, DefaultValue='123963')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=associated_to_id, DefaultValue='123963')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=associated_to_type, DefaultValue='Account')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=contact_via, DefaultValue='Email')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=account_type, DefaultValue='CUST')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=priority, DefaultValue='Normal')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=agency_code, DefaultValue='PIA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=branch_code, DefaultValue='AFF')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=activity_code, DefaultValue='*POL')

        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=note_text, FormField='first')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=note_text, FormField='last')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=note_text, FormField='email')

    def test_raw_request(self):
        raw_request = {"slug": "submit\/241519130843048",
                       "jsExecutionTracker": "build-date-1718212858678=>init-started:1718212858895=>validator-called:1718212858898=>validator-mounted-true:1718212858898=>init-complete:1718212858899=>onsubmit-fired:1718212860027=>submit-validation-passed:1718212860039",
                       "submitSource": "form", "buildDate": "1718212858678",
                       "q3_name": {"first": "John", "last": "Smith"}, "q4_email": "john@example.com",
                       "timeToSubmit": "1", "preview": "true", "validatedNewRequiredFieldIDs": "{\"new\":1}",
                       "path": "\/submit\/241519130843048"}
        converted = epic.processor.convert_form_to_dict(dict_to_process=raw_request)
        self.assertIsNotNone(converted)

    def test_activity_creation(self):
        raw_request = {"slug": "submit\/241519130843048",
                       "jsExecutionTracker": "build-date-1718212858678=>init-started:1718212858895=>validator-called:1718212858898=>validator-mounted-true:1718212858898=>init-complete:1718212858899=>onsubmit-fired:1718212860027=>submit-validation-passed:1718212860039",
                       "submitSource": "form", "buildDate": "1718212858678",
                       "q3_name": {"first": "John", "last": "Smith"}, "q4_email": "john@example.com",
                       "timeToSubmit": "1", "preview": "true", "validatedNewRequiredFieldIDs": "{\"new\":1}",
                       "path": "\/submit\/241519130843048"}
        ams_object_type = AMSObjectType.objects.filter(AMSObjectType='Activity').first()
        ams_object = epic_processor.convert_form_and_post_to_ams(raw_request, ams_object_type)
        self.assertIsNotNone(ams_object)


class OpportunityFormTestCase(TestCase):

    def setUp(self):
        account = Account.objects.create(Name='Test Company')
        sdk_settings = EpicSDKConfiguration.objects.create(
            Account=account,
            Token='crgtjNMl/eiGjEvAQmlpHu2HpnY7CCWHXHD9ltHxlxE=',
            Database='PROFE37_PANO_DEMO',
            Host='de017sdk.appliedonline.net',
            EndpointURL='https://de017sdk.appliedonline.net/EpicSDK/EpicSDK.svc',
            UserCode='RDUNDAS'
        )
        ams_type = AMSType.objects.create(Account=account, AMS='EPIC')
        form_definitions = FormDefinition.objects.create(Account=account, FormTitle='Opportunity Form')
        ams_object_type = AMSObjectType.objects.create(AMSType=ams_type,
                                                       FormDefinition=form_definitions,
                                                       AMSObjectType='Opportunity')
        agency_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AgencyCode', Required=True)
        branch_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='BranchCode', Required=True)
        group = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='StageGroup', Required=True)
        stage = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Stage', Required=True)
        stage_weight = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='StageWeight', Required=True)
        description = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Description', Required=True)
        premium = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Premium', Required=True)
        comments = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Comments', Required=True)
        targeted_close_date = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='TargetedCloseDate', Required=True)
        owner_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='OwnerType', Required=True)
        owner_lookup_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='OwnerLookupCode', Required=True)

        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=agency_code, DefaultValue='PIA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=branch_code, DefaultValue='AFF')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=group, DefaultValue='Default Group')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=stage, DefaultValue='Qualified')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=stage_weight, DefaultValue='1')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=owner_type, DefaultValue='EM')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=owner_lookup_code, DefaultValue='DUNRO1')

        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=description, FormField='opportunityDescription')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=comments, FormField='clientName')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=premium, FormField='targetPremium')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=targeted_close_date, FormField='month')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=targeted_close_date, FormField='day')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=targeted_close_date, FormField='year')

    def test_cognito_form_body(self):
        raw_request = b'{"Form":{"Id":"3","InternalName":"ClaimForm","Name":"Claim Form"},"$version":8,"$etag":"W/\\"datetime\'2024-06-17T02%3A05%3A33.3165757Z\'\\"","PolicyholderInformation":{"FullName":{"First":"Robert","FirstAndLast":"Robert Dundas","Last":"Dundas","Middle":null,"MiddleInitial":null,"Prefix":null,"Suffix":null},"Email":"rbdundas@gmail.com","PhoneNumber":"(559) 492-9647","Address":{"City":"Fresno","CityStatePostalCode":"Fresno, CA 93730","Country":null,"CountryCode":null,"FullAddress":"10451 N Pierpont Cir, Fresno, CA 93730","FullInternationalAddress":"10451 N Pierpont Cir, Fresno, CA 93730","Latitude":null,"Line1":"10451 N Pierpont Cir","Line2":null,"Line3":null,"Longitude":null,"PostalCode":"93730","State":"CA","StreetAddress":"10451 N Pierpont Cir","Type":"Home"},"PolicyNumber":"ABC123"},"DetailsOfLossOrDamage":{"DateOfLossOrDamage":"2024-06-14","NatureOfLossOrDamage":"Water Damage","EstimatedCostOfRepairOrReplacement":10123.0,"WitnessInformation":[{"Id":"2rry3C","FullName1":{"First":"Megan","FirstAndLast":"Megan Dundas","Last":"Dundas","Middle":null,"MiddleInitial":null,"Prefix":null,"Suffix":null},"PhoneNumber1":"5592607373","Email1":"megandundas12@gmail.com","ItemNumber":1}],"PoliceReport":[],"EstimatedCostOfRepairOrReplacement_IncrementBy":1.0},"Entry":{"AdminLink":"https://www.cognitoforms.com/EpOptiInc/3/entries/1","DateCreated":"2024-06-17T02:05:33.252Z","DateSubmitted":"2024-06-17T02:05:33.252Z","DateUpdated":"2024-06-17T02:05:33.252Z","IsBeta":false,"LastPageViewed":null,"Number":1,"Order":null,"Origin":{"City":null,"CountryCode":null,"IpAddress":"76.125.63.83","IsImported":false,"Region":null,"Timezone":null,"UserAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"},"Timestamp":"2024-06-17T02:05:33.252Z","User":{"Email":"rob@epopti.com","Name":"Robert Dundas"},"Version":1,"Action":"Submit","Role":"Public","Status":"Submitted","PublicLink":"https://www.cognitoforms.com/EpOptiInc/ClaimForm#tgQOaTcoEWR_pbAbJAYJPmI75u9SCvzkoqbzz3EECOc$*","InternalLink":"https://www.cognitoforms.com/EpOptiInc/ClaimForm#9gAEpjZCl-XtAHoE_DXo33WjrG4_xqhjQRJlKcu2FAU$*","Document1":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=2g23PTmPSEJVWyvwz4wniOy2MqScEf-DainJL9USMys$","Document2":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=CuRRPURhPcGswV_1Fix4zYsP_aqkZN1VWvo5or4xVSk$"},"Id":"3-1"}'

        converted = epic.processor.convert_form_to_dict(dict_to_process=raw_request)
        self.assertIsNotNone(converted)

    def test_activity_creation(self):
        raw_request = {'slug': 'submit/241556824145054',
                       'jsExecutionTracker': 'build-date-1718242247770=>init-started:1718242248034=>validator-called:1718242248040=>validator-mounted-true:1718242248040=>init-complete:1718242248041=>interval-complete:1718242269041=>onsubmit-fired:1718242285119=>submit-validation-passed:1718242285126',
                       'submitSource': 'form', 'buildDate': '1718242247770',
                       'q11_clientName': 'Roberto Dundidiliocious',
                       'q12_opportunityDescription': 'This is the description', 'q13_targetPremium': '1234.00',
                       'q14_targetDate': {'month': '06', 'day': '12', 'year': '2024'},
                       'formOpenId_V5': '11635797613517714275', 'timeToSubmit': '20', 'preview': 'true',
                       'validatedNewRequiredFieldIDs': '{"new":1}', 'path': '/submit/241556824145054'}
        ams_object_type = AMSObjectType.objects.filter(AMSObjectType='Opportunity').first()
        ams_object = epic_processor.convert_form_and_post_to_ams(raw_request, ams_object_type)
        self.assertIsNotNone(ams_object)


class CognitoClientFormTestCase(TestCase):

    def setUp(self):
        account = Account.objects.create(Name='Test Company')
        sdk_settings = EpicSDKConfiguration.objects.create(
            Account=account,
            Token='crgtjNMl/eiGjEvAQmlpHu2HpnY7CCWHXHD9ltHxlxE=',
            Database='PROFE37_PANO_DEMO',
            Host='de017sdk.appliedonline.net',
            EndpointURL='https://de017sdk.appliedonline.net/EpicSDK/EpicSDK.svc',
            UserCode='RDUNDAS'
        )
        ams_type = AMSType.objects.create(Account=account, AMS='EPIC')
        form_definitions = FormDefinition.objects.create(Account=account, FormTitle='Client Form')
        CognitoParameters.objects.create(FormID=4, InternalName='InsuranceClientInformationForm', Name='Insurance Client Information Form', FormDefinition=form_definitions)
        ams_object_type = AMSObjectType.objects.create(AMSType=ams_type, FormDefinition=form_definitions, AMSObjectType='Client')
        account_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountName', Required=True)
        first_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactFirst', Required=True)
        last_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactLast', Required=True)
        email = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactEmail', Required=True)
        number = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactNumber', Required=True)
        number_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PrimaryContactNumberType', Required=True)
        client_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ClientType', Required=True)
        street1 = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Street1', Required=True)
        street2 = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Street2', Required=False)
        city = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='City', Required=True)
        state = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='StateOrProvinceCode', Required=True)
        zip = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ZipOrPostalCode', Required=True)
        agency_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AgencyCode', Required=True)
        branch_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='BranchCode', Required=True)

        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=agency_code, DefaultValue='PIA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=branch_code, DefaultValue='AFF')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=first_name, FormField='first')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=last_name, FormField='last')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=street1, FormField='line1')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=street2, FormField='line2')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=city, FormField='city')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=state, FormField='state')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=zip, FormField='postalcode')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=email, FormField='emailaddress')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=number, FormField='phonenumber')

    def test_form_elements(self):
        form_post = b'{"Form":{"Id":"4","InternalName":"InsuranceClientInformationForm","Name":"Insurance Client Information Form"},"$version":8,"$etag":"W/\\"datetime\'2024-06-17T02%3A37%3A58.9588525Z\'\\"","PersonalInformation":{"FullName":{"First":"Robert","FirstAndLast":"Robert Dundas","Last":"Dundas","Middle":null,"MiddleInitial":null,"Prefix":null,"Suffix":null},"EmailAddress":"rbdundas@gmail.com","PhoneNumber":"(559) 492-9647","Address":{"City":"Fresno","CityStatePostalCode":"Fresno, CA 93730","Country":null,"CountryCode":null,"FullAddress":"10451 N Pierpont Cir, Fresno, CA 93730","FullInternationalAddress":"10451 N Pierpont Cir, Fresno, CA 93730","Latitude":null,"Line1":"10451 N Pierpont Cir","Line2":null,"Line3":null,"Longitude":null,"PostalCode":"93730","State":"CA","StreetAddress":"10451 N Pierpont Cir","Type":"Home"},"ClientType":"Personal"},"Entry":{"AdminLink":"https://www.cognitoforms.com/EpOptiInc/4/entries/2","DateCreated":"2024-06-17T02:37:58.897Z","DateSubmitted":"2024-06-17T02:37:58.897Z","DateUpdated":"2024-06-17T02:37:58.897Z","IsBeta":false,"LastPageViewed":null,"Number":2,"Order":null,"Origin":{"City":null,"CountryCode":null,"IpAddress":"76.125.63.83","IsImported":false,"Region":null,"Timezone":null,"UserAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"},"Timestamp":"2024-06-17T02:37:58.897Z","User":{"Email":"rob@epopti.com","Name":"Robert Dundas"},"Version":1,"Action":"Submit","Role":"Public","Status":"Submitted","PublicLink":"https://www.cognitoforms.com/EpOptiInc/InsuranceClientInformationForm#aMB-6Zo2SFwSqKN8VZCgt89m-7I2UzHUhjmtb7fIkQQ$*","InternalLink":"https://www.cognitoforms.com/EpOptiInc/InsuranceClientInformationForm#r0A2jWtuWogdbUpa_a7s8mvueoMUURQJVpkRj3OAsNk$*","Document1":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=UanNy6rP2RL-bXTVUNQRRKl_5c0wG8ikUSHjIKhxEBs$","Document2":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=C8Fdc8sXfG-gy8HBuPS7Oa0ZJ1AftB12kgCgOCKaf3o$"},"Id":"4-2"}'
        raw_request = json.loads(form_post)
        converted = epic.processor.convert_form_to_dict(dict_to_process=raw_request)
        print(converted)
        self.assertIsNotNone(converted)

    def test_client_creations(self):
        form_post = b'{"Form":{"Id":"4","InternalName":"InsuranceClientInformationForm","Name":"Insurance Client Information Form"},"$version":8,"$etag":"W/\\"datetime\'2024-06-17T02%3A37%3A58.9588525Z\'\\"","PersonalInformation":{"FullName":{"First":"Robert","FirstAndLast":"Robert Dundas","Last":"Dundas","Middle":null,"MiddleInitial":null,"Prefix":null,"Suffix":null},"EmailAddress":"rbdundas@gmail.com","PhoneNumber":"(559) 492-9647","Address":{"City":"Fresno","CityStatePostalCode":"Fresno, CA 93730","Country":null,"CountryCode":null,"FullAddress":"10451 N Pierpont Cir, Fresno, CA 93730","FullInternationalAddress":"10451 N Pierpont Cir, Fresno, CA 93730","Latitude":null,"Line1":"10451 N Pierpont Cir","Line2":null,"Line3":null,"Longitude":null,"PostalCode":"93730","State":"CA","StreetAddress":"10451 N Pierpont Cir","Type":"Home"},"ClientType":"Personal"},"Entry":{"AdminLink":"https://www.cognitoforms.com/EpOptiInc/4/entries/2","DateCreated":"2024-06-17T02:37:58.897Z","DateSubmitted":"2024-06-17T02:37:58.897Z","DateUpdated":"2024-06-17T02:37:58.897Z","IsBeta":false,"LastPageViewed":null,"Number":2,"Order":null,"Origin":{"City":null,"CountryCode":null,"IpAddress":"76.125.63.83","IsImported":false,"Region":null,"Timezone":null,"UserAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"},"Timestamp":"2024-06-17T02:37:58.897Z","User":{"Email":"rob@epopti.com","Name":"Robert Dundas"},"Version":1,"Action":"Submit","Role":"Public","Status":"Submitted","PublicLink":"https://www.cognitoforms.com/EpOptiInc/InsuranceClientInformationForm#aMB-6Zo2SFwSqKN8VZCgt89m-7I2UzHUhjmtb7fIkQQ$*","InternalLink":"https://www.cognitoforms.com/EpOptiInc/InsuranceClientInformationForm#r0A2jWtuWogdbUpa_a7s8mvueoMUURQJVpkRj3OAsNk$*","Document1":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=UanNy6rP2RL-bXTVUNQRRKl_5c0wG8ikUSHjIKhxEBs$","Document2":"https://www.cognitoforms.com/d/1suRQqPv6Uqq23MjPkVwIg?code=C8Fdc8sXfG-gy8HBuPS7Oa0ZJ1AftB12kgCgOCKaf3o$"},"Id":"4-2"}'
        raw_request = json.loads(form_post)
        form_id = raw_request['Form']['Id']
        internal_name = raw_request['Form']['InternalName']
        name = raw_request['Form']['Name']
        cognito_parameters = CognitoParameters.objects.filter(FormID=form_id, InternalName=internal_name, Name=name).first()
        ams_object = ams_processor.convert_form_to_ams_object(raw_request['PersonalInformation'], form_definition=cognito_parameters.FormDefinition)
        self.assertIsNotNone(ams_object)

class JotformPolicyFormTestCase(TestCase):

    def setUp(self):
        account = Account.objects.create(Name='Test Company')
        sdk_settings = EpicSDKConfiguration.objects.create(
            Account=account,
            Token='crgtjNMl/eiGjEvAQmlpHu2HpnY7CCWHXHD9ltHxlxE=',
            Database='PROFE37_PANO_DEMO',
            Host='de017sdk.appliedonline.net',
            EndpointURL='https://de017sdk.appliedonline.net/EpicSDK/EpicSDK.svc',
            UserCode='RDUNDAS'
        )
        ams_type = AMSType.objects.create(Account=account, AMS='EPIC')
        form_definitions = FormDefinition.objects.create(Account=account, FormTitle='Policy Form')
        form_id = '241815952338058'
        JotformParameters.objects.create(FormDefinition=form_definitions, FormID=form_id)
        ams_object_type = AMSObjectType.objects.create(AMSType=ams_type, FormDefinition=form_definitions, AMSObjectType='Policy')
        account_id = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountID', Required=True)
        agency_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AgencyCode', Required=True)
        branch_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='BranchCode', Required=True)
        department_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='DepartmentCode', Required=True)
        profit_center_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ProfitCenterCode', Required=True)
        issuing_location_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='IssuingLocationCode', Required=True)
        description = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='Description', Required=True)
        effective_date = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='EffectiveDate', Required=True)
        expiration_date = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='ExpirationDate', Required=True)
        estimated_premium = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='EstimatedPremium', Required=True)
        policy_type_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PolicyTypeCode', Required=True)
        line_type_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='LineTypeCode', Required=True)
        policy_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PolicyType', Required=True)
        policy_number = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='PolicyNumber', Required=True)
        status_code = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='StatusCode', Required=True)
        account_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='AccountName', Required=True)
        customer_type = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='CustomerType', Required=True)
        first_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='FirstName', Required=True)
        last_name = AMSObjectValue.objects.create(AMSObjectType=ams_object_type, AMSField='LastName', Required=True)

        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=agency_code, DefaultValue='PIA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=branch_code, DefaultValue='AFF')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=department_code, DefaultValue='CL')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=profit_center_code, DefaultValue='STA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=issuing_location_code, DefaultValue='CA')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=status_code, DefaultValue='NEW')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=policy_number, DefaultValue='TBD')
        AMSObjectValueDefault.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=description, DefaultValue='Quote request from JotForm')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=account_name, FormField='nameof')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=first_name, FormField='first')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=last_name, FormField='last')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=customer_type, FormField='customertype')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=effective_date, FormField='effectivedate')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=expiration_date, FormField='expirationdate')
        FormToAMSValueMapping.objects.create(AMSObjectType=ams_object_type, AMSObjectValue=policy_type, FormField='lineof')

    def test_policy_form(self):
        form_post = {"slug":"submit\/241815952338058","jsExecutionTracker":"build-date-1719780216701=>init-started:1719780423800=>validator-called:1719780423813=>validator-mounted-true:1719780423813=>init-complete:1719780423814=>onsubmit-fired:1719780437447=>submit-validation-passed:1719780437452","submitSource":"form","buildDate":"1719780216701","q8_customerType":"Commercial","q10_clientFull":{"first":"","last":""},"q11_nameOf":"Rob\'s Dog Sitting","q9_existingCustomer":"Yes","q7_lineOf":"Business Owners Policy","q4_effectiveDate":{"month":"06","day":"30","year":"2024"},"q5_expirationDate":{"month":"06","day":"30","year":"2025"},"timeToSubmit":"13","preview":"true","validatedNewRequiredFieldIDs":"{\"new\":1}","path":"\/submit\/241815952338058"}
        converted = epic.processor.convert_form_to_dict(dict_to_process=form_post)
        print(converted)
        self.assertIsNotNone(converted)

    def test_post_policy_form(self):
        raw_request = {"slug":"submit\/241815952338058","jsExecutionTracker":"build-date-1719780216701=>init-started:1719780423800=>validator-called:1719780423813=>validator-mounted-true:1719780423813=>init-complete:1719780423814=>onsubmit-fired:1719780437447=>submit-validation-passed:1719780437452","submitSource":"form","buildDate":"1719780216701","q8_customerType":"Commercial","q10_clientFull":{"first":"","last":""},"q11_nameOf":"Rob\'s Dog Sitting","q9_existingCustomer":"Yes","q7_lineOf":"Business Owners Policy","q4_effectiveDate":{"month":"06","day":"30","year":"2024"},"q5_expirationDate":{"month":"06","day":"30","year":"2025"},"timeToSubmit":"13","preview":"true","validatedNewRequiredFieldIDs":"{\"new\":1}","path":"\/submit\/241815952338058"}
        form_id = '241815952338058'
        jotform_parameters = JotformParameters.objects.filter(FormID=form_id).first()
        ams_object_type = AMSObjectType.objects.filter(AMSObjectType='Policy').first()
        ams_object = epic_processor.convert_form_and_post_to_ams(raw_request, ams_object_type)
        self.assertIsNotNone(ams_object)
