#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
from datetime import datetime
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        features = obj.getFeaturesList()
        x = np.array(features).reshape(1,30) 

        y_pred =gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        
        # Calculate a suspiciousness score based on URL features
        # Count negative indicators (features with value -1)
        suspicious_features = sum(1 for f in features if f == -1)
        total_features = len(features)
        suspicious_ratio = suspicious_features / total_features
        
        # If more than 40% of features are suspicious, mark as dangerous
        # This catches phishing URLs even when the model is uncertain
        if suspicious_ratio > 0.40:
            # URL has many suspicious characteristics
            xx_value = 0.15  # Very low = dangerous
        elif y_pred == 1:
            # Model says it's safe
            xx_value = y_pro_non_phishing
        else:
            # Model says it's phishing
            xx_value = 0.25  # Low = dangerous
        
        return render_template('index.html', xx =round(xx_value,2), url=url, moment=current_time)
    return render_template("index.html", xx =-1, moment=current_time)


if __name__ == "__main__":
    app.run(debug=True)