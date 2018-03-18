import io
import pkgutil
import pandas as pd

data = pkgutil.get_data('mummify', 'datasets/mummy.csv').decode("utf-8")
df = pd.read_csv(io.StringIO(data))

def load_mummy_data():
    y = df['mummified']
    X = df.drop('mummified', axis=1)
    return X, y

load_mummy_data()
