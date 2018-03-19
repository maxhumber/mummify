import logging
import uuid
import re
import subprocess
from subprocess import CalledProcessError

LOGFILE = 'mummify.log'

def _bash(command, capture=False):
    if capture:
        return subprocess.check_output([command], shell=True)
    else:
        subprocess.call([command], shell=True)


class Mummify:

    def __init__(self, message):
        self.message = message
        self.BRANCH = 'mummify-' + str(uuid.uuid4().hex)[:8]
        self.logger = logging.getLogger(self.BRANCH)
        logging.basicConfig(
            filename=LOGFILE,
            level=logging.INFO,
            style='{',
            format='{name}|{message}'
        )
        try:
            _bash(f'git checkout -b {self.BRANCH} --quiet', capture=True)
        # instantiate git if not present
        except CalledProcessError:
            _bash('git init --quiet')
            _bash('git add .')
            _bash('git commit -m "{self.BRANCH}" --quiet')
        self.log(message)

    def log(self, message):
        self.logger.info(message)
        self._commit()

    def _commit(self):
        _bash(f'git add .')
        _bash(f'git commit -m {self.BRANCH} --quiet')
        _bash(f'git checkout master --quiet')
        _bash(f'git merge {self.BRANCH} --quiet')
        _bash(f'git branch -d {self.BRANCH} --quiet')


def _find(identifier):
    log_item = _bash(f'git log --all --grep={identifier}', capture=True)
    log_item = log_item.decode('utf-8')
    commit = re.findall('(?<=commit\s)(.*?)(?=\n)',log_item)[0]
    return commit

def rewind(identifier):
    commit = _find(identifier)
    _bash(f'git add {LOGFILE}')
    _bash('git commit -m "mummify save log" --quiet')
    _bash(f'git reset --soft {commit} --quiet')
    _bash('git reset HEAD~ --quiet')
