import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open('my_model_DStree_Dexi.pkl', 'rb'))

st.set_page_config(page_title="Loan Approval Predictor", page_icon="💰", layout="centered")

st.title('💰 Loan Approval Predictor')
st.write('Enter applicant details below to predict loan approval.')

col1, col2 = st.columns(2)

with col1:
    fico = st.number_input('FICO Score', min_value=300, max_value=850, value=650)
    income = st.number_input('Monthly Gross Income ($)', min_value=0, value=5000)
    housing = st.number_input('Monthly Housing Payment ($)', min_value=0, value=1000)
    loan_amount = st.number_input('Loan Amount ($)', min_value=0, value=50000)

# Auto-assign FICO group
if fico >= 800:
    fico_group = 'excellent'
elif fico >= 740:
    fico_group = 'very_good'
elif fico >= 670:
    fico_group = 'good'
elif fico >= 580:
    fico_group = 'fair'
else:
    fico_group = 'poor'

with col2:
    st.text_input('FICO Score Group (auto)', value=fico_group, disabled=True)
    reason = st.selectbox('Loan Reason', ['cover_an_unexpected_cost', 'credit_card_refinancing', 'home_improvement', 'debt_consolidation', 'major_purchase', 'other'])
    employment = st.selectbox('Employment Status', ['full_time', 'part_time', 'self_employed'])
    sector = st.selectbox('Employment Sector', ['information_technology', 'consumer_discretionary', 'energy', 'healthcare', 'financials', 'industrials', 'materials', 'real_estate', 'utilities', 'communication_services', 'consumer_staples'])
    lender = st.selectbox('Lender', ['A', 'B', 'C'])

# Encoding maps
reason_map = {'cover_an_unexpected_cost': 0, 'credit_card_refinancing': 1, 'debt_consolidation': 2, 'home_improvement': 3, 'major_purchase': 4, 'other': 5}
employment_map = {'full_time': 0, 'part_time': 1, 'self_employed': 2}
sector_map = {'communication_services': 0, 'consumer_discretionary': 1, 'consumer_staples': 2, 'energy': 3, 'financials': 4, 'healthcare': 5, 'industrials': 6, 'information_technology': 7, 'materials': 8, 'real_estate': 9, 'utilities': 10}
lender_map = {'A': 0, 'B': 1, 'C': 2}
fico_group_map = {'excellent': 0, 'fair': 1, 'good': 2, 'poor': 3, 'very_good': 4}

if st.button('🔍 Predict Loan Approval'):
    input_data = pd.DataFrame({
        'Reason': [reason_map[reason]],
        'Granted_Loan_Amount': [loan_amount],
        'Requested_Loan_Amount': [loan_amount],
        'FICO_score': [fico],
        'Fico_Score_group': [fico_group_map[fico_group]],
        'Employment_Status': [employment_map[employment]],
        'Employment_Sector': [sector_map[sector]],
        'Monthly_Gross_Income': [income],
        'Monthly_Housing_Payment': [housing],
        'Ever_Bankrupt_or_Foreclose': [0],
        'Lender': [lender_map[lender]]
    })

    prediction = model.predict(input_data)[0]

    st.markdown("---")
    if prediction == 1:
        st.success('✅ Loan Approved!')
    else:
        st.error('❌ Loan Denied')
