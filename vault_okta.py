#!/usr/bin/env python3
import argparse
import os
import hvac


def get_users(credentials):
    users = []
    client = hvac.Client()
    client = hvac.Client(url=credentials.vaultUrl)
    if credentials.vaultToken is not None:
        client.token = credentials.vaultToken
        client.is_authenticated()
    else:
        print("Credentials are incorrect")
        os.exit(1)
    users = client.auth.okta.list_users()['data']['keys']
    for user in users:
        read_user = client.auth.okta.read_user(username=user)
        print("\n")
        print(user)
        print(*read_user['data']['policies'])
    return users

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--vault-url",
                    dest="vaultUrl", help="Vault URL")
parser.add_argument("-t", "--vault-token",
                    dest="vaultToken", help="Vault token")

credentials = parser.parse_args()

get_users(credentials)
