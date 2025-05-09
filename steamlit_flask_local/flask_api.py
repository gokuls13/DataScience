from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("F:\DataScience\DataScience\streamlit_local\pipe.pkl")  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({'prediction': abs(round(prediction, 2))})

@app.route('/bulk_predict', methods=['POST'])
def bulk_predict():
    content = request.get_json()
    df = pd.DataFrame(content['data'])
    df['Predicted_Price'] = model.predict(df)
    df['Predicted_Price'] = df['Predicted_Price'].abs().round(2)
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(port=5000)