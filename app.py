import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Settings
st.set_page_config(page_title="CVD Data Portal", layout="centered")

# Authentication
if "auth" not in st.session_state: st.session_state.auth = False
def login():
    st.title("🔐 Investigator Login")
    u = st.text_input("Investigator Name")
    p = st.text_input("Access Key", type="password")
    if st.button("Access Portal"):
        if u == "Belay Melaku" and p == "@Belay6669":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Access Denied.")
if not st.session_state.auth: login(); st.stop()

# Connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📋 CVD Event Data Entry")
st.info("እባክዎን መረጃውን በእያንዳንዱ ሴክሽን ስር በጥንቃቄ ይሙሉ")

# Creating Separate Tabs for Each Section
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "S-1 & 2", "S-3", "S-4", "S-5", "S-6", "S-7", "S-8", "Submit"
])

# ዳታዎችን ለጊዜው ለማስቀመጥ
if 'form_data' not in st.session_state: st.session_state.form_data = {}

with tab1:
    st.header("Section 1 & 2: Admin & Eligibility")
    st.session_state.form_data['s_id'] = st.text_input("1.1. Study ID")
    st.session_state.form_data['fac'] = st.selectbox("1.2. Facility", ["1=Densa", "2=Kotet", "3=Work-Mawcha", "4=Ahyo", "5=Atrons"])
    st.session_state.form_data['mrn'] = st.text_input("1.3. Patient MRN")
    st.session_state.form_data['cohort'] = st.selectbox("1.4. Cohort", ["1=Exposed", "2=Unexposed"])
    st.session_state.form_data['d_enroll'] = st.text_input("1.5. Enrollment Date (E.C.)")
    st.session_state.form_data['d_end'] = st.text_input("1.6. Follow-up End Date (E.C.)", value="30/10/2018")
    st.session_state.form_data['age_elig'] = st.selectbox("2.1. Age ≥18?", ["1=Yes", "2=No"])
    st.session_state.form_data['pre_cvd'] = st.selectbox("2.2. Pre-existing CVD?", ["2=No", "1=Yes"])
    st.session_state.form_data['preg_htn'] = st.selectbox("2.3. Pregnancy-induced HTN?", ["2=No", "1=Yes"])

with tab2:
    st.header("Section 3: Socio-Demographic")
    st.session_state.form_data['age'] = st.number_input("3.1. Age (Years)", min_value=0)
    st.session_state.form_data['sex'] = st.selectbox("3.2. Sex", ["1=Male", "2=Female"])
    st.session_state.form_data['res'] = st.selectbox("3.3. Residence", ["1=Urban", "2=Rural"])
    st.session_state.form_data['edu'] = st.selectbox("3.4. Education", ["1=No formal", "2=Primary", "3=Secondary", "4=Higher"])
    st.session_state.form_data['occ'] = st.selectbox("3.5. Occupation", ["1=Gov Employee", "2=Merchant", "3=Farmer", "4=Unemployed", "5=Other"])
    if "Other" in st.session_state.form_data['occ']:
        st.session_state.form_data['occ_oth'] = st.text_input("3.5.1. Specify Occupation")
    else: st.session_state.form_data['occ_oth'] = "NA"
    st.session_state.form_data['marital'] = st.selectbox("3.6. Marital Status", ["1=Single", "2=Married", "3=Widowed", "4=Divorced"])

with tab3:
    st.header("Section 4: Lifestyle Factors")
    st.session_state.form_data['tob'] = st.selectbox("4.1. Tobacco", ["1=Never", "2=Current", "3=Previous"])
    st.session_state.form_data['alc'] = st.selectbox("4.2. Alcohol", ["1=Non-user", "2=Current User"])
    if "Current User" in st.session_state.form_data['alc']:
        st.session_state.form_data['alc_qty'] = st.text_input("4.2.1. Drinks per day")
    else: st.session_state.form_data['alc_qty'] = "0"
    st.session_state.form_data['khat'] = st.selectbox("4.3. Khat Chewing", ["1=Never", "2=Current", "3=History"])
    st.session_state.form_data['phys'] = st.selectbox("4.4. Physical Activity", ["1=Active", "2=Inactive"])
    st.session_state.form_data['salt'] = st.selectbox("4.5. Salt Intake", ["1=High", "2=Normal/Low"])

with tab4:
    st.header("Section 5: Clinical & Physiological")
    sbp = st.number_input("5.1. SBP (mmHg)", min_value=0)
    dbp = st.number_input("5.1. DBP (mmHg)", min_value=0)
    
    # Auto HTN Logic
    htn_stage = "NA"
    if sbp >= 180 or dbp >= 110: htn_stage = "4=Stage 3/4"
    elif sbp >= 160 or dbp >= 100: htn_stage = "3=Stage 2"
    elif sbp >= 140 or dbp >= 90: htn_stage = "2=Stage 1"
    elif sbp >= 120 or dbp >= 80: htn_stage = "1=Pre-HTN"
    
    st.info(f"Auto-Calculated HTN Stage: {htn_stage}")
    st.session_state.form_data['sbp'] = sbp
    st.session_state.form_data['dbp'] = dbp
    st.session_state.form_data['htn_stage'] = htn_stage
    
    w = st.number_input("5.3. Weight (kg)", min_value=0.0)
    h = st.number_input("5.3. Height (cm)", min_value=0.0)
    
    bmi = 0.0
    bmi_cat = "NA"
    if w > 0 and h > 0:
        bmi = round(w / ((h/100)**2), 2)
        if bmi < 18.5: bmi_cat = "1=Underweight"
        elif bmi < 25: bmi_cat = "2=Normal"
        elif bmi < 30: bmi_cat = "3=Overweight"
        else: bmi_cat = "4=Obese"
    
    st.info(f"BMI: {bmi} | Category: {bmi_cat}")
    st.session_state.form_data['w'], st.session_state.form_data['h'] = w, h
    st.session_state.form_data['bmi'], st.session_state.form_data['bmi_cat'] = bmi, bmi_cat
    st.session_state.form_data['dur_htn'] = st.text_input("5.5. Duration (Months)")
    st.session_state.form_data['fam_hx'] = st.selectbox("5.6. Family History", ["1=Yes", "2=No"])

with tab5:
    st.header("Section 6: Biochemical Profile")
    st.session_state.form_data['dm'] = st.selectbox("6.1. DM", ["1=Yes", "2=No"])
    st.session_state.form_data['ckd'] = st.selectbox("6.2. CKD", ["1=Yes", "2=No"])
    st.session_state.form_data['prot'] = st.selectbox("6.3. Proteinuria", ["1=Positive", "2=Negative"])
    st.session_state.form_data['chol'] = st.text_input("6.4. Cholesterol")
    st.session_state.form_data['comp'] = st.selectbox("6.5. Baseline Complications", ["1=None", "2=Prior Stroke", "3=Prior Cardiac"])

with tab6:
    st.header("Section 7: Treatment Factors")
    st.session_state.form_data['tx_type'] = st.selectbox("7.1. Meds Type", ["1=Monotherapy", "2=Dual", "3=Polytherapy"])
    st.session_state.form_data['tx_class'] = st.multiselect("7.2. Specific Class", ["1=ACEi/ARB", "2=CCB", "3=Diuretics", "4=Beta-Blockers"])
    st.session_state.form_data['adh'] = st.selectbox("7.3. Adherence", ["1=Good", "2=Poor"])

with tab7:
    st.header("Section 8: Outcome Data")
    ev = st.selectbox("8.1. CVD Event?", ["2=No", "1=Yes"])
    st.session_state.form_data['ev'] = ev
    if "Yes" in ev:
        st.session_state.form_data['ev_type'] = st.selectbox("8.2. Event Type", ["1=Stroke", "2=MI", "3=Heart Failure"])
        st.session_state.form_data['ev_date'] = st.text_input("8.3. Event Date")
    else:
        st.session_state.form_data['ev_type'], st.session_state.form_data['ev_date'] = "NA", "NA"
    
    censor = st.selectbox("8.4. Censoring", ["1=Not Censored", "2=Lost", "3=Died", "4=Ended"])
    st.session_state.form_data['censor'] = censor
    if censor != "1=Not Censored":
        st.session_state.form_data['censor_date'] = st.text_input("8.5. Last Date")
    else: st.session_state.form_data['censor_date'] = "NA"

with tab8:
    st.header("Review & Submit")
    st.write("እባክዎን ከላይ ያሉትን ትሮች (Tabs) በመጠቀም መረጃው መሞላቱን ያረጋግጡ።")
    if st.button("Final Submit Data"):
        fd = st.session_state.form_data
        df = pd.DataFrame([{
            "Study_ID": fd['s_id'], "Facility_Name": fd['fac'], "Patient_MRN": fd['mrn'], "Cohort_Group": fd['cohort'],
            "Enrollment_Date_EC": fd['d_enroll'], "Followup_End_Date_EC": fd['d_end'], "Age_Eligible_2_1": fd['age_elig'],
            "Preexisting_CVD_2_2": fd['pre_cvd'], "Pregnancy_HTN_2_3": fd['preg_htn'], "Age_3_1": fd['age'],
            "Sex_3_2": fd['sex'], "Residence_3_3": fd['res'], "Educational_Status_3_4": fd['edu'],
            "Occupational_Status_3_5": fd['occ'], "Occupation_Other_Detail": fd['occ_oth'], "Marital_Status_3_6": fd['marital'],
            "Tobacco_Use_4_1": fd['tob'], "Alcohol_Consumption_4_2": fd['alc'], "Alcohol_Drinks_Per_Day": fd['alc_qty'],
            "Khat_Chewing_4_3": fd['khat'], "Physical_Activity_4_4": fd['phys'], "Salt_Intake_4_5": fd['salt'],
            "Baseline_SBP_5_1": fd['sbp'], "Baseline_DBP_5_1": fd['dbp'], "HTN_Stage_5_2": fd['htn_stage'],
            "Weight_kg_5_3": fd['w'], "Height_cm_5_3": fd['h'], "Calculated_BMI_5_3": fd['bmi'],
            "BMI_Category_5_4": fd['bmi_cat'], "Duration_HTN_Months_5_5": fd['dur_htn'], "Family_History_5_6": fd['fam_hx'],
            "Diabetes_Mellitus_6_1": fd['dm'], "CKD_6_2": fd['ckd'], "Proteinuria_6_3": fd['prot'],
            "Total_Cholesterol_6_4": fd['chol'], "Baseline_Complications_6_5": fd['comp'], "Treatment_Type_7_1": fd['tx_type'],
            "Med_Class_7_2": str(fd['tx_class']), "Med_Adherence_7_3": fd['adh'], "CVD_Event_Occurred_8_1": fd['ev'],
            "CVD_Event_Type_8_2": fd['ev_type'], "CVD_Event_Date_8_3": fd['ev_date'], "Censoring_Details_8_4": fd['censor'],
            "Censoring_Date_8_5": fd['censor_date'], "Data_Collector": "Belay Melaku", "Timestamp": datetime.now()
        }])
        
        # Write to GSheets
        existing = conn.read()
        updated = pd.concat([existing, df], ignore_index=True)
        conn.update(data=updated)
        st.success("ዳታው በትክክል ተመዝግቧል! ✅")
        st.balloons()
