<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/mummify/master/images/mummify.png" width="200px" alt="chart">
</h3>
<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="MIT" src="https://img.shields.io/github/license/maxhumber/mummify.svg"></a>
  <a href="https://travis-ci.org/maxhumber/mummify"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/mummify.svg"></a>
  <a href="https://pypi.python.org/pypi/mummify"><img alt="PyPI" src="https://img.shields.io/pypi/v/mummify.svg"></a>
  <a href="https://pypi.python.org/pypi/mummify"><img alt="Downloads" src="https://img.shields.io/pypi/dm/mummify.svg"></a>
</p>

#### About

mummify makes model prototyping faster. The package manages git and performance logging for your machine learning project so that you can focus on what's important...

#### Functions

mummify is composed of just three simple functions:

- `log` - to automatically log and commit model changes
- `history` - to view model changes over time
- `switch` - to switch back to an earlier version of your model

#### Usage

Import `mummify` at the top of your script (in this case, `model.py`) and add `mummify.log(<message>)` at the very end:

```
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

When you call `python model.py` from the command line, mummify will initialize a protected `.mummify` git directory, create a `mummify.log` file, and automtically keep track of model performance:

![](https://raw.githubusercontent.com/maxhumber/mummify/master/images/mummify-init.png)

Whenever you make a change to your model (try a different algorithm)...

```
import mummify
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = load_wine()
y = data.target
X = data.data

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
mummify.log(f'Test accuracy: {accuracy:.3f}')
```

...and re-run `python model.py` mummify will update the `mummify.log` file and save the state of your model:

![](https://raw.githubusercontent.com/maxhumber/mummify/master/images/mummify-first-change.png)

To view the history of your model, just run  `mummify history` from the command line:

```
max-mbp:quick-start max$ mummify history

*  HEAD mummify-f0e66a82
*  mummify-75dea5e9
*  mummify-start

max-mbp:quick-start max$
```

And to rewind or jump back to a previous state, just grab the mummify identifier that you would like switch to from the `mummify.log` file and run `mummify switch <id>` from the command line:

![](https://raw.githubusercontent.com/maxhumber/mummify/master/images/mummify-switch.png)

mummify will preserve all state history during and after a switch and keep the `mummify.log` file immutable.

#### Installation

```
pip install mummify
```

#### Contribute

For feature requests or bug reports, please use [Github Issues](https://github.com/maxhumber/chart/issues)
