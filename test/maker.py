import subprocess
import re

file = 'model.py'
contents = '''import mummify
train_accuracy = 0.80
test_accuracy = 0.80
mummify.log(f'Train: {train_accuracy:.3f}, Test: {test_accuracy:.3f}')
'''

# instantiate 'model'
with open(file, 'w+') as f:
    f.write(contents)

# first mummify log
subprocess.call(['python model.py &>/dev/null'], shell=True)
subprocess.call(["echo 'maker.py' >> .gitignore"], shell=True)

# change
def fake_change(file, previous, new):
    with open(file, "r+") as f:
        contents = f.read()
        contents = contents.replace(previous, new)
        f.seek(0)
        f.write(contents)
        f.truncate()

fake_change(file, '0.80', '0.750')

subprocess.call(['python model.py &>/dev/null'], shell=True)

fake_change(file, '0.750', '0.767')

history = subprocess.check_output(['mummify history'], shell=True).decode('utf-8').strip()
mummify_id = re.search('(?<=\n\*\s\s)(.*)(?=\n\*\s\smummify-start)', history).group(0)

subprocess.call([f'mummify switch {mummify_id}'], shell=True)

def tear_down():
    subprocess.call(['rm .git .gitignore model.py mummify.log'], shell=True)
    subprocess.call(['rm -rf .mummify'], shell=True)

tear_down()
