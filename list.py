#!/usr/bin/env python3
import openai
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# https://platform.openai.com/account/api-keys
with open(f"{dir_path}/api_key.txt") as f:
  openai.api_key = f.read().strip()
with open(f"{dir_path}/api_organization.txt") as f:
  openai.organization = f.read().strip()

print(openai.Model.list())
