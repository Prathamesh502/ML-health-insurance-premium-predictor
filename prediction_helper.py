import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler

# Paths to artifacts
model_rest_path = "artifacts/model_rest.joblib"
model_young_path = "artifacts/model_young.joblib"
scaler_rest_path = "artifacts/scaler_rest3.joblib"
scaler_young_path = "artifacts/scaler_young3.joblib"

# Load models and scalers
model_rest = load(model_rest_path)
model_young = load(model_young_path)
scaler_rest = load(scaler_rest_path)
scaler_young = load(scaler_young_path)

def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    # Split the medical history into potential two parts and convert to lowercase
    diseases = medical_history.lower().split(" & ")

    # Calculate the total risk score by summing the risk scores for each part
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)  # Default to 0 if disease not found

    max_score = 14  # risk score for heart disease (8) + second max risk score (6) for diabetes or high blood pressure
    min_score = 0  # Since the minimum score is always 0

    # Normalize the total risk score
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)

    return normalized_risk_score

def preprocess_input(input_dict):
    # Define the expected feature names
    expected_columns = [
        'age', 'number_of_dependants', 'income_level', 'income_lakhs', 'insurance_plan', 'genetical_risk',
        'normalized_health_risk_score', 'gender_Male', 'marital_status_Unmarried', 'region_Northwest',
        'region_Southeast', 'region_Southwest', 'bmi_category_Obesity', 'bmi_category_Overweight',
        'bmi_category_Underweight', 'employment_status_Salaried', 'employment_status_Self-Employed',
        'smoking_status_Occasional', 'smoking_status_Regular'
    ]

    # Initialize an empty DataFrame with the expected features and set default values to 0
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    # Encoding mappings
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}

    # Process the input dictionary and populate the DataFrame
    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'Age':
            df['age'] = value
        elif key == 'Number of Dependants':
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':
            df['income_lakhs'] = value
        elif key == 'Genetical Risk':
            df['genetical_risk'] = value
        elif key == 'Income Level':
            df['income_level'] = value

    # Handle normalized health risk score
    if 'Medical History' in input_dict:
        df['normalized_health_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    else:
        df['normalized_health_risk_score'] = 0  # Default value

    # Perform scaling
    df = handle_scaling(input_dict.get('Age', 0), df)  # Use a default value if Age is not provided

    return df

def handle_scaling(age, df):
    # Determine the scaler based on age
    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    # Validate scaler_object
    if not isinstance(scaler_object, dict) or 'cols_to_scale' not in scaler_object or 'scaler' not in scaler_object:
        raise ValueError("Invalid scaler_object structure. Ensure it contains 'cols_to_scale' and 'scaler' keys.")

    # Perform scaling
    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['Age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])