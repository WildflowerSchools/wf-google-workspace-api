import json

from app import const
from google.oauth2 import service_account
import googleapiclient.discovery as discovery
from googleapiclient import errors

from app.models.members import Member

GSUITE_SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.domain.readonly',
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group'
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


def get_group_key_by_email(group_email):
    results = directory_service().groups().list(
        customer=const.GOOGLE_WORKSPACE_CUSTOMER_ID,
        maxResults=1,
        query="email:{0}*".format(group_email)).execute()
    groups = results.get('groups', [])
    if len(groups) == 0:
        return None

    return groups[0]


def get_group_members_by_key(group_key):
    results = directory_service().members().list(
        groupKey=group_key
    ).execute()
    members = results.get('members', [])
    if len(members) > 0:
        return members
    else:
        return None


def get_group_by_email(group_email):
    group = get_group_key_by_email(group_email)
    if group is None:
        return None

    members = get_group_members_by_key(group_key=group['id'])
    group['members'] = members

    return group


def add_member_to_group(group_email, member_email):
    member = Member(
        email=member_email,
        role='MEMBER'
    )
    results = directory_service().members().insert(
        groupKey=group_email,
        body=member.dict()

    ).execute()

    return results


def remove_member_from_group(group_email, member_email):
    results = directory_service().members().delete(
        groupKey=group_email,
        memberKey=member_email

    ).execute()

    return results
