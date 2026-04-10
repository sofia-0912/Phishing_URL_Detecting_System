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
    
    # Drop the Index column and use the remaining columns
    # The last column is the target ('class'), so features are everything except 'class'
    X = df.drop(['Index', 'class'], axis=1)  # All columns except 'Index' and 'class'
    y = df['class']  # Target column
    
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