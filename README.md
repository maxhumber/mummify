<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/mummify/master/images/mummify.png" width="200px" alt="chart">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-zero-blueviolet"></a>
  <a href="https://travis-ci.org/maxhumber/mummify"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/mummify.svg"></a>
  <a href="https://pypi.python.org/pypi/mummify"><img alt="PyPI" src="https://img.shields.io/pypi/v/mummify.svg"></a>
  <a href="https://pepy.tech/project/mummify"><img alt="Downloads" src="https://pepy.tech/badge/mummify"></a>  
</p>

#### About

mummify makes model prototyping faster. The package automagically takes care of git and logging for your machine learning project so that you can focus on what's important.

#### Functions

mummify is one function and two command line tools:

- `log` - to automatically log and commit model changes
- `mummify history` - to view those changes
- `mummify switch` - to go back to a different version of your model

#### Usage

mummify is simple to use. Just add `import mummify` at the top and `mummify.log(<string>)` at the bottom of your model:

```python
import mummify

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

data = load_wine()
y = data.target
X = data.data

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = KNeighborsClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

mummify.log(f'Test accuracy: {accuracy:.3f}')
```

When you run your model (`python model.py`) for the first time mummify will create a protected `.mummify ` git folder and will start to log messages to a `mummify.log` file.

When you make changes and run everything again:

```python
...
model = LogisticRegression()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

mummify.log(f'Test accuracy: {accuracy:.3f}')
```

mummify will update the `mummify.log` file and save a snapshot of your working directory.

To view the history of your model, just run  `mummify history` from the command line:

```sh
max$ mummify history

*  HEAD mummify-3d15c7c2
*  mummify-2d234a8a
*  mummify-1fad5388
*  mummify-root
```

And to go back to a previous snapshot of your model just grab the mummify id from the `mummify.log` file and run `mummify switch <id>` from the command line:

```sh
max$ mummify switch mummify-2d234a8a
```

mummify will preserve all state history during and after a switch and keep the `mummify.log` file intact.

#### Installation

```sh
pip install mummify
```

#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/chart/issues)
