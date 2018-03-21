import subprocess
file = 'model.py'

# instantiate
with open(file, 'w+') as f:
    f.seek(0, 0)

# first write
contents = '''import mummify
train_accuracy = 0.80
test_accuracy = 0.80
mummify.log(f'Train: {train_accuracy:.3f}, Test: {test_accuracy:.3f}')
'''

with open(file, "w") as f:
    f.write(contents)

subprocess.call(['python model.py'], shell=True)


# first change
with open('model.py', )


with open(f'manuscript/{notebook}.txt', encoding='UTF-8') as f:
    chapter = f.read()

# correct image locations
chapter = chapter.replace(f'({notebook}_files/', '(images/')
chapter = chapter.replace(f'(../manuscript/', '(')
chapter = chapter.replace(f'![png](', '![](')

with open()
