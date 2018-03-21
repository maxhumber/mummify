import logging
import uuid
import re
import subprocess
from ast import literal_eval

LOGFILE = 'mummify.log'

def shell(command, capture_output=False, silent=True):
    '''Execute bash commands'''
    if type(command) is str:
        command = [command]
    if capture_output:
        o = [
            subprocess.check_output([c], shell=True)
            .decode('utf-8')
            .strip()
            for c in command]
        if len(o) == 1:
            return o[0]
        else:
            return o
    if silent:
        command = [c + ' &>/dev/null' for c in command]
    [subprocess.call([c], shell=True) for c in command]
    return None

def view():
    '''CLI - view modified git graph'''
    graph = shell('git log --graph --decorate --oneline', capture_output=True)
    graph = re.sub('\s([a-zA-Z0-9_-]){7}\s', '  ', graph)
    graph = re.sub(r'\(HEAD -> master\)', 'CURRENT', graph)
    return '\n' + graph + '\n'

def find(id):
    '''Find git commit id'''
    log_item = shell(f'git log --all --grep={id}', capture_output=True)
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    return commit

def switch(id):
    '''CLI - switch to mummify commit'''
    commit = find(id)
    shell([
        'git checkout -b logger',
        'git checkout -b switch',
        f'git reset --hard {commit}',
        'git merge -s ours --no-commit master',
        f'git checkout log {LOGFILE}',
        f'git commit -m "switch-{id}"',
        'git checkout master',
        'git merge switch',
        'git branch -D logger',
        'git branch -D switch'
    ])

def create_branch(BRANCH):
    '''Create new mummify branch'''
    git = (
        subprocess.Popen(
            'git status >/dev/null 2>&1 && echo True',
            shell=True,
            stdout=subprocess.PIPE
        ).communicate()[0].decode('utf-8').strip())
    if git:
        shell(f'git checkout -b {BRANCH}')
    else:
        shell([
            'git init',
            'git add .',
            'git commit -m "mummify-start"'
        ])

def commit(BRANCH):
    '''Commit run to mummify'''
    shell([
        'git add .',
        f'git commit -m {BRANCH} --quiet',
        'git checkout master --quiet',
        f'git merge {BRANCH} --quiet',
        f'git branch -d {BRANCH} --quiet'
    ])

def log(message):
    '''Main interface'''
    BRANCH = 'mummify-' + str(uuid.uuid4().hex)[:8]
    logger = logging.getLogger(BRANCH)
    logging.basicConfig(
        filename=LOGFILE,
        level=logging.INFO,
        style='{',
        format='{name}|{message}'
    )
    create_branch(BRANCH)
    logger.info(message)
    commit(BRANCH)
