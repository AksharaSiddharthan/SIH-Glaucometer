import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the cleaned data file
file_name = 'full_dataset_cleaned.csv'
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found. Please ensure it is in the same folder.")
    exit()

# --- Prepare the data for the model ---
# Define the independent variables (features)
# Gender needs to be encoded. We'll use 0 for Male and 1 for Female.
# Assuming 'Gender' column has 'Male' and 'Female' values.
df['Gender_encoded'] = df['Gender'].apply(lambda x: 1 if x == 'Female' else 0)

features = ['Age', 'Gender_encoded', 'Cornea Thickness']
X = df[features]

# Define the dependent variable (target)
y = df['IOP']

# --- Train the regression model ---
model = LinearRegression()
model.fit(X, y)

# --- Get the beta factors (coefficients) ---
beta_coefficients = model.coef_
intercept = model.intercept_

print("Regression Model Results:")
print("--------------------------")
print(f"Intercept (β₀): {intercept:.4f}")
print(f"Beta factor for Age (β₁): {beta_coefficients[0]:.4f}")
print(f"Beta factor for Gender (β₂): {beta_coefficients[1]:.4f}")
print(f"Beta factor for Cornea Thickness (β₃): {beta_coefficients[2]:.4f}")

# The equation of the model is:
# IOP = β₀ + β₁*(Age) + β₂*(Gender) + β₃*(Cornea Thickness)