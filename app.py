import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="CVD Research Data Abstraction", layout="wide")

# 1. Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("🔐 Investigator Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "Belay Melaku" and pw == "@Belay6669":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Database Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📋 CVD Event Data Abstraction Portal")
st.write("**Study Title:** Time to Cardiovascular Disease Event and Its Determinant Among Hypertensive Patients on Follow-Up at Health Centers in Mehal Amhara Saynt District.")

# Data Collection Form
with st.form("cvd_final_form", clear_on_submit=True):
    
    # --- SECTION 1 & 2: ADMINISTRATIVE & ELIGIBILITY ---
    st.header("Section 1 & 2: Administrative & Eligibility")
    col1, col2 = st.columns(2)
    with col1:
        s_id = st.text_input("1.1 Study ID")
        facility = st.selectbox("1.2 Facility Name", ["1=Densa", "2=Kotet", "3=Work-Mawcha", "4=Ahyo", "5=Atrons"])
        mrn = st.text_input("1.3 Patient MRN")
        cohort = st.selectbox("1.4 Cohort Group", ["1=Exposed (Hypertensive)", "2=Unexposed (Normotensive)"])
    with col2:
        enroll_date = st.text_input("1.5 Date of Enrollment (E.C.)", placeholder="DD/MM/YYYY")
        follow_end_date = st.text_input("1.6 Follow-up End Date (E.C.)", value="30/10/2018")
        age_elig = st.selectbox("2.1 Age ≥18 years?", ["1=Yes", "2=No"])
        pre_cvd = st.selectbox("2.2 Pre-existing CVD (Stroke/MI/HF) before enrolment?", ["2=No", "1=Yes"])
        preg_htn = st.selectbox("2.3 Pregnancy-induced Hypertension?", ["2=No", "1=Yes"])

    # --- SECTION 3: SOCIO-DEMOGRAPHIC ---
    st.header("SECTION 3: SOCIO-DEMOGRAPHIC CHARACTERISTICS")
    col3, col4 = st.columns(2)
    with col3:
        age_yrs = st.number_input("3.3 Age (in years)", min_value=0)
        sex = st.selectbox("3.4 Sex", ["1=Male", "2=Female"])
        residence = st.selectbox("3.5 Residence", ["1=Urban", "2=Rural"])
    with col4:
        edu = st.selectbox("3.6 Educational Status", ["1=No formal education", "2=Primary (1-8)", "3=Secondary (9-12)", "4=Higher"])
        occ = st.selectbox("3.7 Occupational Status", ["1=Government Employee", "2=Merchant/Trader", "3=Farmer", "4=Unemployed", "5=Other"])
        occ_other = st.text_input("3.7.1 If Other Occupation, specify:") if "Other" in occ else "NA"
        marital = st.selectbox("3.8 Marital Status", ["1=Single", "2=Married", "3=Widowed", "4=Divorced/Separated"])

    # --- SECTION 4: LIFESTYLE & BEHAVIORAL ---
    st.header("SECTION 4: LIFESTYLE & BEHAVIORAL FACTORS")
    col5, col6 = st.columns(2)
    with col5:
        tobacco = st.selectbox("4.1 Tobacco Use", ["1=Never Smoker", "2=Current Smoker", "3=Previous Smoker"])
        alcohol = st.selectbox("4.2 Alcohol Consumption", ["1=Non-user", "2=Current User"])
        alc_qty = st.text_input("4.2.1 Average drinks/day (if current user)") if "Current User" in alcohol else "0"
        khat = st.selectbox("4.3 Khat Chewing", ["1=Never", "2=Current User", "3=History of regular use"])
    with col6:
        phys_act = st.selectbox("4.4 Physical Activity (≥30 min/day, 5 days/week)", ["1=Physically Active", "2=Inactive"])
        salt = st.selectbox("4.5 Salt Intake", ["2=Normal/Low", "1=High (Adds salt)"])

    # --- SECTION 5: CLINICAL & PHYSIOLOGICAL ---
    st.header("SECTION 5: CLINICAL & PHYSIOLOGICAL MEASUREMENTS")
    col7, col8 = st.columns(2)
    with col7:
        sbp = st.number_input("5.1 SBP (mmHg)", min_value=0)
        dbp = st.number_input("5.1 DBP (mmHg)", min_value=0)
        htn_stage = st.selectbox("5.2 Hypertension Stage", ["1=Pre-HTN", "2=Stage 1", "3=Stage 2", "4=Stage 3/4"])
        htn_months = st.text_input("5.5 Duration of HTN (months)")
        fam_hx = st.selectbox("5.6 Family History of CVD/HTN", ["2=No", "1=Yes"])
    with col8:
        weight = st.number_input("5.3.1 Weight (kg)", min_value=0.0)
        height = st.number_input("5.3.2 Height (cm)", min_value=0.0)
        
        # BMI Calculation
        bmi_val = 0.0
        bmi_cat = "NA"
        if weight > 0 and height > 0:
            bmi_val = round(weight / ((height/100)**2), 2)
            if bmi_val < 18.5: bmi_cat = "1=Underweight (<18.5)"
            elif 18.5 <= bmi_val < 25: bmi_cat = "2=Normal"
            elif 25 <= bmi_val < 30: bmi_cat = "3=Overweight (25-29.9)"
            else: bmi_cat = "4=Obese (≥30)"
        st.info(f"5.3 BMI: {bmi_val} | 5.4 BMI Category: {bmi_cat}")

    # --- SECTION 6: BIOCHEMICAL & COMORBIDITY ---
    st.header("SECTION 6: BIOCHEMICAL & COMORBIDITY PROFILE")
    col9, col10 = st.columns(2)
    with col9:
        dm = st.selectbox("6.1 Diabetes Mellitus (FBS ≥126 or meds)", ["2=No", "1=Yes"])
        ckd = st.selectbox("6.2 Chronic Kidney Disease (CKD)", ["2=No", "1=Yes"])
        proteinuria = st.selectbox("6.3 Proteinuria", ["2=Negative", "1=Positive"])
    with col10:
        cholesterol = st.text_input("6.4 Total Cholesterol Level (mg/dL)", value="NA")
        baseline_comp = st.selectbox("6.5 Baseline Complications", ["1=None", "2=Prior Stroke", "3=Prior Cardiac issues"])

    # --- SECTION 7: TREATMENT & MANAGEMENT ---
    st.header("SECTION 7: TREATMENT & MANAGEMENT FACTORS")
    col11, col12 = st.columns(2)
    with col11:
        tx_type = st.selectbox("7.1 Type of Antihypertensive Meds", ["1=Monotherapy", "2=Dual Therapy", "3=Polytherapy"])
        tx_class = st.selectbox("7.2 Specific Class", ["1=ACEi/ARB", "2=CCB", "3=Diuretics", "4=Beta-Blockers"])
    with col12:
        adherence = st.selectbox("7.3 Medication Adherence (≥80% intake)", ["1=Good", "2=Poor"])

    # --- SECTION 8: OUTCOME & SURVIVAL ---
    st.header("SECTION 8: OUTCOME & SURVIVAL DATA")
    col13, col14 = st.columns(2)
    with col13:
        cvd_event = st.selectbox("8.1 CVD Event Occurred?", ["2=No", "1=Yes"])
        event_type = st.selectbox("8.2 Type of CVD Event", ["1=Stroke", "2=MI", "3=Heart Failure"]) if "1=Yes" in cvd_event else "NA"
        event_date = st.text_input("8.3 Date of CVD Event (E.C.)") if "1=Yes" in cvd_event else "NA"
    with col14:
        censor_detail = st.selectbox("8.4 Censoring Details", ["1=Lost to Follow-up", "2=Died (Non-CVD cause)", "3=Study ended without event"])
        last_date = st.text_input("8.5 Date of Last Follow-up/Censoring (E.C.)")

    submit = st.form_submit_button("Submit Form")

    if submit:
        # Create Data Dictionary for All Fields
        data_to_save = {
            "Study_ID": s_id, "Facility": facility, "MRN": mrn, "Cohort": cohort, 
            "Enroll_Date": enroll_date, "Follow_End_Date": follow_end_date,
            "Age_Elig": age_elig, "Pre_CVD": pre_cvd, "Preg_HTN": preg_htn,
            "Age": age_yrs, "Sex": sex, "Residence": residence, "Education": edu,
            "Occupation": occ, "Occ_Other": occ_other, "Marital": marital,
            "Tobacco": tobacco, "Alcohol": alcohol, "Alc_Qty": alc_qty, "Khat": khat,
            "Phys_Act": phys_act, "Salt": salt, "SBP": sbp, "DBP": dbp, "HTN_Stage": htn_stage,
            "Weight": weight, "Height": height, "BMI": bmi_val, "BMI_Cat": bmi_cat,
            "HTN_Duration": htn_months, "Fam_Hx": fam_hx, "DM": dm, "CKD": ckd,
            "Proteinuria": proteinuria, "Cholesterol": cholesterol, "Baseline_Comp": baseline_comp,
            "Tx_Type": tx_type, "Tx_Class": tx_class, "Adherence": adherence,
            "CVD_Event": cvd_event, "Event_Type": event_type, "Event_Date": event_date,
            "Censor_Detail": censor_detail, "Last_Date": last_date, "Entry_Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to GSheets
        try:
            df = pd.DataFrame([data_to_save])
            existing = conn.read()
            updated = pd.concat([existing, df], ignore_index=True)
            conn.update(data=updated)
            st.success("✅ መረጃው በትክክል ተመዝግቧል!")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
