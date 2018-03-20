import os
import logging
import uuid
import re
from subprocess import call, check_output, CalledProcessError

LOGFILE = 'mummify.log'

#TODO: accept a list of commands
def _execute(command, output=False):
    if output:
        return check_output([command], shell=True).decode('utf-8').strip()
    else:
        call([command], shell=True)

def _find(id):
    log_item = _execute(f'git log --all --grep={id}', output=True)
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    return commit

#TODO: supress git messages
#TODO: make this cleaner
def switch(id):
    commit = _find(id)
    _execute('git checkout -b log --quiet')
    _execute('git checkout -b switch --quiet')
    _execute(f'git reset --hard {commit} --quiet')
    _execute('git merge -s ours --no-commit master --quiet')
    _execute(f'git checkout log {LOGFILE} --quiet')
    #TODO: remove mummify- ?
    _execute(f'git commit -m "switch-{id}" --quiet')
    _execute('git checkout master --quiet')
    _execute('git merge switch --quiet')
    _execute('git branch -D log --quiet')
    _execute('git branch -D switch --quiet')

#TODO: fix the git fatal message
def _create_branch(BRANCH):
    try:
        _execute(f'git checkout -b {BRANCH} --quiet', output=True)
    except CalledProcessError:
        _execute('git init --quiet')
        _execute('git add .')
        _execute('git commit -m "mummify-start" --quiet')

def _commit(BRANCH):
    _execute(f'git add .')
    _execute(f'git commit -m {BRANCH} --quiet')
    _execute(f'git checkout master --quiet')
    _execute(f'git merge {BRANCH} --quiet')
    _execute(f'git branch -d {BRANCH} --quiet')

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
