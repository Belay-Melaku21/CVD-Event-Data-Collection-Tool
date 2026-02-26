import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- APP CONFIG & SECURITY ---
st.set_page_config(page_title="CVD Research Portal", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("🔐 Research Data Portal")
    u = st.text_input("Investigator Name")
    p = st.text_input("Access Key", type="password")
    if st.button("Login"):
        if u == "Belay Melaku" and p == "@Belay6669":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Access Denied.")

if not st.session_state.auth:
    login()
    st.stop()

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORM INTERFACE ---
st.title("CVD Event Data Abstraction")
st.caption("Mehal Amhara Saynt District Research Project")

with st.form("cvd_research_form", clear_on_submit=True):
    # SECTION 1 & 2: ADMIN
    st.header("1. Administration & Eligibility")
    col1, col2, col3 = st.columns(3)
    with col1:
        s_id = st.text_input("1.1 Study ID*")
        fac = st.selectbox("1.2 Facility", ["Densa", "Kotet", "Work-Mawcha", "Ahyo", "Atrons"])
    with col2:
        mrn = st.text_input("1.3 Patient MRN*")
        cohort = st.selectbox("1.4 Cohort", ["1=Exposed", "2=Unexposed"])
    with col3:
        d_enroll = st.text_input("1.5 Enrollment Date (E.C.)", placeholder="DD/MM/YYYY")
        d_end = st.text_input("1.6 Study End Date (E.C.)", value="30/10/2018")

    # SECTION 3 & 4: SOCIO-DEMOGRAPHICS & LIFESTYLE
    st.divider()
    st.header("2. Demographics & Lifestyle")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("3.3 Age (years)", min_value=0)
        sex = st.selectbox("3.4 Sex", ["1=Male", "2=Female"])
        occ = st.selectbox("3.7 Occupation", ["Gov Employee", "Merchant", "Farmer", "Unemployed", "Other"])
        occ_other = st.text_input("If Other, specify:") if occ == "Other" else "NA"
    with c2:
        alc = st.selectbox("4.2 Alcohol Consumption", ["1=Non-user", "2=Current User"])
        # Branching Logic for Alcohol
        alc_qty = st.text_input("Average drinks/day (if user)") if "Current User" in alc else "0"
        smoke = st.selectbox("4.1 Tobacco", ["1=Never", "2=Current", "3=Previous"])

    # SECTION 5: BMI CALCULATION
    st.divider()
    st.header("3. Clinical Measurements")
    m1, m2 = st.columns(2)
    with m1:
        weight = st.number_input("Weight (kg)", min_value=0.0)
        height = st.number_input("Height (cm)", min_value=0.0)
        
        # Automatic BMI logic
        bmi_val = 0.0
        bmi_cat = "NA"
        if weight > 0 and height > 0:
            bmi_val = round(weight / ((height/100)**2), 2)
            if bmi_val < 18.5: bmi_cat = "Underweight"
            elif 18.5 <= bmi_val < 25: bmi_cat = "Normal"
            elif 25 <= bmi_val < 30: bmi_cat = "Overweight"
            else: bmi_cat = "Obese"
        st.metric("Calculated BMI", f"{bmi_val}", f"Category: {bmi_cat}")

    with m2:
        sbp = st.number_input("Baseline SBP", min_value=0)
        dbp = st.number_input("Baseline DBP", min_value=0)
        chol = st.text_input("Total Cholesterol (if available)", value="NA")

    # SECTION 8: OUTCOME (SURVIVAL DATA)
    st.divider()
    st.header("4. Outcome & Survival Data")
    o1, o2 = st.columns(2)
    with o1:
        event = st.selectbox("8.1 CVD Event Occurred?", ["2=No", "1=Yes"])
        event_type = st.selectbox("8.2 Type", ["Stroke", "MI", "Heart Failure"]) if "Yes" in event else "NA"
        event_date = st.text_input("8.3 Event Date (E.C.)") if "Yes" in event else "NA"
    with o2:
        censor = st.selectbox("8.4 Censoring", ["Study ended", "Lost to Follow-up", "Death (Non-CVD)"])
        last_date = st.text_input("8.5 Last Follow-up Date (E.C.)")

    submit = st.form_submit_button("🚀 SUBMIT RECORD")

    if submit:
        if not s_id or not mrn:
            st.error("Missing Study ID or MRN!")
        else:
            # Prepare data row matching the 48 headers
            row_data = pd.DataFrame([{
                "Study_ID": s_id, "Facility": fac, "MRN": mrn, "Cohort_Group": cohort,
                "Enrollment_Date_EC": d_enroll, "Followup_End_Date_EC": d_end,
                "Age_Years": age, "Sex": sex, "Occupation": occ, "Occupation_Other": occ_other,
                "Alcohol_Use": alc, "Drinks_Per_Day": alc_qty, "Calculated_BMI": bmi_val,
                "BMI_Category": bmi_cat, "Baseline_SBP": sbp, "Baseline_DBP": dbp,
                "Total_Cholesterol": chol, "CVD_Event_Occurred": event,
                "CVD_Event_Type": event_type, "CVD_Event_Date": event_date,
                "Censoring_Details": censor, "Last_Followup_Date": last_date,
                "Data_Collector": "Belay Melaku", "Entry_Timestamp": datetime.now(),
                "Form_Status": "Submitted"
            }])
            
            # Connection logic
            existing = conn.read()
            updated = pd.concat([existing, row_data], ignore_index=True)
            conn.update(data=updated)
            st.success("Record Saved to Google Sheets!")
            st.balloons()
