import os
import logging
import uuid
import re
from subprocess import call, check_output, CalledProcessError

LOGFILE = 'mummify.log'

def shell(command, silent=True, output=False):
    if type(command) is str:
        command = [command]
    if output:
        o = [
            check_output([c], shell=True)
            .decode('utf-8')
            .strip()
            for c in command]
        if len(o) == 1:
            return o[0]
        else:
            return o
    else:
        [call([c], shell=True) for c in command]
        return None

def _find(id):
    log_item = shell(f'git log --all --grep={id}', output=True)
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    return commit

def view():
    graph = shell('git log --graph --decorate --oneline', output=True)
    graph = re.sub('\s([a-zA-Z0-9_-]){7}\s', '  ', graph)
    graph = re.sub(r'\(HEAD -> master\)', 'CURRENT', graph)
    return '\n' + graph + '\n'

#TODO: supress git messages
#TODO: make this cleaner
def switch(id):
    commit = _find(id)
    shell('git checkout -b log --quiet')
    shell('git checkout -b switch --quiet')
    shell(f'git reset --hard {commit} --quiet')
    shell('git merge -s ours --no-commit master --quiet')
    shell(f'git checkout log {LOGFILE} --quiet')
    #TODO: remove mummify- ?
    shell(f'git commit -m "switch-{id}" --quiet')
    shell('git checkout master --quiet')
    shell('git merge switch --quiet')
    shell('git branch -D log --quiet')
    shell('git branch -D switch --quiet')

#TODO: fix the git fatal message
def _create_branch(BRANCH):
    try:
        shell(f'git checkout -b {BRANCH} --quiet', output=True)
    except CalledProcessError:
        shell('git init --quiet')
        shell('git add .')
        shell('git commit -m "mummify-start" --quiet')

def _commit(BRANCH):
    shell('git add .')
    shell(f'git commit -m {BRANCH} --quiet')
    shell('git checkout master --quiet')
    shell(f'git merge {BRANCH} --quiet')
    shell(f'git branch -d {BRANCH} --quiet')

def log(message):
    BRANCH = 'mummify-' + str(uuid.uuid4().hex)[:8]
    logger = logging.getLogger(BRANCH)
    logging.basicConfig(
        filename=LOGFILE,
        level=logging.INFO,
        style='{',
        format='{name}|{message}'
    )
    _create_branch(BRANCH)
    logger.info(message)
    _commit(BRANCH)
