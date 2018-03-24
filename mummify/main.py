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

def history():
    '''CLI - view modified git'''
    graph = shell('git --git-dir=.mummify log --graph --decorate --oneline',
        capture_output=True)
    graph = re.sub('\s([a-zA-Z0-9_-]){7}\s', '  ', graph)
    graph = re.sub(r'\(HEAD -> master\)', 'HEAD', graph)
    return '\n' + graph + '\n'

def find(id):
    '''Find git commit id'''
    log_item = shell(f'git --git-dir=.mummify log --all --grep={id}',
        capture_output=True)
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    return commit

def switch(id):
    '''CLI - switch to mummify commit'''
    commit = find(id)
    shell([
        'git --git-dir=.mummify checkout -b logger',
        'git --git-dir=.mummify checkout -b switcher',
        f'git --git-dir=.mummify reset --hard {commit}',
        'git --git-dir=.mummify merge -s ours --no-commit master',
        f'git --git-dir=.mummify checkout logger {LOGFILE}',
        f'git --git-dir=.mummify commit -m "switch-{id}"',
        'git --git-dir=.mummify checkout master',
        'git --git-dir=.mummify merge switcher',
        'git --git-dir=.mummify branch -D logger',
        'git --git-dir=.mummify branch -D switcher'
    ])

def create_branch(BRANCH):
    '''Create new mummify branch'''
    git = (
        subprocess.Popen(
            'git --git-dir=.mummify status >/dev/null 2>&1 && echo True',
            shell=True,
            stdout=subprocess.PIPE
        ).communicate()[0].decode('utf-8').strip())
    if git:
        shell(f'git --git-dir=.mummify checkout -b {BRANCH}')
    else:
        shell('git init --separate-git-dir .mummify')
        shell("echo '.mummify' >> .gitignore", silent=False)
        shell([
            'git --git-dir=.mummify add .',
            'git --git-dir=.mummify commit -m "mummify-start"'
        ])
        print('Mummify Initialized!')

def commit(BRANCH):
    '''Commit run to mummify'''
    shell([
        'git --git-dir=.mummify add .',
        f'git --git-dir=.mummify commit -m {BRANCH} --quiet',
        'git --git-dir=.mummify checkout master --quiet',
        f'git --git-dir=.mummify merge {BRANCH} --quiet',
        f'git --git-dir=.mummify branch -d {BRANCH} --quiet'
    ])

def check_status():
    git_status = subprocess.Popen(
        "git --git-dir=.mummify status | grep 'nothing to commit'",
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0].decode('utf-8').strip()
    return git_status

def log(message):
    '''Main interface'''
    if check_status() == 'nothing to commit, working tree clean':
        return
    BRANCH = 'mummify-' + str(uuid.uuid4().hex)[:8]
    logger = logging.getLogger(BRANCH)
    logging.basicConfig(
        filename=LOGFILE,
        level=logging.INFO,
        style='{',
        format='[{name}] {message}'
    )
    create_branch(BRANCH)
    logger.info(message)
    print(message)
    commit(BRANCH)
