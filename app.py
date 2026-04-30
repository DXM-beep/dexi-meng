import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load model
model = pickle.load(open('my_model_DStree_Dexi.pkl', 'rb'))

st.set_page_config(page_title="Loan Approval Predictor", page_icon="💰", layout="centered")

st.title('💰 Loan Approval Predictor')
st.write('Enter applicant details below to predict loan approval.')

# Input fields
col1, col2 = st.columns(2)

with col1:
    fico = st.number_input('FICO Score', min_value=300, max_value=850, value=650)
    income = st.number_input('Monthly Gross Income ($)', min_value=0, value=5000)
    housing = st.number_input('Monthly Housing Payment ($)', min_value=0, value=1000)
    loan_amount = st.number_input('Granted Loan Amount ($)', min_value=0, value=50000)
    requested = st.number_input('Requested Loan Amount ($)', min_value=0, value=55000)

with col2:
    reason = st.selectbox('Loan Reason', ['cover_an_unexpected_cost', 'credit_card_refinancing', 'home_improvement', 'debt_consolidation', 'major_purchase', 'other'])
    employment = st.selectbox('Employment Status', ['full_time', 'part_time', 'self_employed'])
    sector = st.selectbox('Employment Sector', ['information_technology', 'consumer_discretionary', 'energy', 'healthcare', 'financials', 'industrials', 'materials', 'real_estate', 'utilities', 'communication_services', 'consumer_staples'])
    lender = st.selectbox('Lender', ['A', 'B', 'C'])
    bankrupt = st.selectbox('Ever Bankrupt or Foreclose', [0, 1])
    fico_group = st.selectbox('FICO Score Group', ['poor', 'fair', 'good', 'very_good', 'excellent'])

# Predict
if st.button('🔍 Predict Loan Approval'):
    input_data = pd.DataFrame({
        'Reason': [reason],
        'Granted_Loan_Amount': [loan_amount],
        'Requested_Loan_Amount': [requested],
        'FICO_score': [fico],
        'Fico_Score_group': [fico_group],
        'Employment_Status': [employment],
        'Employment_Sector': [sector],
        'Monthly_Gross_Income': [income],
        'Monthly_Housing_Payment': [housing],
        'Ever_Bankrupt_or_Foreclose': [bankrupt],
        'Lender': [lender]
    })

    le = LabelEncoder()
    for col in input_data.select_dtypes(include='object').columns:
        input_data[col] = le.fit_transform(input_data[col])

    prediction = model.predict(input_data)[0]

    st.markdown("---")
    if prediction == 1:
        st.success('✅ Loan Approved!')
    else:
        st.error('❌ Loan Denied')
