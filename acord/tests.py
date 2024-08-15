from django.test import TestCase
from .models import *
from datetime import datetime


class TestModel(TestCase):
    def setUp(self):
        address_type = AddressType(
            Type='Mailing',
        )
        address_type.save()
        address = Address(
            Type=address_type,
            Address1='10451 N Pierpont Cir',
            City='Fresno',
            State='CA',
            Zip='93730',
        )
        address.save()
        agency_information = AgencyInformation(
            Name='Dundas Agency, Inc.',
            Address=address,
            ContactName='Rob Dundas',
            ContactPhone='(559) 492-9647',
            ContactEmail='rbdundas@gmail.com'
        )
        agency_information.save()
        carrier_information = CarrierInformation(
            Name='Hartford Insurance Company',
            NAIC='1234'
        )
        carrier_information.save()
        transaction_status = TransactionStatus(
                Status='Quote'
        )
        transaction_status.save()
        lob_business_owners = LinesOfBusiness(
            Name='BUSINESS OWNERS'
        )
        lob_business_owners.save()
        attachment_sov = Attachment(
            Name='STATEMENT / SCHEDULE OF VALUES'
        )
        attachment_sov.save()
        application = Application(
            AgencyInformation=agency_information,
            Date=datetime.now(),
            CarrierInformation=carrier_information,
            PolicyNumber='1234567890',
            Underwriter='John Doe',
            AgencyCustomerID='12345',
            TransactionStatus=transaction_status,
            BindTimestamp=None
        )
        application.save()
        application.LinesOfBusiness.add(lob_business_owners)
        application.Attachments.add(attachment_sov)
        application.save()


    def test_application(self):
        application = Application.objects.get(id=1)
        self.assertEqual(application.AgencyInformation.Name, 'Dundas Agency, Inc.')
