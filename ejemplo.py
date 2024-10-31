import pandas as pd
import numpy as np
import sklearn 

# Crear un DataFrame con dos características
data = {
    'Feature1': np.random.randint(1, 100, 10),  # valores entre 1 y 100
    'Feature2': np.random.randint(1000, 10000, 10)  # valores entre 1000 y 10000
}

df = pd.DataFrame(data)
print("Datos originales:")
print(df)

# Crear el normalizador Min-Max
scaler_min_max = MinMaxScaler()

# Aplicar la normalización
df_min_max = pd.DataFrame(scaler_min_max.fit_transform(df), columns=df.columns)
print("\nDatos normalizados con Min-Max:")
print(df_min_max)