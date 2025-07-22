import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('asthma_data.csv')

# Preview data
print("Original Data:")
print(df.head())

# One-hot encode wind_direction
df_encoded = pd.get_dummies(df, columns=['wind_direction'])

# Drop unused columns
df_encoded.drop(columns=['date'], inplace=True)

# Split into features (X) and target (y)
X = df_encoded.drop(columns=['asthma_risk'])
y = df_encoded['asthma_risk']

# Train/test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save split datasets
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("\nPreprocessing Complete. Shapes:")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)
