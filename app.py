import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="ITR Suggestion App", layout="centered")

# Title
st.title("📄 ITR Form & Plan Suggestion App")
st.markdown("Provide your details and get the best ITR form and plan recommendation.")

# Input fields
st.header("🔍 Personal and Financial Information")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

salary_income = st.radio("Do you have salary income?", ["Yes", "No"], key="salary_income")
salary_above_50 = st.radio("Is your salary income above ₹50 lakh?", ["Yes", "No"], key="salary_above_50")

capital_gains = st.radio("Do you have capital gains (Crypto, FnO, etc)?", ["Yes", "No"], key="capital_gains")
business_income = st.radio("Do you have business income?", ["Yes", "No"], key="business_income")
freelancer = st.radio("Are you a freelancer?", ["Yes", "No"], key="freelancer")
presumptive = st.radio("Are you under presumptive taxation?", ["Yes", "No"], key="presumptive")

foreign_assets = st.radio("Do you have foreign income or foreign assets?", ["Yes", "No"], key="foreign_assets")
multi_property = st.radio("Do you own more than one house property?", ["Yes", "No"], key="multi_property")
firm_type = st.radio("Are you a partner in a firm (excluding LLP)?", ["Yes", "No"], key="firm_type")
company = st.radio("Is your income from a company?", ["Yes", "No"], key="company")
trust = st.radio("Is your income from a trust or political party?", ["Yes", "No"], key="trust")

total_income = st.number_input("Enter your total income (in ₹)", min_value=0, step=1000, key="total_income")

# Suggestion logic
def suggest_itr_and_plan():
    if st.session_state.trust == "Yes":
        itr_form = "ITR-7"
    elif st.session_state.company == "Yes":
        itr_form = "ITR-6"
    elif st.session_state.firm_type == "Yes":
        itr_form = "ITR-5"
    elif st.session_state.business_income == "Yes" or st.session_state.freelancer == "Yes":
        if st.session_state.presumptive == "Yes" and st.session_state.total_income <= 5000000:
            itr_form = "ITR-4 (Sugam)"
        else:
            itr_form = "ITR-3"
    elif st.session_state.capital_gains == "Yes" or st.session_state.foreign_assets == "Yes" or st.session_state.multi_property == "Yes":
        itr_form = "ITR-2"
    elif st.session_state.salary_income == "Yes":
        if st.session_state.salary_above_50 == "Yes":
            itr_form = "ITR-2"
        elif st.session_state.salary_above_50 == "No" and st.session_state.multi_property == "No":
            itr_form = "ITR-1 (Sahaj)"
        else:
            itr_form = "ITR-2"
    else:
        itr_form = "More details needed."

    # Filing Plan Suggestion
    income = st.session_state.total_income
    has_capital_gains = st.session_state.capital_gains == "Yes"
    has_foreign_income = st.session_state.foreign_assets == "Yes"
    is_business = st.session_state.business_income == "Yes" or st.session_state.freelancer == "Yes"

    if income > 5000000 or has_foreign_income or is_business:
        plan = "Assisted Filing Black"
    elif has_capital_gains or st.session_state.multi_property == "Yes":
        plan = "Assisted Filing Premium"
    elif st.session_state.salary_income == "Yes" and income <= 5000000:
        plan = "Assisted Filing Basic"
    else:
        plan = "Assisted Filing Premium"

    return itr_form, plan

# Button to process
if st.button("📤 Submit & Get Suggestion"):
    if name and email and phone:
        itr_form, filing_plan = suggest_itr_and_plan()
        st.success(f"✅ Based on your inputs, you should file: **{itr_form}**")
        st.info(f"📦 Recommended ITR Filing Plan: **{filing_plan}**")

        # Collect data for PDF
        user_data = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Salary Income": salary_income,
            "Salary > ₹50L": salary_above_50,
            "Capital Gains": capital_gains,
            "Business Income": business_income,
            "Freelancer": freelancer,
            "Presumptive Taxation": presumptive,
            "Foreign Assets/Income": foreign_assets,
            "Multiple Properties": multi_property,
            "Firm Partner": firm_type,
            "Company Income": company,
            "Trust/Political Income": trust,
            "Total Income": f"₹{total_income:,}",
            "Recommended ITR Form": itr_form,
            "Recommended Plan": filing_plan
        }

        # PDF Generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="ITR Suggestion Report", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=1, align="C")
        pdf.ln(10)

        for key, value in user_data.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=1)

        pdf_output = "itr_suggestion.pdf"
        pdf.output(pdf_output)

        with open(pdf_output, "rb") as f:
            st.download_button("📄 Download Your ITR Suggestion Report", f, file_name="ITR_Suggestion_Report.pdf")

    else:
        st.error("❗ Please fill in all required fields (Name, Email, Phone).")
