import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="ITR Selector", layout="centered")
st.title("📄 ITR Form Selector")
st.write("Answer the questions below to get a suggestion on which ITR form you should file.")

# --- Input Fields ---
resident = st.radio("Are you a Resident Indian?", ["Yes", "No"])
salary_income = st.radio("Do you have Salary Income?", ["Yes", "No"])
business_income = st.radio("Do you have Business or Professional Income?", ["Yes", "No"])
presumptive_scheme = st.radio("Are you using Presumptive Income Scheme (44AD/44ADA/44AE)?", ["Yes", "No"])
capital_gains = st.radio("Do you have Capital Gains?", ["Yes", "No"])
foreign_assets = st.radio("Do you have Foreign Assets or Foreign Income?", ["Yes", "No"])
multiple_properties = st.radio("Do you own more than one house property?", ["Yes", "No"])
total_income = st.number_input("Enter your total income (in ₹):", min_value=0)

# --- Logic Function ---
def suggest_itr(resident, salary_income, business_income, presumptive_scheme,
                capital_gains, foreign_assets, multiple_properties, total_income):

    if resident == "No":
        return "ITR-2"

    if business_income == "Yes":
        if presumptive_scheme == "Yes" and total_income <= 5000000:
            return "ITR-4 (Sugam)"
        else:
            return "ITR-3"

    if capital_gains == "Yes" or foreign_assets == "Yes" or multiple_properties == "Yes":
        return "ITR-2"

    if salary_income == "Yes" and total_income <= 5000000 and multiple_properties == "No":
        return "ITR-1 (Sahaj)"

    return "More details needed to determine the right ITR."

# --- PDF Export Function ---
def create_pdf(data, suggestion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="ITR Suggestion Summary", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Suggested ITR Form: {suggestion}", ln=True)

    filename = f"itr_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- Result Button ---
if st.button("Suggest ITR Form"):
    suggestion = suggest_itr(resident, salary_income, business_income, presumptive_scheme,
                             capital_gains, foreign_assets, multiple_properties, total_income)
    
    st.success(f"✅ Based on your inputs, you should file: **{suggestion}**")

    # --- Summary Dictionary ---
    user_data = {
        "Resident Indian": resident,
        "Salary Income": salary_income,
        "Business Income": business_income,
        "Presumptive Scheme": presumptive_scheme,
        "Capital Gains": capital_gains,
        "Foreign Assets/Income": foreign_assets,
        "Owns Multiple Properties": multiple_properties,
        "Total Income": f"Rs. {total_income}" 
    }

    # --- PDF Creation ---
    filename = create_pdf(user_data, suggestion)

    # --- Download Link ---
    with open(filename, "rb") as file:
        st.download_button(
            label="📥 Download PDF Summary",
            data=file,
            file_name=filename,
            mime="application/pdf"
        )
