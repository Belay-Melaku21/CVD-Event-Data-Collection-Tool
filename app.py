import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CVD Research Tool", layout="wide")

# Login Check
if "auth" not in st.session_state: st.session_state.auth = False
def login():
    st.title("🔐 Investigator Access")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == "Belay Melaku" and p == "@Belay6669":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Incorrect credentials")
if not st.session_state.auth: login(); st.stop()

# Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📋 CVD Event Data Abstraction Portal")

with st.form("cvd_research_form", clear_on_submit=True):
    
    # SECTION 1 & 2
    st.header("Section 1 & 2: Admin & Eligibility")
    col1, col2 = st.columns(2)
    with col1:
        s_id = st.text_input("1.1. Study ID")
        fac = st.selectbox("1.2. Facility Name", ["1=Densa", "2=Kotet", "3=Work-Mawcha", "4=Ahyo", "5=Atrons"])
        mrn = st.text_input("1.3. Patient MRN")
    with col2:
        cohort = st.selectbox("1.4. Cohort Group", ["1=Exposed (Hypertensive)", "2=Unexposed (Normotensive)"])
        d_enroll = st.text_input("1.5. Date of Enrollment (E.C.)")
        d_end = st.text_input("1.6. Follow-up End Date (E.C.)", value="30/10/2018")
    
    c1, c2, c3 = st.columns(3)
    age_elig = c1.selectbox("2.1. Age ≥18?", ["1=Yes", "2=No"])
    pre_cvd = c2.selectbox("2.2. Pre-existing CVD?", ["2=No", "1=Yes"])
    preg_htn = c3.selectbox("2.3. Pregnancy-induced HTN?", ["2=No", "1=Yes"])

    # SECTION 3 & 4
    st.header("Section 3 & 4: Demographics & Lifestyle")
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("3.1. Age (years)", min_value=0)
        sex = st.selectbox("3.2. Sex", ["1=Male", "2=Female"])
        res = st.selectbox("3.3. Residence", ["1=Urban", "2=Rural"])
        edu = st.selectbox("3.4. Education", ["1=No formal", "2=Primary", "3=Secondary", "4=Higher"])
    with col4:
        occ = st.selectbox("3.5. Occupation", ["1=Gov Employee", "1=Merchant", "1=Farmer", "1=Unemployed", "1=Other"])
        occ_oth = st.text_input("3.5.1. Specify Other") if "Other" in occ else "NA"
        marital = st.selectbox("3.6. Marital Status", ["1=Single", "2=Married", "3=Widowed", "4=Divorced"])
    
    st.subheader("Lifestyle")
    tob = st.selectbox("4.1. Tobacco Use", ["1=Never", "2=Current", "3=Previous"])
    alc = st.selectbox("4.2. Alcohol Consumption", ["1=Non-user", "2=Current User"])
    alc_qty = st.text_input("4.2.1. Drinks per day") if "Current User" in alc else "0"
    khat = st.selectbox("4.3. Khat Chewing", ["1=Never", "2=Current", "3=History"])
    phys = st.selectbox("4.4. Physical Activity", ["1=Active", "2=Inactive"])
    salt = st.selectbox("4.5. Salt Intake", ["1=High", "2=Normal/Low"])

    # SECTION 5: CLINICAL (AUTOMATED)
    st.header("Section 5: Clinical Measurements")
    sbp = st.number_input("5.1. SBP (mmHg)", min_value=0)
    dbp = st.number_input("5.1. DBP (mmHg)", min_value=0)
    
    # 5.2 HTN Stage Auto-logic
    htn_stage = "NA"
    if sbp >= 180 or dbp >= 110: htn_stage = "4=Stage 3/4"
    elif sbp >= 160 or dbp >= 100: htn_stage = "3=Stage 2"
    elif sbp >= 140 or dbp >= 90: htn_stage = "2=Stage 1"
    elif sbp >= 120 or dbp >= 80: htn_stage = "1=Pre-HTN"
    st.info(f"5.2. Auto-Calculated HTN Stage: {htn_stage}")

    weight = st.number_input("5.3. Weight (kg)", min_value=0.0)
    height = st.number_input("5.3. Height (cm)", min_value=0.0)
    
    # 5.3 & 5.4 BMI Logic
    bmi_val = 0.0
    bmi_cat = "NA"
    if weight > 0 and height > 0:
        bmi_val = round(weight / ((height/100)**2), 2)
        if bmi_val < 18.5: bmi_cat = "1=Underweight"
        elif bmi_val < 25: bmi_cat = "2=Normal"
        elif bmi_val < 30: bmi_cat = "3=Overweight"
        else: bmi_cat = "4=Obese"
    st.info(f"5.3. BMI: {bmi_val} | 5.4. Category: {bmi_cat}")
    
    dur_htn = st.text_input("5.5. Duration of HTN (months)")
    fam_hx = st.selectbox("5.6. Family History CVD/HTN", ["1=Yes", "2=No"])

    # SECTION 6 & 7
    st.header("Section 6 & 7: Profile & Treatment")
    c4, c5 = st.columns(2)
    dm = c4.selectbox("6.1. DM", ["1=Yes", "2=No"])
    ckd = c4.selectbox("6.2. CKD", ["1=Yes", "2=No"])
    prot = c4.selectbox("6.3. Proteinuria", ["1=Positive", "2=Negative"])
    chol = c5.text_input("6.4. Cholesterol")
    comp = c5.selectbox("6.5. Baseline Complications", ["1=None", "2=Prior Stroke", "3=Prior Cardiac"])
    
    tx_type = st.selectbox("7.1. Meds Type", ["1=Monotherapy", "2=Dual", "3=Polytherapy"])
    tx_class = st.multiselect("7.2. Specific Class", ["1=ACEi/ARB", "2=CCB", "3=Diuretics", "4=Beta-Blockers"])
    adh = st.selectbox("7.3. Adherence", ["1=Good", "2=Poor"])

    # SECTION 8: OUTCOME
    st.header("Section 8: Outcome & Survival")
    ev = st.selectbox("8.1. CVD Event?", ["2=No", "1=Yes"])
    ev_type = st.selectbox("8.2. Event Type", ["1=Stroke", "2=MI", "3=Heart Failure"]) if "Yes" in ev else "NA"
    ev_date = st.text_input("8.3. Event Date") if "Yes" in ev else "NA"
    
    censor = st.selectbox("8.4. Censoring Details", ["1=Not Censored", "2=Lost to Follow-up", "3=Died (Non-CVD)", "4=Study ended"])
    censor_date = st.text_input("8.5. Last Follow-up/Censoring Date") if censor != "1=Not Censored" else "NA"

    submit = st.form_submit_button("Submit Record")
    if submit:
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
        existing = conn.read()
        updated = pd.concat([existing, df], ignore_index=True)
        conn.update(data=updated)
        st.success("Record Saved!")
