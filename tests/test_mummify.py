import subprocess
import re
from ast import literal_eval
from pathlib import Path

file = 'model.py'
contents = '''import mummify
test_accuracy = 0.80
mummify.log(f'Test: {test_accuracy:.3f}')
'''

def setup_mummify():
    subprocess.call(["echo 'test_mummify.py' >> .gitignore"], shell=True)
    with open(file, 'w+') as f:
        f.write(contents)
    subprocess.call(['python model.py &>/dev/null'], shell=True)
    return None

def check_status():
    git_status = subprocess.Popen(
            "git --git-dir=.mummify status | grep 'nothing to commit'",
            shell=True,
            stdout=subprocess.PIPE
        ).communicate()[0].decode('utf-8').strip()
    return git_status

def check_log_line_count():
    return int(subprocess.check_output('wc -l mummify.log', shell=True).split()[0])

def fake_change(file, new):
    with open(file, "r+") as f:
        contents = f.read()
        contents = re.sub('(?<=\=\s)(.*?)(?=\n)', f'{new}', contents)
        f.seek(0)
        f.write(contents)
        f.truncate()
    return None

def test_first_mummify_log():
    setup_mummify()
    errors = []
    if not Path('.mummify').is_dir():
        errors.append('.mummify wasn\'t properly initialized')
    if not check_status() == 'nothing to commit, working tree clean':
        errors.append('mummify didn\'t properly commit everything')
    if not check_log_line_count() == 1:
        errors.append('mummify didn\'t properly log')
    assert not errors, 'errors occured:\n{}'.format('\n'.join(errors))

def test_first_change():
    fake_change(file, 0.83)
    errors = []
    if not check_status() == '':
        errors.append('change wasn\'t made')
    subprocess.call(['python model.py &>/dev/null'], shell=True)
    if not check_status() == 'nothing to commit, working tree clean':
        errors.append('mummify didn\'t properly commit everything')
    if not check_log_line_count() == 2:
        errors.append('mummify didn\'t properly log')
    assert not errors, 'errors occured:\n{}'.format('\n'.join(errors))

def test_multiple_changes():
    fake_change(file, 0.72)
    subprocess.call(['python model.py &>/dev/null'], shell=True)
    fake_change(file, 0.74)
    subprocess.call(['python model.py &>/dev/null'], shell=True)
    errors = []
    if not check_log_line_count() == 4:
        errors.append('mummify didn\'t properly log')
    assert not errors, 'errors occured:\n{}'.format('\n'.join(errors))

def test_mummify_history():
    history = (
        subprocess.check_output(['mummify history'], shell=True)
        .decode('utf-8').strip())
    assert history.count('*') == 5


test_first_mummify_log()
test_first_change()
test_multiple_changes()
test_mummify_history()
tear_down_mummify()


# history = subprocess.check_output(['mummify history'], shell=True).decode('utf-8').strip()
# print(history)
# history.splitlines()[-3].replace('*  ', '')
#
# history[-3]
#
# mummify_id = re.search('(?<=\n\*\s\s)(.*)(?=\n\*\s\smummify-start)', history).group(0)
#
# subprocess.call([f'mummify switch {mummify_id}'], shell=True)
#
# def tear_down_mummify():
#     subprocess.call([f'rm .git .gitignore mummify.log {file}'], shell=True)
#     subprocess.call(['rm -rf .mummify'], shell=True)
#     return None
#
# tear_down_mummify()
