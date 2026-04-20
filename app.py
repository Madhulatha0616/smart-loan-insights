import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Loan Insights", layout="centered")

st.title("💰 Smart Loan Insights System")
st.write("Advanced Loan Eligibility & Risk Analysis Dashboard")

# ---------------- INPUT ----------------
salary = st.number_input("Enter Monthly Salary (₹)", min_value=0)
loan_amount = st.number_input("Enter Loan Amount Required (₹)", min_value=0)

job = st.selectbox(
    "Select Your Work Field",
    ["IT / Software", "Government Job", "Business", "Daily Labourer", "Student", "Others"]
)

credit_score = st.slider("Enter Credit Score", 300, 900, 650)

tenure_years = st.selectbox("Select Loan Tenure (Years)", [1, 3, 5, 10])

# ---------------- LOGIC ----------------
def get_multiplier(job):
    return {
        "IT / Software": 20,
        "Government Job": 25,
        "Business": 15,
        "Daily Labourer": 8,
        "Student": 5,
        "Others": 10
    }[job]

def get_interest_rate(score):
    if score >= 750:
        return 0.07
    elif score >= 650:
        return 0.08
    elif score >= 550:
        return 0.10
    else:
        return 0.13

# ---------------- BUTTON ----------------
if st.button("Check Eligibility"):

    if salary == 0:
        st.warning("⚠️ Please enter salary")

    else:
        multiplier = get_multiplier(job)
        interest_rate = get_interest_rate(credit_score)

        annual_salary = salary * 12
        eligible_loan = annual_salary * (multiplier / 10)

        tenure = tenure_years * 12
        monthly_rate = interest_rate / 12

        # EMI
        if loan_amount > 0:
            emi = (loan_amount * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)
        else:
            emi = 0

        # EMI affordability
        max_emi = salary * 0.4

        st.subheader("📊 Results")
        st.write(f"💼 Job: {job}")
        st.write(f"💰 Annual Salary: ₹{annual_salary}")
        st.write(f"🏦 Eligible Loan: ₹{int(eligible_loan)}")
        st.write(f"📈 Credit Score: {credit_score}")
        st.write(f"📊 Interest Rate: {interest_rate*100}%")

        # Risk
        if credit_score >= 750:
            risk = "Low"
        elif credit_score >= 650:
            risk = "Medium"
        elif credit_score >= 550:
            risk = "High"
        else:
            risk = "Very High"

        st.write(f"⚠️ Risk Level: {risk}")

        # Approval
        if credit_score < 550:
            decision = "Rejected"
            st.error("❌ Rejected (Low Credit Score)")
        elif loan_amount > eligible_loan:
            decision = "Rejected"
            st.error("❌ Rejected (Exceeds Eligibility)")
        elif emi > max_emi:
            decision = "Rejected"
            st.error("❌ Rejected (EMI too high)")
        else:
            decision = "Approved"
            st.success("✅ Loan Approved")

        # EMI display
        st.subheader("📅 EMI Details")
        st.write(f"Monthly EMI: ₹{int(emi)}")
        st.write(f"Max Affordable EMI: ₹{int(max_emi)}")

        # ================= BAR CHART =================
        st.subheader("📊 Financial Comparison")

        df = pd.DataFrame({
            "Category": ["Annual Salary", "Requested Loan", "Eligible Loan"],
            "Amount": [annual_salary, loan_amount, eligible_loan]
        })

        fig, ax = plt.subplots()
        ax.bar(df["Category"], df["Amount"])
        st.pyplot(fig)

        # ================= PIE CHART =================
        st.subheader("🥧 Loan Distribution")

        remaining = max(eligible_loan - loan_amount, 0)

        fig2, ax2 = plt.subplots()
        ax2.pie([loan_amount, remaining], labels=["Used Loan", "Remaining"], autopct='%1.1f%%')
        st.pyplot(fig2)

        # ================= EXTRA INSIGHTS =================
        st.subheader("📌 Insights")

        usage_percent = (loan_amount / eligible_loan) * 100 if eligible_loan > 0 else 0
        st.write(f"📊 Loan Usage: {usage_percent:.2f}% of eligibility")

        # ================= DOWNLOAD REPORT =================
        report = f"""
        Loan Report
        --------------------
        Job: {job}
        Salary: ₹{salary}
        Loan Requested: ₹{loan_amount}
        Eligible Loan: ₹{int(eligible_loan)}
        Credit Score: {credit_score}
        Interest Rate: {interest_rate*100}%
        EMI: ₹{int(emi)}
        Decision: {decision}
        """

        st.download_button("📥 Download Report", report)