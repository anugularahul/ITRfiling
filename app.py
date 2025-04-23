import streamlit as st

st.set_page_config(page_title="ITR Suggestion App", layout="centered")
st.title("📄 ITR Form & Plan Suggestion App")

# User Inputs
st.header("👤 Personal & Income Details")

resident_status = st.radio("Are you an NRI (Non-Resident Indian)?", ["Yes", "No"])
esops_held_or_sold = st.radio("Do you hold or have sold ESOPs / RSUs?", ["Yes", "No"])

salary_income = st.radio("Do you have salary income?", ["Yes", "No"])
capital_gains = st.radio("Do you have capital gains (e.g. shares, mutual funds)?", ["Yes", "No"])
fno_trading = st.radio("Have you traded in Futures & Options (F&O)?", ["Yes", "No"])
crypto_income = st.radio("Do you have cryptocurrency income?", ["Yes", "No"])
business_income = st.radio("Do you have business or professional income?", ["Yes", "No"])
foreign_income = st.radio("Do you have foreign income or foreign assets?", ["Yes", "No"])

total_income = st.number_input("Enter your total income (in ₹)", min_value=0, step=1000)

# ITR Suggestion Logic
def suggest_itr_form():
    if resident_status == "Yes":
        return "ITR-2 or ITR-3 (based on other sources)"
    elif business_income == "Yes":
        return "ITR-3"
    elif fno_trading == "Yes":
        return "ITR-3"
    elif crypto_income == "Yes" or capital_gains == "Yes":
        return "ITR-2"
    elif salary_income == "Yes":
        return "ITR-1 or ITR-2"
    else:
        return "More info needed"

# Plan Suggestion Logic
def suggest_plan():
    if resident_status == "Yes":
        return "Black"
    if foreign_income == "Yes":
        return "Black"
    if esops_held_or_sold == "Yes":
        return "Black"
    if business_income == "Yes":
        return "Black"
    if fno_trading == "Yes":
        return "Premium"
    if crypto_income == "Yes":
        return "Premium"
    if capital_gains == "Yes":
        return "Premium"
    if salary_income == "Yes" and total_income < 5000000:
        return "Basic"
    if salary_income == "Yes":
        return "Premium"
    return "Premium"

# Submit Button
if st.button("📤 Submit & Get Suggestion"):
    itr_form = suggest_itr_form()
    plan = suggest_plan()

    st.success(f"✅ You should file: **{itr_form}**")
    st.info(f"📦 Recommended Plan: **{plan}**")
