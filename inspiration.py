import logging
import subprocess
import uuid

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

branch = str(uuid.uuid4())

subprocess.check_output(['git show -s --format=%h'], shell=True).decode('utf-8').strip()
subprocess.call([f'git checkout -b {branch}'], shell=True)

logger = logging.getLogger(branch)
logging.basicConfig(
    filename='model.log',
    level=logging.INFO,
    style='{',
    format='BRANCH|{name}|{message}'
)

df = pd.read_csv('data/data.csv')

y = df['y'].values
X = df.drop('y', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

model = LogisticRegression()
model.fit(X_train, y_train)
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)
logger.info(f'Train Accuracy: {train_accuracy}, Test Accuracy: {test_accuracy}')

subprocess.call([f'git add .'], shell=True)
subprocess.call([f'git commit -m {branch}'], shell=True)
subprocess.call([f'git checkout master'], shell=True)
subprocess.call([f'git merge {branch}'], shell=True)
subprocess.call([f'git branch -d {branch}'], shell=True)
