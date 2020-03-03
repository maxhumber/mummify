import logging
from pathlib import Path
import re
import subprocess
import uuid

LOGFILE = 'mummify.log'

def run(command, output=False, silent=False):
    '''Run shell commands

    - command (str): a bash command
    - output (bool, False): capture and return the STDOUT
    - silent (bool, False): force commands to run silently

    Example:

    `run('git --git-dir=.mummify status')`
    '''
    if silent:
        command += ' --quiet'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        output = s.stdout.decode('utf-8').strip()
        return output
    subprocess.run(command, shell=True)

def colour(string):
    '''Paint it purple!

    - string (str): colour a string purple

    Example:

    `purple('Hello World!')`
    '''
    print(f"\033[35m{string}\033[0m")

def init_mummify():
    '''Initialize mummify'''
    run('git --work-tree=. --git-dir=.mummify init', silent=True)
    run("echo '.mummify' >> .gitignore")
    run("echo '__pycache__' >> .gitignore")
    run('git --work-tree=. --git-dir=.mummify add .gitignore')
    run('git --work-tree=. --git-dir=.mummify commit -m "mummify-root"', silent=True)
    colour('Initializing mummify')

def history():
    '''View modified git graph (CLI)'''
    graph = run(
        'git --work-tree=. --git-dir=.mummify log --graph --decorate --oneline',
        output=True)
    graph = re.sub(r'\s([a-zA-Z0-9_-]){7}\s', '  ', graph)
    graph = re.sub(r'\(HEAD -> master\)', 'HEAD', graph)
    return f'\n{graph}\n'

def check_status():
    '''Check mummify git status'''
    git_status = run("git --work-tree=. --git-dir=.mummify status", output=True)
    return git_status

def create_branch(BRANCH):
    '''Create new mummify branch

    - BRANCH (str): branch UUID
    '''
    run(f'git --work-tree=. --git-dir=.mummify checkout -b {BRANCH}', silent=True)

def commit(BRANCH):
    '''Commit run to .mummify

    - BRANCH (str): branch UUID
    '''
    run('git --work-tree=. --git-dir=.mummify add .')
    run(f'git --work-tree=. --git-dir=.mummify commit -m {BRANCH}', silent=True)
    run('git --work-tree=. --git-dir=.mummify checkout master', silent=True)
    run(f'git --work-tree=. --git-dir=.mummify merge {BRANCH}', silent=True)
    run(f'git --work-tree=. --git-dir=.mummify branch -d {BRANCH}', silent=True)

def find(id):
    '''Find git commit based on mummify id

    - id (str): branch UUID

    Example:

    `find('mummify-2d234a8a')`
    '''
    log_item = run(
        f'git --work-tree=. --git-dir=.mummify log --all --grep={id}',
        output=True)
    commit = re.findall(r'(?<=commit\s)(.*?)(?=\n)', log_item)[0]
    return commit

def switch(id):
    '''Switch to a specific mummify commit (CLI)

    - id (str): branch UUID

    Example:

    `switch('mummify-2d234a8a')`
    '''
    commit = find(id)
    run('git --work-tree=. --git-dir=.mummify checkout -b logger', silent=True)
    run('git --work-tree=. --git-dir=.mummify checkout -b switcher', silent=True)
    run(f'git --work-tree=. --git-dir=.mummify reset --hard {commit}', silent=True)
    run('git --work-tree=. --git-dir=.mummify merge -s ours --no-commit master', silent=True)
    run(f'git --work-tree=. --git-dir=.mummify checkout logger {LOGFILE}', silent=True)
    run(f'git --work-tree=. --git-dir=.mummify commit -m "switch-{id}"', silent=True)
    run('git --work-tree=. --git-dir=.mummify checkout master', silent=True)
    run('git --work-tree=. --git-dir=.mummify merge switcher', silent=True)
    run('git --work-tree=. --git-dir=.mummify branch -D logger', silent=True)
    run('git --work-tree=. --git-dir=.mummify branch -D switcher', silent=True)
    return colour(f'Sucessfully switched to {id}')

def log(message):
    '''Log a message to mummify.log and save a snapshot

    - message (str): message to be logged

    Example:

    `log('Accuracy: 0.98')`
    '''
    logging.basicConfig(
        filename=LOGFILE,
        level=logging.INFO,
        style='{',
        format='[{name}] {message}'
    )
    BRANCH = f'mummify-{str(uuid.uuid4().hex)[:8]}'
    logger = logging.getLogger(BRANCH)
    if not Path('.mummify').is_dir():
        init_mummify()
    if 'nothing to commit' in check_status():
        colour('Nothing changed, nothing logged')
        return None
    create_branch(BRANCH)
    logger.info(message)
    colour(message)
    commit(BRANCH)
