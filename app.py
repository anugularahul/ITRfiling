import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="ITR Selector", layout="centered")

st.title("📄 Income Tax Return (ITR) Form Selector")
st.write("Answer the questions to know which ITR form suits you best.")

# --- Initialize session state for reset ---
if "clear" not in st.session_state:
    st.session_state.clear = False

# --- Clear Form Function ---
def reset_form():
    for key in list(st.session_state.keys()):
        if key != "clear":
            st.session_state[key] = None
    st.session_state.clear = True

# --- Input Questions ---
# --- Input Questions ---
with st.form("itr_form"):
    st.subheader("👤 Personal & Income Information")

    resident = st.radio("Are you a Resident Indian?", ["-- Select --", "Yes", "No"], key="resident")
    salary_income = st.radio("Do you have Salary Income?", ["-- Select --", "Yes", "No"], key="salary_income")
    salary_above_50 = st.radio("Is your Salary above ₹50 lakhs?", ["-- Select --", "Yes", "No", "N/A"], key="salary_above_50")
    business_income = st.radio("Do you have Business or Professional Income?", ["-- Select --", "Yes", "No"], key="business_income")
    freelancer = st.radio("Are you a Freelancer?", ["-- Select --", "Yes", "No"], key="freelancer")
    presumptive_scheme = st.radio("Are you using Presumptive Income Scheme (44AD/44ADA/44AE)?", ["-- Select --", "Yes", "No"], key="presumptive")
    capital_gains = st.radio("Do you have Capital Gains?", ["-- Select --", "Yes", "No"], key="capital_gains")
    foreign_assets = st.radio("Do you have Foreign Assets or Foreign Income?", ["-- Select --", "Yes", "No"], key="foreign_assets")
    multiple_properties = st.radio("Do you own more than one house property?", ["-- Select --", "Yes", "No"], key="multi_property")
    income_from_firm = st.radio("Do you have income as a partner in a firm?", ["-- Select --", "Yes", "No"], key="partner_income")
    firm_type = st.radio("Are you filing for a Partnership Firm / LLP / AOP / BOI?", ["-- Select --", "Yes", "No"], key="firm_type")
    company = st.radio("Are you filing for a company?", ["-- Select --", "Yes", "No"], key="company")
    trust_income = st.radio("Are you filing for a trust, institution, or political party?", ["-- Select --", "Yes", "No"], key="trust")

    total_income = st.number_input("Enter your Total Income (in ₹):", min_value=0, key="total_income")

    submitted = st.form_submit_button("Suggest ITR Form")
    clear_clicked = st.form_submit_button("Clear", on_click=reset_form)


# --- Suggestion Logic ---
def suggest_itr():
    if st.session_state.trust == "Yes":
        return "ITR-7"
    if st.session_state.company == "Yes":
        return "ITR-6"
    if st.session_state.firm_type == "Yes":
        return "ITR-5"
    if st.session_state.business_income == "Yes" or st.session_state.freelancer == "Yes":
        if st.session_state.presumptive == "Yes" and st.session_state.total_income <= 5000000:
            return "ITR-4 (Sugam)"
        return "ITR-3"
    if st.session_state.capital_gains == "Yes" or st.session_state.foreign_assets == "Yes" or st.session_state.multi_property == "Yes":
        return "ITR-2"
    if st.session_state.salary_income == "Yes":
        if st.session_state.salary_above_50 == "Yes":
            return "ITR-2"
        elif st.session_state.salary_above_50 == "No" and st.session_state.multi_property == "No":
            return "ITR-1 (Sahaj)"
    return "More details needed."

# --- PDF Creation Function ---
def create_pdf(data, suggestion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="ITR Suggestion Summary", ln=True, align='C')
    pdf.ln(10)

    for key, value in data.items():
        line = f"{key}: {value}"
        pdf.cell(200, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'), ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Suggested ITR Form: {suggestion}", ln=True)

    filename = f"itr_summary_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- Process Submission ---
if submitted:
    suggestion = suggest_itr()

    st.success(f"✅ Based on your inputs, you should file: **{suggestion}**")

    user_data = {
        "Resident Indian": resident,
        "Salary Income": salary_income,
        "Salary above ₹50L": salary_above_50,
        "Business Income": business_income,
        "Freelancer": freelancer,
        "Presumptive Income": presumptive_scheme,
        "Capital Gains": capital_gains,
        "Foreign Assets/Income": foreign_assets,
        "Multiple Properties": multiple_properties,
        "Income from Firm": income_from_firm,
        "Filing for Firm/LLP": firm_type,
        "Filing for Company": company,
        "Filing for Trust/Institution": trust_income,
        "Total Income": f"₹{total_income}"
    }

    filename = create_pdf(user_data, suggestion)

    with open(filename, "rb") as file:
        st.download_button(
            label="📥 Download PDF Summary",
            data=file,
            file_name=filename,
            mime="application/pdf"
        )
