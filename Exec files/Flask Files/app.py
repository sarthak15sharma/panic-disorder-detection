from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the label encodings and the trained model
le = pickle.load(open('label_encoding.pkl', 'rb'))
print("Label encodings loaded successfully.")

model = pickle.load(open('gradient.pkl', 'rb'))
print("Model loaded successfully.")

@app.route('/')
def input():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    Psychatric_History = request.form.get("Psychatric_History")
    Lifestyle_Factors = request.form.get("Lifestyle_Factors")
    Social_Support = request.form.get("Social_Support")
    Substance_Use = request.form.get("Substance_Use")
    Personal_History = request.form.get("Personal_History")
    Medical_History = request.form.get("Medical_History")
    Severity = request.form.get("Severity")
    Coping_Mechanisms = request.form.get("Coping_Mechanisms")
    Current_Stressors = request.form.get("Current_Stressors")
    Demographics = request.form.get("Demographics")
    Family_History = request.form.get("Family_History")
    Gender = request.form.get("Gender")
    Impact_on_Life = request.form.get("Impact_on_Life")
    Symptoms = request.form.get("Symptoms")

    # Print form data for debugging
    print(f"Form data received: {Coping_Mechanisms}, {Current_Stressors}, {Demographics}, {Family_History}, {Gender}, {Impact_on_Life}, {Symptoms}")

    # Create a dictionary of the form data
    form_data = {
        'Psychiatric History': Psychatric_History,
        'Lifestyle Factors': Lifestyle_Factors,
        'Social Support': Social_Support,
        'Substance Use': Substance_Use,
        'Personal History': Personal_History,
        'Medical History': Medical_History,
        'Severity': Severity,
        'Coping Mechanisms': Coping_Mechanisms,
        'Current Stressors': Current_Stressors,
        'Demographics': Demographics,
        'Family History': Family_History,
        'Gender': Gender,
        'Impact on Life': Impact_on_Life,
        'Symptoms': Symptoms
    }

    # Ensure the form_data keys match the training data feature names
    feature_order = [
        'Psychiatric History', 'Lifestyle Factors', 'Social Support', 
        'Substance Use', 'Personal History', 'Medical History', 'Severity', 
        'Coping Mechanisms', 'Current Stressors', 'Demographics', 
        'Family History', 'Gender', 'Impact on Life', 'Symptoms'
    ]

    # Encode form data using the label encodings
    encoded_data = []
    for feature in feature_order:
        value = form_data[feature]
        if feature in le and value in le[feature]:
            encoded_data.append(le[feature][value])
        else:
            encoded_data.append(-1)  # Handle unknown values

    # Convert to numpy array and reshape to 2D array
    encoded_data = np.array(encoded_data).reshape(1, -1)
    
    # Print encoded data for debugging
    print(f"Encoded data: {encoded_data}")

    # Make prediction
    prediction = model.predict(encoded_data)
    # Print prediction and prediction probabilities for debugging
    print(f"Model prediction: {prediction}")

    # Interpret the prediction
    result1 = 'User has panic attack symptoms.'
    if prediction[0] == 1:
        result2 = 'Do not worry, we are here to help!'
    else:
        result1 = 'Hurray !'
        result2= " User does not have panic attack symptoms"

    
    return render_template('inner-page.html', p1=result1,p2=result2)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
