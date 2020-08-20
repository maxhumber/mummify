<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/mummify/master/assets/mummify.png" width="200px" alt="mummify">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/gazpacho/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-0-green"></a>
  <a href="https://travis-ci.org/maxhumber/mummify"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/mummify.svg"></a>
  <a href="https://pypi.python.org/pypi/mummify"><img alt="PyPI" src="https://img.shields.io/pypi/v/mummify.svg"></a>
  <a href="https://pepy.tech/project/mummify"><img alt="Downloads" src="https://pepy.tech/badge/mummify"></a>  
</p>

### About

`mummify` is a version control tool for machine learning. It's simple, fast, designed to help you focus on modeling.

### Quickstart

<img src="https://raw.githubusercontent.com/maxhumber/mummify/master/assets/quickstart.gif" width="400px" alt="quickstart">

### Usage

Import `mummify ` at the top and add `mummify.log(<string>)` to the bottom of your model:

```python
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier

import mummify

data = load_wine()
X, y = data.data, data.target

model = KNeighborsClassifier(n_neighbors=4)
model.fit(X, y)
accuracy = round(model.score(X, y), 4)

mummify.log(f'Accuracy: {accuracy}')
```

Run your model at the command:

```sh
python model.py
```

Edit your model:

```python
...
model = LogisticRegression()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

mummify.log(f'Test accuracy: {accuracy}')
```

View model history at the command line with:

```sh
mummify history
```

And peek at the the logged messages with:

```sh
cat mummify.log
```

Switch to an earlier model version:

```sh
mummify switch <id>
```

`mummify` will persist snapshots and the `mummify.log` through switches so that you can quickly move between past versions of your model.

#### Installation

```sh
pip install mummify
```

#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/chart/issues)
