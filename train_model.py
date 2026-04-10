import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import os

print('Checking for phishing.csv...')
if os.path.exists('phishing.csv'):
    print('Loading phishing.csv...')
    df = pd.read_csv('phishing.csv')
    print(f'Dataset shape: {df.shape}')
    
    # Assuming the last column is the target variable
    X = df.iloc[:, :-1]  # All columns except the last one
    y = df.iloc[:, -1]   # Last column as target
    
    print(f'Feature matrix shape: {X.shape}')
    print(f'Target vector shape: {y.shape}')
    
    # Train a basic model
    gbc = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gbc.fit(X, y)
    
    # Save the model to pickle folder
    with open('pickle/model.pkl', 'wb') as f:
        pickle.dump(gbc, f)
    
    print('Model created and saved to pickle/model.pkl')
else:
    print('phishing.csv not found')
    
    # Create a dummy model as fallback
    import numpy as np
    from sklearn.dummy import DummyClassifier
    
    # Create a dummy classifier that predicts based on simple heuristics
    class SimplePhishingDetector:
        def predict(self, X):
            # Return a prediction (1 for safe, -1 for phishing)
            # This is a very basic placeholder
            return np.array([1 if x[0] > 0 else -1 for x in X])  # Placeholder logic
        
        def predict_proba(self, X):
            # Return probabilities
            prob_safe = np.array([[0.5, 0.5]] * len(X))  # Placeholder probabilities
            return prob_safe
    
    # Save the dummy model
    with open('pickle/model.pkl', 'wb') as f:
        pickle.dump(SimplePhishingDetector(), f)
    
    print('Created dummy model as phishing.csv was not found')