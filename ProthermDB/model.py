from helper import read_embedding
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

class Protein:
    def __init__(self):
        self.temp = None
        self.id = None
        self.sequence = None

# Parse dataset
file_path = 'Datasets/Dataset.xlsx' 
df = pd.read_excel(file_path)
proteins = []
for index, row in df.iterrows():
    protein = Protein()
    protein.temp = row['Tm_(C)']
    protein.sequence = row['Sequence']
    protein.id = row['UNIPROT_ID']
    proteins.append(protein)


directory = 'Embeddings'
mse_list = []
models = {}

for layer in range(1, 34):
    xs = []
    ys = []
    
    for p in proteins:
        x = read_embedding(directory, p.id, layer)
        y = p.temp
        xs.append(x)
        ys.append(y)

    xs = np.array(xs)
    ys = np.array(ys)

    X_train, X_test, y_train, y_test = train_test_split(xs, ys, test_size=0.2, random_state=42)
   
    model = LinearRegression()
    model.fit(X_train, y_train)

    models[layer] = model

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)

layers = range(1, 34)

plt.figure(figsize=(14, 6))
plt.subplot(1, 1, 1)
plt.plot(layers, mse_list, marker='o')
plt.xlabel('ESM2 Layer')
plt.ylabel('Mean Squared Error')
plt.title('Sequence Melting Temperatures')
plt.xticks(layers)
plt.tight_layout()
plt.show()