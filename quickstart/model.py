from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier

import mummify

data = load_wine()
X, y = data.data, data.target

model = KNeighborsClassifier(n_neighbors=10)
model.fit(X, y)
accuracy = round(model.score(X, y), 4)

mummify.log(accuracy)
