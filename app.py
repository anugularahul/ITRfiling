import streamlit as st

st.set_page_config(page_title="ITR Suggestion App", layout="centered")
st.title("📄 ITR Form & Plan Suggestion App")

# Input fields
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

salary_income = st.radio("Do you have salary income?", ["Yes", "No"])
salary_above_50 = st.radio("Is your salary income above ₹50 lakh?", ["Yes", "No"])

capital_gains = st.radio("Do you have capital gains (Crypto, FnO, etc)?", ["Yes", "No"])
business_income = st.radio("Do you have business income?", ["Yes", "No"])
freelancer = st.radio("Are you a freelancer?", ["Yes", "No"])
presumptive = st.radio("Are you under presumptive taxation?", ["Yes", "No"])

foreign_assets = st.radio("Do you have foreign income or foreign assets?", ["Yes", "No"])
multi_property = st.radio("Do you own more than one house property?", ["Yes", "No"])
firm_type = st.radio("Are you a partner in a firm (excluding LLP)?", ["Yes", "No"])
company = st.radio("Is your income from a company?", ["Yes", "No"])
trust = st.radio("Is your income from a trust or political party?", ["Yes", "No"])

total_income = st.number_input("Enter your total income (in ₹)", min_value=0, step=1000)

# Suggest ITR and Plan
def suggest_itr_and_plan():
    # ITR Form Logic
    if trust == "Yes":
        itr_form = "ITR-7"
    elif company == "Yes":
        itr_form = "ITR-6"
    elif firm_type == "Yes":
        itr_form = "ITR-5"
    elif business_income == "Yes" or freelancer == "Yes":
        if presumptive == "Yes" and total_income <= 5000000:
            itr_form = "ITR-4 (Sugam)"
        else:
            itr_form = "ITR-3"
    elif capital_gains == "Yes" or foreign_assets == "Yes" or multi_property == "Yes":
        itr_form = "ITR-2"
    elif salary_income == "Yes":
        if salary_above_50 == "Yes":
            itr_form = "ITR-2"
        elif salary_above_50 == "No" and multi_property == "No":
            itr_form = "ITR-1 (Sahaj)"
        else:
            itr_form = "ITR-2"
    else:
        itr_form = "More details needed."

    # Plan Logic
    if itr_form in ["ITR-5", "ITR-6", "ITR-7"]:
        plan = "Assisted Filing Luxury"
    elif total_income > 5000000 or foreign_assets == "Yes" or business_income == "Yes" or freelancer == "Yes":
        plan = "Assisted Filing Black"
    elif salary_income == "Yes" and total_income <= 5000000:
        plan = "Assisted Filing Premium"
    elif capital_gains == "Yes" or multi_property == "Yes":
        plan = "Assisted Filing Basic"
    else:
        plan = "Assisted Filing Basic"

    return itr_form, plan

# Submit Button
if st.button("📤 Submit & Get Suggestion"):
    if name and email and phone:
        itr_form, filing_plan = suggest_itr_and_plan()

        st.success(f"✅ You should file: **{itr_form}**")
        st.info(f"📦 Recommended Plan: **{filing_plan}**")
    else:
        st.error("❗ Please enter Name, Email, and Phone.")
