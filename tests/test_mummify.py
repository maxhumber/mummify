import os
from pathlib import Path
import re
import subprocess

import mummify

def setup_mummify():
    subprocess.run("echo 'test_mummify.py' >> .gitignore", shell=True)
    subprocess.run("echo '__pycache__' >> .gitignore", shell=True)
    contents = '''import mummify
accuracy = 0.80
mummify.log(f'Accruacy: {accuracy:.3f}')
'''
    with open('model.py', 'w+') as f:
        f.write(contents)
    subprocess.run('python model.py', shell=True)

def check_status():
    s = subprocess.run(
        'git --git-dir=.mummify status',
        shell=True,
        capture_output=True)
    return s.stdout.decode('utf-8').strip()

def check_log_line_count():
    s = subprocess.run('wc -l mummify.log', shell=True, capture_output=True)
    return int(s.stdout.decode('utf-8').strip().split(' ')[0])

def simulate_change(new):
    with open('model.py', "r+") as f:
        contents = f.read()
        contents = re.sub(r'(?<=\=\s)(.*?)(?=\n)', f'{new}', contents)
        f.seek(0)
        f.write(contents)
        f.truncate()
    subprocess.run('python model.py', shell=True)

def check_history():
    s = subprocess.run('mummify history', capture_output=True, shell=True)
    return s.stdout.decode('utf-8').strip()

def tear_down_mummify():
    subprocess.run(
        'rm -rf .gitignore .git .mummify mummify.log model.py',
        shell=True)

def test_mummify():
    os.chdir('tests')
    setup_mummify()
    assert 'nothing to commit' in check_status()
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
    subprocess.run(f'mummify switch {mummify_id}', shell=True)
    assert check_history().count('*') == 7
    with open('model.py', 'r') as f:
        model = f.read()
    score = float(re.search(r'(?<=\=\s)(.*)(?=\n)', model).group(0))
    assert score == 0.87
    tear_down_mummify()
