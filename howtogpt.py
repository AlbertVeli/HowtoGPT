#!/usr/bin/env python3
#
# ChatGPT script based on https://gynvael.coldwind.pl/?lang=en&id=771
# which in turn is based on the openai examples:
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

import os
import sys
import getopt
try:
    from openai import OpenAI
except ImportError:
    print('Please install openai with "apt install python3-openai" or pip')
    sys.exit(1)
try:
    from dotenv import dotenv_values
except ImportError:
    print('Please install python-dotenv with "apt install python3-dotenv" or pip')
    sys.exit(1)

client = None

def load_secrets():
    global client
    # Load API key and organization from .env file
    # Don't forget to add .env to your .gitignore file
    path = os.path.dirname(os.path.realpath(__file__)) + os.sep
    if not os.path.exists(path + '.env'):
        print('Please create a .env file with your OpenAI API key and organization')
        sys.exit(1)
    config = dotenv_values(path + ".env")
    client = OpenAI(api_key = config['OPENAI_API_KEY'],
                    organization = config['OPENAI_ORGANIZATION'])
    if client is None:
        print('Could not load valid OpenAI API key and organization from .env file')
        sys.exit(1)

# Uses global variable mode (set by parse_opts)
def do_question(s):
    #m = 'gpt-3.5-turbo'
    m = 'gpt-4o'
    system = 'You are a CLI assistant. Provide only the command, no explanations or extra text.'

    if mode == 'raw':
        prompt = ''
    else:
        # mode cmdline (default is Ubuntu)
        prompt = f'Provide the {mode} command-line command to '

    user = prompt + s

    ret = client.chat.completions.create(model = m,
    messages = [ {'role': 'system', 'content': system}, {'role': 'user', 'content': user} ])
    md = ret.model_dump()
    text = md['choices'][0]['message']['content']
    # Clean up answer text
    text = text.strip()
    if text.startswith('``'):
        # Remove first line which starts with ``
        # or ```bash or similar, cmd is in the next line
        lines = text.split('\n')
        if len(lines) > 1:
            text = lines[1]
    if text[0] == '`' or text[0] == '"' or text[0] == "'":
        # Remove quotes
        text = text[1:-1]
    return text

def print_help():
    print(f'Usage: {sys.argv[0]} [-h] [-r] [-m <system>] <question>')
    print('')
    print('  Use -m raw (or -r) for a raw question or')
    print('  the name of any system for a cmdline.')
    print('  Default value is "Ubuntu".')
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

answer = do_question(' '.join(args))
print(answer)
