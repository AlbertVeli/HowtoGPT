#!/usr/bin/env python3
#
# ChatGPT script based on https://gynvael.coldwind.pl/?lang=en&id=771
# which in turn is based on the openai examples:
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

from openai import OpenAI
import sys
import os
import getopt

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

# Uses global variable mode (set by parse_opts)
def do_question(s):
    #m = 'gpt-3.5-turbo'
    m = 'gpt-4o'
    system = 'You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.'

    if mode == 'raw':
        prompt = ''
    else:
        # mode cmdline
        prompt = f'Answer with only the actual command without any intro or explanation. What is the {mode} command line command to '

    user = prompt + s

    ret = client.chat.completions.create(model = m,
    messages = [ {'role': 'system', 'content': system}, {'role': 'user', 'content': user} ])
    md = ret.model_dump()
    text = md['choices'][0]['message']['content']
    return text

def print_help():
    print(f'Usage: {sys.argv[0]} [-h] [-r] [-m <system>] <question>')
    print('')
    print('  Use -m raw (or -r) for a raw question or')
    print('  the name of any system for a cmdline.')
    print('  Default value is "ubuntu".')
    print('')
    print('  EXAMPLES')
    print('')
    print(f'  $ {sys.argv[0]} reverse lines in one file')
    print('  tac <filename>')
    print('')
    print(f'  $ {sys.argv[0]} -m powershell reverse lines in one file')
    print('  Get-Content -Path "file.txt" | Select-Object -Reverse | Set-Content -Path "reversed.txt"')
    print('')
    print(f'  $ {sys.argv[0]} -r describe the gecos field in a unix password file')
    print('  The GECOS field in a Unix password file contains general information about a user. It')
    print('  typically includes the user\'s full name, contact information, office location, and')
    print('  other optional details. This field is primarily used for administrative purposes and')
    print('  may vary depending on the Unix system in use.')
    sys.exit(1)

# parse options
def parse_opts():
    global mode
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
    if len(args) == 0:
        print_help()

    return args

# --- main ---

# args = arguments left after parsing flags
args = parse_opts()
load_secrets()

print(do_question(' '.join(args)))
