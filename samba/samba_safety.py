import os
import requests
import json
import urllib.parse
import time
from .models import SambaSettings
from lxml import etree
from datetime import datetime
import base64
from epic_sdk_scripts_rbdundas import epic_sdk, xml_utilities
import concurrent.futures
from core.models import EpicSDKConfiguration, Account
from billing import utils as billing_utils


def get_epic_sdk(account):
    sdk_settings = EpicSDKConfiguration.objects.get(Account=account)
    sdk = epic_sdk.EpicSDK(
        endpoint_url=sdk_settings.EndpointURL,
        host=sdk_settings.Host,
        database=sdk_settings.Database,
        user_code=sdk_settings.UserCode,
        password=sdk_settings.Token
    )
    return sdk


sdk = get_epic_sdk(1)


def get_token_from_samba(account):
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=settings.URL + '/oauth2/v1/token',
        headers={
            'x-api-key': settings.APIKey,
            'Content-Type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
            'Authorization': f'Basic MG9hMTgzOXdsbGpCU09GUlczNTg6Rk1tRk12cG9nR3pMYU9VaXdXV0xqVW1WQl9lOHNnNHFFUUUwMy1JdlZ0MG8wZmRIVm9Mekg3WEtBczExR1lvcA=='
        },
        method='POST',
        data=urllib.parse.urlencode({
            'grant_type': 'client_credentials',
            'scope': 'API'
        })
    )
    token = req.json()['access_token']
    print(token)
    return token


account = Account.objects.get(id=1)
token = get_token_from_samba(account)


def place_order(account, search_critera: dict):
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=f'{settings.URL}/transactional/v1/mvrorders',
        headers={
            'x-api-key': settings.APIKey,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        method='POST',
        data=json.dumps(search_critera)
    )
    print(req.status_code)
    return req.json()


def get_order_status(account, order_id: str):
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=f'{settings.URL}/transactional/v1/mvrorders/{order_id}',
        headers={
            'x-api-key': settings.APIKey,
            'Content-Type': 'application/vnd.sambasafety.qorta.mvr+json;version=3.0.0',
            'Authorization': f'Bearer {token}'
        },
        method='GET'
    )
    return json.loads(req.content)


def get_all_order_status(account, start_date: datetime.date, end_date: datetime.date) -> dict:
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=settings.URL + f'/orders/v1/licensereports/verifydriver?page=1&size=50&startOrderDate={start_date.strftime("%Y-%m-%d")}&endOrderDate={end_date.strftime("%Y-%m-%d")}',
        headers={
            'x-api-key': settings.APIKey,
            'Content-Type': 'text/json',
            'Authorization': f'Bearer {token}'
        },
        method='GET'
    )
    print(req.json())
    return req.json()


def get_report(account, report_id: str) -> bytes:
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=f'{settings.URL}/reports/v1/motorvehiclereports/{report_id}',
        headers={
            'x-api-key': settings.APIKey,
            'Accept': 'application/vnd.sambasafety.qorta.mvr+json;version=3.0.0',
            'Authorization': f'Bearer {token}'
        },
        method='GET'
    )
    return json.loads(req.content)


def get_report_pdf(account, report_id: str) -> bytes:
    settings = SambaSettings.objects.filter(Account=account).first()
    req = requests.request(
        url=f'{settings.URL}/reports/v1/motorvehiclereports/{report_id}',
        headers={
            'x-api-key': settings.APIKey,
            'Accept': 'application/vnd.sambasafety.qorta.mvr+pdf',
            'Authorization': f'Bearer {token}'
        },
        method='GET'
    )
    return req.content


def samba_to_epic(driver: dict):
    account = Account.objects.get(id=driver['AccountID'])
    sdk = get_epic_sdk(account)

    billing_utils.create_billing_event(account, 'Samba', description='Place Order')
    order = place_order(account, driver)
    order_id = order['orderId']

    billing_utils.create_billing_event(account, 'Samba', description='Check Order Status')
    order = get_order_status(account, order_id)
    order_status = order['orderStatus']
    print(order_status)
    while order_status.lower() != 'fulfilled':
        time.sleep(1)
        billing_utils.create_billing_event(account, 'Samba', description='Check Order Status')
        order = get_order_status(account, order_id)
        print(order_status)
        order_status = order['orderStatus']
        continue
    report_id = order['links'][0]['id']
    billing_utils.create_billing_event(account, 'Samba', description='Get Report PDF')
    report = get_report_pdf(account, report_id)
    pdf_bytes = base64.b64decode(report)
    file_name = f'{driver['firstName']}_{driver["lastName"]}.pdf'
    with open(f'{file_name}', 'wb') as f:
        f.write(pdf_bytes)
    billing_utils.create_billing_event(account, 'Epic SDK', description='Upload Attachment')
    ticket = sdk.upload_attachment(file_name)

    file_name = file_name
    ticket = ticket
    agency_code = 'PIA'
    branch_code = 'AFF'
    attach_to_id = driver['PolicyID']
    attach_to_type = 'Policy'
    flag = 'Insert'
    folder = 'ARC Accessible'

    file_stats = os.stat(file_name)
    file_detail_item = {
        'AttachmentObject': {
            'AccountID': driver['ClientID'],
            'AccountTypeCode': 'CUST',
            'AgencyStructures': [
                {'AgencyStructureItem': {'AgencyCode': agency_code, 'BranchCode': branch_code}},
            ],
            'AttachedTos': [{
                'AttachedToItem': {
                    'AttachedToID': attach_to_id,
                    'AttachedToType': attach_to_type,
                    'Flag': flag
                }
            }],
            'Description': 'MVR',
            'Files': [{
                'FileDetailItem': {
                    'Extension': file_name.split('.')[1],
                    'FileName': file_name,
                    'Length': file_stats.st_size,
                    'TicketName': ticket,
                }
            }],
            'Folder': folder,
            'ClientAccessible': 'true'
        },
    }
    billing_utils.create_billing_event(account, 'Epic SDK', description='Associate Attachment')
    attachment = sdk.insert_object('attachment', file_detail_item)
    return attachment


def epic_to_samba(account, data: dict) -> bool:
    sdk = get_epic_sdk(account)
    billing_utils.create_billing_event(account, 'Epic SDK', description='Get Line')
    line = sdk.get_object('Line', search_criteria={'PolicyID': data['PolicyID']})
    line_xml = etree.fromstring(line)
    _line = xml_utilities.xml_to_dict(line_xml, 'Line')
    line_id = _line[0]['Line']['LineID']

    billing_utils.create_billing_event(account, 'Epic SDK', description='Get Business Auto Drivers')
    line = sdk.get_object('businessauto_driver', search_criteria={'ID': str(line_id), 'IDType': 'LineID'})
    print(line)
    line_xml = etree.fromstring(line)
    _drivers = xml_utilities.xml_to_dict(line_xml, 'Driver')
    drivers = []
    for _driver in _drivers:
        driver = {
            'ClientID': data['ClientID'],
            'PolicyID': data['PolicyID'],
            'purpose': 'INSURANCE',
            'firstName': _driver['Driver']['Name'].split(' ')[0],
            'lastName': _driver['Driver']['Name'].split(' ')[1],
            'licenseNumber': _driver['Driver']['DriverLicenseNumber'],
            'licenseState': _driver['Driver']['StateLicensed'],
            'birthDate': _driver['Driver']['DateOfBirth'],
            "productId": "DL",
            "subType": "STANDARD",
            "host": "ONLINE",
            'AccountID': account.id
        }
        drivers.append(driver)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(samba_to_epic, drivers)
    return True


