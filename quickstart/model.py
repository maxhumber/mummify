from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier

data = load_wine()
X, y = data.data, data.target

model = KNeighborsClassifier(n_neighbors=4)
model.fit(X, y)
accuracy = round(model.score(X, y), 4)

print(accuracy)
