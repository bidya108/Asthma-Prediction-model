import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('asthma_data.csv')
print("Original Data:")
print(df.head())

df = df.dropna()                    #missing values if any
if 'wind_direction' in df.columns:
    df = pd.get_dummies(df, columns=['wind_direction'])

if 'date' in df.columns:                     #Drop non-numeric
    df.drop(columns=['date'], inplace=True)

X = df.drop(columns=['asthma_risk'])                    #then split testing and target
y = df['asthma_risk']
numeric_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()    # Standardizing all the numerical features
scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

X_train, X_test, y_train, y_test = train_test_split(             #spliting
    X, y, test_size=0.2, random_state=42, stratify=y)

X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("\n Preprocessing Complete. Shapes:")
print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)
