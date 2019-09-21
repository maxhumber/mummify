import logging
from pathlib import Path
import re
import subprocess
import uuid

LOGFILE = 'mummify.log'

# TODO: fix silent
def run(command, output=False, silent=True):
    '''Run shell commands'''
    # if silent and not output:
    #     command += ' &>/dev/null'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        output = s.stdout.decode('utf-8').strip()
        return output
    else:
        subprocess.run(command, shell=True)

def colour(string):
    '''Paint it purple!'''
    print(f"\033[35m{string}\033[0m")

def init_mummify():
    '''Initialize mummify'''
    run('git init --separate-git-dir .mummify')
    run("echo '.mummify' >> .gitignore")
    run("echo '__pycache__' >> .gitignore") # delete
    run('git --git-dir=.mummify add .gitignore')
    run('git --git-dir=.mummify commit -m "mummify-root"')
    colour('mummify initialized')

def history():
    '''View modified git graph (CLI)'''
    graph = run(
        'git --git-dir=.mummify log --graph --decorate --oneline',
        output=True)
    graph = re.sub(r'\s([a-zA-Z0-9_-]){7}\s', '  ', graph)
    graph = re.sub(r'\(HEAD -> master\)', 'HEAD', graph)
    print(f'\n{graph}\n')

def check_status():
    '''Check mummify git status'''
    git_status = run("git --git-dir=.mummify status", output=True)
    return git_status

def create_branch(BRANCH):
    '''Create new mummify branch'''
    run(f'git --git-dir=.mummify checkout -b {BRANCH}')

def commit(BRANCH):
    '''Commit run to .mummify'''
    run('git --git-dir=.mummify add .')
    run(f'git --git-dir=.mummify commit -m {BRANCH} --quiet')
    run('git --git-dir=.mummify checkout master --quiet')
    run(f'git --git-dir=.mummify merge {BRANCH} --quiet')
    run(f'git --git-dir=.mummify branch -d {BRANCH} --quiet')

def find(id):
    '''Find git commit based on mummify id'''
    log_item = run(
        f'git --git-dir=.mummify log --all --grep={id}',
        output=True)
    commit = re.findall(r'(?<=commit\s)(.*?)(?=\n)', log_item)[0]
    return commit

def switch(id):
    '''Switch to a specific mummify commit (CLI)'''
    commit = find(id)
    run('git --git-dir=.mummify checkout -b logger')
    run('git --git-dir=.mummify checkout -b switcher')
    run(f'git --git-dir=.mummify reset --hard {commit}')
    run('git --git-dir=.mummify merge -s ours --no-commit master')
    run(f'git --git-dir=.mummify checkout logger {LOGFILE}')
    run(f'git --git-dir=.mummify commit -m "switch-{id}"')
    run('git --git-dir=.mummify checkout master')
    run('git --git-dir=.mummify merge switcher')
    run('git --git-dir=.mummify branch -D logger')
    run('git --git-dir=.mummify branch -D switcher')

def log(message):
    '''Log a message to mummify.log and save a snapshot'''
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

# # delete
# def cleanup():
#     run('rm -rf .gitignore .git .mummify mummify.log')
