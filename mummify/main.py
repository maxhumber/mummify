import logging
import uuid
import re
import subprocess
from subprocess import CalledProcessError

def _bash(command, mode='', capture=False):
    if capture:
        return subprocess.check_output([command + mode], shell=True)
    else:
        subprocess.call([command + mode], shell=True)

class Mummify:

    def __init__(self, quiet=True):
        self.MODE = (' --quiet' if quiet else '')
        self.BRANCH = 'mummify-' + str(uuid.uuid4().hex)[:8]
        self.logger = logging.getLogger(self.BRANCH)
        logging.basicConfig(
            filename='mummify.log',
            level=logging.INFO,
            style='{',
            format='{name}|{message}'
        )
        try:
            _bash(f'git checkout -b {self.BRANCH}', self.MODE, capture=True)
        # instantiate git if not present
        except CalledProcessError:
            _bash('git init', self.MODE)
            _bash('git add .')
            _bash('git commit -m "initial commit"', self.MODE)
            _bash(f'git checkout -b {self.BRANCH}', self.MODE)

    def log(self, message, commit=False):
        self.logger.info(message)
        if commit:
            self.commit()

    def commit(self):
        _bash(f'git add .')
        _bash(f'git commit -m {self.BRANCH}', self.MODE)
        _bash(f'git checkout master', self.MODE)
        _bash(f'git merge {self.BRANCH}', self.MODE)
        _bash(f'git branch -d {self.BRANCH}', self.MODE)

# TODO: need to make this work
# identifier = 1234
def find(identifier):
    log_item = _bash(f'git log --all --grep={identifier}', capture=True)
    log_item = log_item.decode('utf-8')
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    print(commit)

#
