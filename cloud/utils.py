import os
from google.cloud import billing_v1 as billing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_APPLICATION_CREDENTIALS = f'{BASE_DIR}/cloud/gcloud_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS


def get_billing_client():
    billing_client = billing.CloudBillingClient()
    return billing_client


get_billing_client()
