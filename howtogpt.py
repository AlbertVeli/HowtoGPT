#!/usr/bin/env python3
#
# ChatGPT script based on https://gynvael.coldwind.pl/?lang=en&id=771
# which in turn is based on the openai examples:
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

import sys
import getopt
from pathlib import Path
try:
    from openai import OpenAI
except ImportError:
    sys.exit('Please install openai with "apt install python3-openai" or pip')
try:
    from dotenv import dotenv_values
except ImportError:
    sys.exit('Please install python-dotenv with "apt install python3-dotenv" or pip')

def load_client():
    env_path = Path(__file__).parent / '.env'
    try:
        config = dotenv_values(env_path)
    except Exception:
        sys.exit('Please create a .env file with your OpenAI API key and organization')
    if 'OPENAI_API_KEY' not in config or 'OPENAI_ORGANIZATION' not in config:
        sys.exit('Missing OPENAI_API_KEY or OPENAI_ORGANIZATION in .env')
    return OpenAI(api_key=config['OPENAI_API_KEY'], organization=config['OPENAI_ORGANIZATION'])

def do_question(client, s, mode):
    system = 'You are a CLI assistant. Provide only the command, no explanations or extra text.'
    prompt = '' if mode == 'raw' else f'Provide the {mode} command-line command to '

    ret = client.chat.completions.create(
        model='gpt-5.2',
        messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt + s}])
    text = ret.choices[0].message.content.strip()
    if text.startswith('``'):
        # Remove opening ```bash or similar fence; command is on the next line
        lines = text.split('\n')
        if len(lines) > 1:
            text = lines[1]
    if len(text) > 2 and text[0] in '`"\'':
        text = text[1:-1]
    return text

def print_help():
    print(f"""\
Usage: {sys.argv[0]} [-h] [-r] [-m <system>] <question>

  Use -m raw (or -r) for a raw question or
  the name of any system for a cmdline.
  Default value is "Ubuntu".

  EXAMPLES

  $ {sys.argv[0]} reverse lines in one file
  tac <filename>

  $ {sys.argv[0]} -m powershell reverse lines in one file
  Get-Content -Path "file.txt" | Select-Object -Reverse | Set-Content -Path "reversed.txt"

  $ {sys.argv[0]} -r describe the gecos field in a unix password file
  The GECOS field in a Unix password file contains general information about a user. It
  typically includes the user's full name, contact information, office location, and
  other optional details. This field is primarily used for administrative purposes and
  may vary depending on the Unix system in use.""")
    sys.exit(1)

def parse_opts():
    mode = 'ubuntu'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hrm:', ['mode='])
    except getopt.GetoptError:
        print_help()

    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt == '-r':
            mode = 'raw'
        elif opt in ('-m', '--mode'):
            mode = arg
    if not args:
        print_help()

    return mode, args

# --- main ---

mode, args = parse_opts()
client = load_client()
print(do_question(client, ' '.join(args), mode))
