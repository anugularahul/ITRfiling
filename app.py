import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

st.set_page_config(page_title="ITR Suggestion App", layout="centered")

st.title("📄 ITR Form & Plan Suggestion App")

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

def suggest_itr_and_plan():
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

    if total_income > 5000000 or foreign_assets == "Yes" or business_income == "Yes" or freelancer == "Yes":
        plan = "Assisted Filing Black"
    elif capital_gains == "Yes" or multi_property == "Yes":
        plan = "Assisted Filing Premium"
    elif salary_income == "Yes" and total_income <= 5000000:
        plan = "Assisted Filing Basic"
    else:
        plan = "Assisted Filing Premium"

    return itr_form, plan

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", size=14)
        self.cell(200, 10, txt="📋 ITR Suggestion Report", ln=True, align="C")
        self.set_font("DejaVu", size=10)
        self.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True, align="C")
        self.ln(10)

    def body(self, data_dict):
        self.set_font("DejaVu", size=12)
        for key, value in data_dict.items():
            self.cell(0, 10, txt=f"{key}: {value}", ln=True)

# Register Unicode font
def create_pdf(user_data, file_name):
    pdf = PDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.body(user_data)
    pdf.output(file_name)

if st.button("📤 Submit & Get Suggestion"):
    if name and email and phone:
        itr_form, filing_plan = suggest_itr_and_plan()
        st.success(f"✅ You should file: **{itr_form}**")
        st.info(f"📦 Recommended Plan: **{filing_plan}**")

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
            "Trust Income": trust,
            "Total Income": f"₹{total_income:,}",
            "Recommended ITR Form": itr_form,
            "Recommended Plan": filing_plan
        }

        pdf_path = "itr_report.pdf"
        create_pdf(user_data, pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download ITR Report", f, file_name="ITR_Suggestion_Report.pdf")

        os.remove(pdf_path)
    else:
        st.error("❗ Please enter Name, Email, and Phone.")
