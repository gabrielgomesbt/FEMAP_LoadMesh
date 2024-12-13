import numpy as np
import pandas as pd

data = {'Nome': ['João', 'Maria', 'José'], 'Idade': [25, 30, 22]}


L = []
for i in range(10):

    df = pd.DataFrame(data)
    df.attrs['title'] = f"Título do DataFrame {i}"
    L.append(df)

for dataframe in L:
    print(dataframe.attrs['title'])
    print("--------------------")
