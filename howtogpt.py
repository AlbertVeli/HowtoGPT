#!/usr/bin/env python3
#
# ChatGPT script based on https://gynvael.coldwind.pl/?lang=en&id=771
# which in turn is based on the openai examples:
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

import openai
import sys
import os
import getopt

def load_secrets():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # https://platform.openai.com/account/api-keys
    # Do not check in secrets, put these in .gitignore
    with open(f'{dir_path}/api_key.txt') as f:
        openai.api_key = f.read().strip()
    with open(f'{dir_path}/api_organization.txt') as f:
        openai.organization = f.read().strip()

# Uses global variable mode (set by parse_opts)
def do_question(s):
    m = 'gpt-3.5-turbo'
    # m = 'gpt-4'
    system = 'You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.'

    if mode == 'raw':
        prompt = ''
    else:
        # mode cmdline
        prompt = f'Answer with only the actual command without any intro or explanation. What is the {mode} command line command to '

    user = prompt + s

    ret = openai.ChatCompletion.create(
            model = m,
            messages = [ {'role': 'system', 'content': system}, {'role': 'user', 'content': user} ]
            )
    text = ret['choices'][0]['message']['content']
    if text.startswith('`') and text.endswith('`'):
        text = text[1:-1]
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
    print(f'  $ {sys.argv[0]} -r What do you know about the japanese wwii unit 731?')
    print('  Unit 731 was a covert biological and chemical warfare research unit of the Imperial Japanese')
    print('  Army during World War II. It conducted unethical human experimentation on prisoners, including')
    print('  infecting them with deadly diseases to study their effects. This included vivisections, frostbite')
    print('  studies, and testing various weapons. The unit\'s activities were kept classified until the end')
    print('  of the war, and those involved largely evaded prosecution in exchange for sharing their research')
    print('  with the Allies.')
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
            sys.exit(0)
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
