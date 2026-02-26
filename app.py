import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="CVD Research Portal", layout="wide")

# Authentication
if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("🔐 Investigator Access")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == "Belay Melaku" and p == "@Belay6669":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Incorrect credentials")

if not st.session_state.auth:
    login()
    st.stop()

# Database Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 CVD Event Data Abstraction Portal")
st.markdown("---")

# እያንዳንዱን ሴክሽን ለየብቻ በTabs መክፈል
tabs = st.tabs([
    "Section 1-2: Admin & Eligibility", 
    "Section 3-4: Demographic & Lifestyle", 
    "Section 5: Clinical Measures", 
    "Section 6-7: Profile & Treatment", 
    "Section 8: Outcome & Survival"
])

# ዳታዎችን በሴክሽን ለመሰብሰብ መጀመሪያ ዲክሽነሪ ማዘጋጀት
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- SECTION 1 & 2 ---
with tabs[0]:
    st.subheader("Section 1: Administrative & Eligibility")
    col1, col2 = st.columns(2)
    with col1:
        s_id = st.text_input("1.1. Study ID", key="s_id")
        fac = st.selectbox("1.2. Facility Name", ["1=Densa", "2=Kotet", "3=Work-Mawcha", "4=Ahyo", "5=Atrons"], key="fac")
        mrn = st.text_input("1.3. Patient MRN", key="mrn")
    with col2:
        cohort = st.selectbox("1.4. Cohort Group", ["1=Exposed (Hypertensive)", "2=Unexposed (Normotensive)"], key="cohort")
        d_enroll = st.text_input("1.5. Date of Enrollment (E.C.)", key="d_enroll")
        d_end = st.text_input("1.6. Follow-up End Date (E.C.)", value="30/10/2018", key="d_end")
    
    st.subheader("Section 2: Eligibility Checklist")
    e1, e2, e3 = st.columns(3)
    age_elig = e1.selectbox("2.1. Age ≥18?", ["1=Yes", "2=No"], key="age_elig")
    pre_cvd = e2.selectbox("2.2. Pre-existing CVD?", ["2=No", "1=Yes"], key="pre_cvd")
    preg_htn = e3.selectbox("2.3. Pregnancy-induced HTN?", ["2=No", "1=Yes"], key="preg_htn")

# --- SECTION 3 & 4 ---
with tabs[1]:
    st.header("Section 3: Socio-Demographics")
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("3.1. Age (years)", min_value=0, key="age")
        sex = st.selectbox("3.2. Sex", ["1=Male", "2=Female"], key="sex")
        res = st.selectbox("3.3. Residence", ["1=Urban", "2=Rural"], key="res")
    with col4:
        edu = st.selectbox("3.4. Education", ["1=No formal", "2=Primary", "3=Secondary", "4=Higher"], key="edu")
        occ = st.selectbox("3.5. Occupation", ["1=Gov Employee", "2=Merchant", "3=Farmer", "4=Unemployed", "5=Other"], key="occ")
        occ_oth = st.text_input("3.5.1. Specify Other", key="occ_oth") if "Other" in occ else "NA"
        marital = st.selectbox("3.6. Marital Status", ["1=Single", "2=Married", "3=Widowed", "4=Divorced"], key="marital")
    
    st.header("Section 4: Lifestyle Factors")
    tob = st.selectbox("4.1. Tobacco Use", ["1=Never", "2=Current", "3=Previous"], key="tob")
    alc = st.selectbox("4.2. Alcohol Consumption", ["1=Non-user", "2=Current User"], key="alc")
    alc_qty = st.text_input("4.2.1. Drinks per day", key="alc_qty") if "Current User" in alc else "0"
    khat = st.selectbox("4.3. Khat Chewing", ["1=Never", "2=Current", "3=History"], key="khat")
    phys = st.selectbox("4.4. Physical Activity", ["1=Active", "2=Inactive"], key="phys")
    salt = st.selectbox("4.5. Salt Intake", ["1=High", "2=Normal/Low"], key="salt")

# --- SECTION 5 ---
with tabs[2]:
    st.header("Section 5: Clinical Measurements")
    

[Image of Blood Pressure Measurement Technique]

    sbp = st.number_input("5.1. SBP (mmHg)", min_value=0, key="sbp")
    dbp = st.number_input("5.1. DBP (mmHg)", min_value=0, key="dbp")
    
    # 5.2 HTN Stage Logic
    htn_stage = "NA"
    if sbp >= 180 or dbp >= 110: htn_stage = "4=Stage 3/4"
    elif sbp >= 160 or dbp >= 100: htn_stage = "3=Stage 2"
    elif sbp >= 140 or dbp >= 90: htn_stage = "2=Stage 1"
    elif sbp >= 120 or dbp >= 80: htn_stage = "1=Pre-HTN"
    st.warning(f"5.2. Auto-Calculated HTN Stage: {htn_stage}")

    weight = st.number_input("5.3. Weight (kg)", min_value=0.0, key="weight")
    height = st.number_input("5.3. Height (cm)", min_value=0.0, key="height")
    
    # 5.3 & 5.4 BMI Logic
    

[Image of BMI Classification Chart]

    bmi_val = 0.0; bmi_cat = "NA"
    if weight > 0 and height > 0:
        bmi_val = round(weight / ((height/100)**2), 2)
        if bmi_val < 18.5: bmi_cat = "1=Underweight"
        elif bmi_val < 25: bmi_cat = "2=Normal"
        elif bmi_val < 30: bmi_cat = "3=Overweight"
        else: bmi_cat = "4=Obese"
    st.success(f"5.3. BMI: {bmi_val} | 5.4. Category: {bmi_cat}")
    
    dur_htn = st.text_input("5.5. Duration of HTN (months)", key="dur_htn")
    fam_hx = st.selectbox("5.6. Family History CVD/HTN", ["1=Yes", "2=No"], key="fam_hx")

# --- SECTION 6 & 7 ---
with tabs[3]:
    st.header("Section 6: Biochemical Profile")
    dm = st.selectbox("6.1. DM", ["1=Yes", "2=No"], key="dm")
    ckd = st.selectbox("6.2. CKD", ["1=Yes", "2=No"], key="ckd")
    prot = st.selectbox("6.3. Proteinuria", ["1=Positive", "2=Negative"], key="prot")
    chol = st.text_input("6.4. Cholesterol", key="chol")
    comp = st.selectbox("6.5. Baseline Complications", ["1=None", "2=Prior Stroke", "3=Prior Cardiac"], key="comp")
    
    st.header("Section 7: Treatment Factors")
    tx_type = st.selectbox("7.1. Meds Type", ["1=Monotherapy", "2=Dual", "3=Polytherapy"], key="tx_type")
    tx_class = st.multiselect("7.2. Specific Class", ["1=ACEi/ARB", "2=CCB", "3=Diuretics", "4=Beta-Blockers"], key="tx_class")
    adh = st.selectbox("7.3. Adherence", ["1=Good", "2=Poor"], key="adh")

# --- SECTION 8 ---
with tabs[4]:
    st.header("Section 8: Outcome & Survival")
    ev = st.selectbox("8.1. CVD Event?", ["2=No", "1=Yes"], key="ev")
    ev_type = st.selectbox("8.2. Event Type", ["1=Stroke", "2=MI", "3=Heart Failure"], key="ev_type") if "Yes" in ev else "NA"
    ev_date = st.text_input("8.3. Event Date", key="ev_date") if "Yes" in ev else "NA"
    
    censor = st.selectbox("8.4. Censoring Details", ["1=Not Censored", "2=Lost to Follow-up", "3=Died (Non-CVD)", "4=Study ended"], key="censor")
    censor_date = st.text_input("8.5. Last Date", key="censor_date") if censor != "1=Not Censored" else "NA"

    st.markdown("---")
    if st.button("🚀 SUBMIT COMPLETE RECORD"):
        if not s_id or not mrn:
            st.error("Please fill Study ID and MRN before submitting!")
        else:
            df = pd.DataFrame([{
                "Study_ID": s_id, "Facility_Name": fac, "Patient_MRN": mrn, "Cohort_Group": cohort,
                "Enrollment_Date_EC": d_enroll, "Followup_End_Date_EC": d_end, "Age_Eligible_2_1": age_elig,
                "Preexisting_CVD_2_2": pre_cvd, "Pregnancy_HTN_2_3": preg_htn, "Age_3_1": age, "Sex_3_2": sex,
                "Residence_3_3": res, "Educational_Status_3_4": edu, "Occupational_Status_3_5": occ,
                "Occupation_Other_Detail": occ_oth, "Marital_Status_3_6": marital, "Tobacco_Use_4_1": tob,
                "Alcohol_Consumption_4_2": alc, "Alcohol_Drinks_Per_Day": alc_qty, "Khat_Chewing_4_3": khat,
                "Physical_Activity_4_4": phys, "Salt_Intake_4_5": salt, "Baseline_SBP_5_1": sbp,
                "Baseline_DBP_5_1": dbp, "HTN_Stage_5_2": htn_stage, "Weight_kg_5_3": weight,
                "Height_cm_5_3": height, "Calculated_BMI_5_3": bmi_val, "BMI_Category_5_4": bmi_cat,
                "Duration_HTN_Months_5_5": dur_htn, "Family_History_5_6": fam_hx, "Diabetes_Mellitus_6_1": dm,
                "CKD_6_2": ckd, "Proteinuria_6_3": prot, "Total_Cholesterol_6_4": chol,
                "Baseline_Complications_6_5": comp, "Treatment_Type_7_1": tx_type, "Med_Class_7_2": str(tx_class),
                "Med_Adherence_7_3": adh, "CVD_Event_Occurred_8_1": ev, "CVD_Event_Type_8_2": ev_type,
                "CVD_Event_Date_8_3": ev_date, "Censoring_Details_8_4": censor, "Censoring_Date_8_5": censor_date,
                "Data_Collector": "Belay Melaku", "Timestamp": datetime.now()
            }])
            try:
                existing = conn.read()
                updated = pd.concat([existing, df], ignore_index=True)
                conn.update(data=updated)
                st.success("Record Saved Successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
