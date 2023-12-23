#!/usr/bin/env python3
from openai import OpenAI
import sys
import os

client = None

def load_secrets():
    global client
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # https://platform.openai.com/account/api-keys
    # Do not check in secrets, put these in .gitignore
    with open(f'{dir_path}/api_key.txt') as f:
        key = f.read().strip()
    with open(f'{dir_path}/api_organization.txt') as f:
        org = f.read().strip()
        client = OpenAI(api_key = key, organization = org)

load_secrets()
print(client.models.list())

