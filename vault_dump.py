#!/usr/bin/env python3
import argparse
import os
import hvac


def dump_secrets(credentials):
    client = hvac.Client()
    client = hvac.Client(url=credentials.vaultUrl)
    if credentials.vaultToken is not None:
        client.token = credentials.vaultToken
        client.is_authenticated()
    elif credentials.roleId is not None and credentials.secretId is not None:
        client.auth.approle.login(
            role_id=credentials.roleId,
            secret_id=credentials.secretId,
        )
    else:
        print("Credentials are incorrect")
        os.exit(1)
    if credentials.secretList == "":
        print("secret list is empty")
        os.exit(1)
    else:
        secrets = credentials.secretList.split(",")
    f = open("./secrets.env", "a")
    for secret in secrets:
        res_l = client.secrets.kv.v1.list_secrets(mount_point='/', path=secret)
        for s in res_l['data']['keys']:
            # skip nested
            if '/' not in s:
                response = client.secrets.kv.v1.read_secret(
                    mount_point=secret, path=s)
                for k, v in response['data'].items():
                    f.write(k.upper() + '=' + v + '\n')
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--vault-token",
                    dest="vaultToken", help="Vault token")
parser.add_argument("-u", "--vault-url",
                    dest="vaultUrl", help="Vault URL")
parser.add_argument("-r", "--role-id",
                    dest="roleId", help="Vault approle id")
parser.add_argument("-s", "--secret-id",
                    dest="secretId", help="Vault approle secret id")
parser.add_argument("-l", "--secret-list",
                    dest="secretList", help="Comma-separated list of secrets")

credentials = parser.parse_args()

dump_secrets(credentials)
