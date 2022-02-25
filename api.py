import json

import const
from google.oauth2 import service_account
import googleapiclient.discovery as discovery


GSUITE_SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.domain.readonly',
    'https://www.googleapis.com/auth/admin.directory.user'
]


def gsuite_credentials():
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(const.GOOGLE_WORKSPACE_SERVICE_ACCOUNT_CREDENTIALS),
        scopes=GSUITE_SCOPES,
        subject=const.GOOGLE_WORKSPACE_SERVICE_ACCOUNT_DELEGATED_USER)
    return credentials


def directory_service():
    credentials = gsuite_credentials()
    return discovery.build('admin', 'directory_v1', credentials=credentials)


def get_user_by_email(email):
    results = directory_service().users().list(
        customer=const.GOOGLE_WORKSPACE_CUSTOMER_ID,
        projection='full',
        maxResults=1,
        query="email:{0}".format(email)).execute()
    users = results.get('users', [])
    if len(users) > 0:
        return users[0]
    else:
        return None
