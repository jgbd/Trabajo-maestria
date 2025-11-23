from app.database import get_db
from app.services import resultado
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, explained_variance_score, max_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler

import numpy as np

db = next(get_db())

resultados = resultado.get_resultados(db)

df = pd.DataFrame(resultados)

porcentajes_nulos = df.isnull().mean() * 100
# print("Porcentaje de nulos por columna:")
# print(porcentajes_nulos)

# 2. Definir umbrales, por ejemplo:
umbral_eliminar = 70  # eliminar columnas con >70% de nulos

# Crear una lista de columnas a eliminar
columnas_eliminar = porcentajes_nulos[porcentajes_nulos > umbral_eliminar].index.tolist()
# print("Columnas a eliminar:", columnas_eliminar)

# Eliminar esas columnas
df = df.drop(columns=columnas_eliminar)

# Ahora, para las columnas numéricas restantes (por ejemplo, resultados que se puedan imputar):
numerical_columns = [col for col in df.columns if 'resultado' in col.lower()]

categorical_columns = [col for col in df.columns if 'diagnostico' in col.lower()]

df.drop(columns=categorical_columns, inplace=True)
df.drop(columns=['nivel_Riesgo'], inplace=True)

for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['IRCA'] = pd.to_numeric(df['IRCA'], errors='coerce')

imputer_num = SimpleImputer(strategy="median")
df[numerical_columns] = imputer_num.fit_transform(df[numerical_columns])



# Dividir los datos en características (X) y objetivo (y)
X = df.drop(columns=['IRCA'], axis=1)
y = df['IRCA']

# normalizar las columnas numéricas
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = scaler.fit_transform(y.values.reshape(-1, 1)).flatten()

print (X.shape, y.shape)

# Dividir en conjuntos de entrenamiento y prueba/validacion
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = MLPRegressor(hidden_layer_sizes=(16,), 
                     activation='relu', 
                     solver='adam', 
                     learning_rate='adaptive', 
                     learning_rate_init=0.001,
                     max_iter=1000, 
                     random_state=42, 
                     validation_fraction=0.1, 
                     n_iter_no_change=20, 
                     verbose=True)

model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
evs = explained_variance_score(y_test, y_pred)
max_err = max_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
print(f"Mean Absolute Error: {mae}")
print(f"Explained Variance Score: {evs}")
print(f"Max Error: {max_err}")
print(f"Mean Absolute Percentage Error: {mape}")

