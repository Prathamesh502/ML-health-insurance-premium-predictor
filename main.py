import streamlit as st
from prediction_helper import predict
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Health Insurance Cost Predictor", page_icon="💊", layout="wide")

# Function to load Lottie animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load a Lottie animation (replace URL with any animation you prefer)
lottie_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_z9ed2jna.json")

# Set up the app title and animation
st.title("🌟 Health Insurance Cost Predictor 🌟")
st_lottie(lottie_animation, height=300, key="header_animation")

categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Create input fields
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('🧑 Age', min_value=18, step=1, max_value=100)
with row1[1]:
    number_of_dependants = st.number_input('👨‍👩‍👧 Number of Dependants', min_value=0, step=1, max_value=20)
with row1[2]:
    income_lakhs = st.number_input('💰 Income in Lakhs', step=1, min_value=0, max_value=200)

with row2[0]:
    genetical_risk = st.number_input('🧬 Genetical Risk', step=1, min_value=0, max_value=5)
with row2[1]:
    insurance_plan = st.selectbox('📋 Insurance Plan', categorical_options['Insurance Plan'])
with row2[2]:
    employment_status = st.selectbox('💼 Employment Status', categorical_options['Employment Status'])

with row3[0]:
    gender = st.selectbox('🚹 Gender', categorical_options['Gender'])
with row3[1]:
    marital_status = st.selectbox('💍 Marital Status', categorical_options['Marital Status'])
with row3[2]:
    bmi_category = st.selectbox('📊 BMI Category', categorical_options['BMI Category'])

with row4[0]:
    smoking_status = st.selectbox('🚬 Smoking Status', categorical_options['Smoking Status'])
with row4[1]:
    region = st.selectbox('📍 Region', categorical_options['Region'])
with row4[2]:
    medical_history = st.selectbox('🏥 Medical History', categorical_options['Medical History'])

# Create a dictionary for input values
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# Add a prediction button with a spinner
if st.button('🔮 Predict Cost'):
    with st.spinner("Calculating... Please wait! 🚀"):
        prediction = predict(input_dict)

        st.markdown(
            f'<h1 style="text-align:center; color:orange;">🎉 Predicted Health Insurance Cost: ₹{prediction:.2f}</h1>',
            unsafe_allow_html=True)
    st.balloons()


