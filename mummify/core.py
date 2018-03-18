import logging
import uuid
import subprocess
from subprocess import CalledProcessError

class Mummify:

    def __init__(self):
        self.BRANCH = 'mummify-' + str(uuid.uuid4())
        self.logger = logging.getLogger(self.BRANCH)
        logging.basicConfig(
            filename='mummify.log',
            level=logging.INFO,
            style='{',
            format='{name}|{message}'
        )
        try:
            subprocess.check_output([f'git checkout -b {self.BRANCH}'], shell=True)
        except CalledProcessError:
            subprocess.call(['git init'], shell=True)
            subprocess.call(['git add .'], shell=True)
            subprocess.call(['git commit -m "initial commit"'], shell=True)
            subprocess.call([f'git checkout -b {self.BRANCH}'], shell=True)

    def log(self, message):
        self.logger.info(message)

    def commit(self):
        subprocess.call([f'git add .'], shell=True)
        subprocess.call([f'git commit -m {self.BRANCH}'], shell=True)
        subprocess.call([f'git checkout master'], shell=True)
        subprocess.call([f'git merge {self.BRANCH}'], shell=True)
        subprocess.call([f'git branch -d {self.BRANCH}'], shell=True)
