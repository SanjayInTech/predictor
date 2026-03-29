import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
data = pd.read_csv("dataset.csv")

# Input features
X = data[['Demand','CompetitorPrice','Season']]

# Output value
y = data['FinalPrice']

# Create model
model = LinearRegression()

# Train model
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("Model trained successfully")
