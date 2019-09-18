import os
from pathlib import Path
import re
import subprocess

import mummify

def setup_mummify():
    subprocess.call(["echo 'test_mummify.py' >> .gitignore"], shell=True)
    contents = '''
import mummify
accuracy = 0.80
mummify.log(f'Accruacy: {accuracy:.3f}')
'''
    with open('model.py', 'w+') as f:
        f.write(contents)
    subprocess.call(['python model.py &>/dev/null'], shell=True)

def check_status():
    git_status = subprocess.Popen(
        "git --git-dir=.mummify status | grep 'nothing to commit'",
        shell=True,
        stdout=subprocess.PIPE
    ).communicate()[0].decode('utf-8').strip()
    return git_status

def check_log_line_count():
    return int(subprocess.check_output('wc -l mummify.log', shell=True).split()[0])

def simulate_change(new):
    with open('model.py', "r+") as f:
        contents = f.read()
        contents = re.sub(r'(?<=\=\s)(.*?)(?=\n)', f'{new}', contents)
        f.seek(0)
        f.write(contents)
        f.truncate()
    subprocess.call(['python model.py &>/dev/null'], shell=True)

def check_history():
    history = (
        subprocess.check_output(['mummify history'], shell=True)
        .decode('utf-8').strip()
    )
    return history

def tear_down_mummify():
    subprocess.call([f'rm .git .gitignore mummify.log model.py'], shell=True)
    subprocess.call(['rm -rf .mummify'], shell=True)
    return None

def test_mummify():
    os.chdir('tests')
    setup_mummify()
    print(subprocess.check_output(['git --version'], shell=True).decode('utf-8'))
    assert check_status() == 'nothing to commit, working tree clean'
    assert check_log_line_count() == 1
    simulate_change(0.75)
    assert check_log_line_count() == 2
    simulate_change(0.82)
    simulate_change(0.87)
    simulate_change(0.85)
    assert check_log_line_count() == 5
    assert check_history().count('*') == 6
    with open('mummify.log', 'r') as f:
        log = f.readlines()
    log_line = log[3]
    mummify_id = re.search(r'(?<=\-)(.*)(?=\])', log_line).group(0)
    subprocess.call([f'mummify switch {mummify_id}'], shell=True)
    assert check_history().count('*') == 7
    with open('model.py', 'r') as f:
        model = f.read()
    score = float(re.search(r'(?<=\=\s)(.*)(?=\n)', model).group(0))
    assert score == 0.87
    tear_down_mummify()
