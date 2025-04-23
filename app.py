import streamlit as st

st.set_page_config(page_title="ITR Suggestion App", layout="centered")
st.title("📄 ITR Form & Plan Suggestion App")

# User Inputs
salary_income = st.radio("Do you have salary income?", ["Yes", "No"])
salary_above_50 = st.radio("Is your salary income above ₹50 lakh?", ["Yes", "No"])

capital_gains = st.radio("Do you have capital gains (Crypto, FnO, etc)?", ["Yes", "No"])
business_income = st.radio("Do you have business income?", ["Yes", "No"])
presumptive = st.radio("Are you under presumptive taxation?", ["Yes", "No"])

foreign_assets = st.radio("Do you have foreign income or foreign assets?", ["Yes", "No"])
multi_property = st.radio("Do you own more than one house property?", ["Yes", "No"])
firm_type = st.radio("Are you a partner in a firm (excluding LLP)?", ["Yes", "No"])
company = st.radio("Is your income from a company?", ["Yes", "No"])
trust = st.radio("Is your income from a trust or political party?", ["Yes", "No"])

nri_status = st.radio("Are you an NRI?", ["Yes", "No"])
esops_or_rsus = st.radio("Do you hold or have sold ESOPs or RSUs?", ["Yes", "No"])

total_income = st.number_input("Enter your total income (in ₹)", min_value=0, step=1000)

# Logic Functions
def suggest_itr_form():
    if trust == "Yes":
        return "ITR-7"
    elif company == "Yes":
        return "ITR-6"
    elif firm_type == "Yes":
        return "ITR-5"
    elif business_income == "Yes":
        if presumptive == "Yes" and total_income <= 5000000:
            return "ITR-4 (Sugam)"
        else:
            return "ITR-3"
    elif capital_gains == "Yes" or foreign_assets == "Yes" or multi_property == "Yes":
        return "ITR-2"
    elif salary_income == "Yes":
        if salary_above_50 == "Yes":
            return "ITR-2"
        elif multi_property == "No":
            return "ITR-1 (Sahaj)"
        else:
            return "ITR-2"
    else:
        return "More details needed."

def suggest_plan(itr_form):
    # Black Plan
    if nri_status == "Yes" or esops_or_rsus == "Yes" or foreign_assets == "Yes" or (business_income == "Yes" and presumptive == "No"):
        return "Black"

    # Premium Plan
    if capital_gains == "Yes" or business_income == "Yes" or salary_above_50 == "Yes" or multi_property == "Yes":
        return "Premium"

    # Basic Plan
    if salary_income == "Yes" and salary_above_50 == "No" and multi_property == "No" and business_income == "No":
        return "Basic"

    # Default fallback
    return "Premium"

# Submit Button
if st.button("📤 Submit & Get Suggestion"):
    itr_form = suggest_itr_form()
    plan = suggest_plan(itr_form)

    st.success(f"✅ You should file: **{itr_form}**")
    st.info(f"📦 Recommended Plan: **{plan}**")
