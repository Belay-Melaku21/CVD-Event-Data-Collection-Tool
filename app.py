import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="CVD Data Abstraction Tool", layout="wide")

# Authentication Logic
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
            st.error("Invalid Username or Password")

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Header Information
st.title("📋 CVD Event Data Abstraction Portal")
st.markdown("---")
st.info("**Study Title:** Time to Cardiovascular Disease Event and Its Determinant Among Hypertensive Patients on Follow-Up at Health Centers in Mehal Amhara Saynt District.")

# Data Entry Form
with st.form("cvd_full_checklist_form", clear_on_submit=True):
    
    # --- SECTION 1: ADMINISTRATIVE & ELIGIBILITY ---
    st.header("Section 1: Administrative & Eligibility")
    col1, col2 = st.columns(2)
    with col1:
        study_id = st.text_input("1.1. Study ID")
        facility = st.selectbox("1.2. Facility Name", ["1=Densa", "2=Kotet", "3=Work-Mawcha", "4=Ahyo", "5=Atrons"])
        mrn = st.text_input("1.3. Patient MRN")
    with col2:
        cohort = st.selectbox("1.4. Cohort Group", ["1=Exposed (Hypertensive)", "2=Unexposed (Normotensive)"])
        enroll_date = st.text_input("1.5. Date of Enrollment (E.C.)", placeholder="DD/MM/YYYY")
        follow_end_date = st.text_input("1.6. Follow-up End Date (E.C.)", value="30/10/2018")

    # --- SECTION 2: ELIGIBILITY CHECKLIST ---
    st.header("Section 2: Eligibility Checklist (Exclusion Criteria)")
    e1, e2, e3 = st.columns(3)
    age_elig = e1.selectbox("2.1. Age ≥18 years?", ["1=Yes", "2=No"])
    pre_cvd = e2.selectbox("2.2. Pre-existing CVD (Stroke/MI/HF)?", ["2=No", "1=Yes"])
    preg_htn = e3.selectbox("2.3. Pregnancy-induced Hypertension?", ["2=No", "1=Yes"])

    # --- SECTION 3: SOCIO-DEMOGRAPHIC ---
    st.divider()
    st.header("SECTION 3: SOCIO-DEMOGRAPHIC CHARACTERISTICS")
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("3.1. Age (in years)", min_value=0, step=1)
        sex = st.selectbox("3.2. Sex", ["1=Male", "2=Female"])
        residence = st.selectbox("3.3. Residence", ["1=Urban", "2=Rural"])
    with col4:
        edu = st.selectbox("3.4. Educational Status", ["1=No formal education", "2=Primary (1-8)", "3=Secondary (9-12)", "4=Higher"])
        occ = st.selectbox("3.5. Occupational Status", ["1=Government Employee", "2=Merchant/Trader", "3=Farmer", "4=Unemployed", "5=Other"])
        occ_other = st.text_input("Specify if Other Occupation:") if "Other" in occ else "NA"
        marital = st.selectbox("3.6. Marital Status", ["1=Single", "2=Married", "3=Widowed", "4=Divorced/Separated"])

    # --- SECTION 4: LIFESTYLE & BEHAVIORAL ---
    st.header("SECTION 4: LIFESTYLE & BEHAVIORAL FACTORS")
    col5, col6 = st.columns(2)
    with col5:
        tobacco = st.selectbox("4.1. Tobacco Use", ["1=Never Smoker", "2=Current Smoker", "3=Previous Smoker"])
        alcohol = st.selectbox("4.2. Alcohol Consumption", ["1=Non-user", "2=Current User"])
        # Branching for Alcohol
        alc_qty = st.text_input("Average drinks/day (If current user)") if "Current User" in alcohol else "0"
    with col6:
        khat = st.selectbox("4.3. Khat Chewing", ["1=Never", "2=Current User", "3=History of regular use"])
        phys_act = st.selectbox("4.4. Physical Activity (≥30 min/day)", ["1=Physically Active", "2=Inactive"])
        salt = st.selectbox("4.5. Salt Intake", ["1=High (Adds salt)", "2=Normal/Low"])

    # --- SECTION 5: CLINICAL & PHYSIOLOGICAL ---
    st.divider()
    st.header("SECTION 5: CLINICAL & PHYSIOLOGICAL MEASUREMENTS")
    col7, col8 = st.columns(2)
    with col7:
        sbp = st.number_input("5.1. SBP (mmHg)", min_value=0)
        dbp = st.number_input("5.1. DBP (mmHg)", min_value=0)
        htn_stage = st.selectbox("5.2. Hypertension Stage", ["1=Pre-HTN", "2=Stage 1", "3=Stage 2", "4=Stage 3/4"])
        htn_months = st.text_input("5.5. Duration of HTN (months)")
        fam_hx = st.selectbox("5.6. Family History of CVD/HTN", ["1=Yes", "2=No"])
    with col8:
        weight = st.number_input("5.3. Weight (kg)", min_value=0.0, format="%.2f")
        height = st.number_input("5.3. Height (cm)", min_value=0.0, format="%.2f")
        
        # BMI Automated Calculation
        bmi_val = 0.0
        bmi_cat = "NA"
        if weight > 0 and height > 0:
            bmi_val = round(weight / ((height/100)**2), 2)
            if bmi_val < 18.5: bmi_cat = "1=Underweight (<18.5)"
            elif 18.5 <= bmi_val < 25: bmi_cat = "2=Normal"
            elif 25 <= bmi_val < 30: bmi_cat = "3=Overweight (25-29.9)"
            else: bmi_cat = "4=Obese (≥30)"
        
        st.metric("5.3. Calculated BMI", f"{bmi_val} kg/m²")
        st.write(f"**5.4. BMI Category:** {bmi_cat}")

    # --- SECTION 6: BIOCHEMICAL & COMORBIDITY ---
    st.header("SECTION 6: BIOCHEMICAL & COMORBIDITY PROFILE")
    col9, col10 = st.columns(2)
    with col9:
        dm = st.selectbox("6.1. Diabetes Mellitus (DM)", ["1=Yes", "2=No"])
        ckd = st.selectbox("6.2. Chronic Kidney Disease (CKD)", ["1=Yes", "2=No"])
        proteinuria = st.selectbox("6.3. Proteinuria", ["1=Positive", "2=Negative"])
    with col10:
        cholesterol = st.text_input("6.4. Total Cholesterol (mg/dL)", value="NA")
        baseline_comp = st.selectbox("6.5. Baseline Complications", ["1=None", "2=Prior Stroke", "3=Prior Cardiac issues"])

    # --- SECTION 7: TREATMENT & MANAGEMENT ---
    st.header("SECTION 7: TREATMENT & MANAGEMENT FACTORS")
    col11, col12 = st.columns(2)
    with col11:
        tx_type = st.selectbox("7.1. Type of Antihypertensive Meds", ["1=Monotherapy", "2=Dual Therapy", "3=Polytherapy"])
        tx_class = st.selectbox("7.2. Specific Class", ["1=ACEi/ARB", "2=CCB", "3=Diuretics", "4=Beta-Blockers"])
    with col12:
        adherence = st.selectbox("7.3. Medication Adherence (≥80%)", ["1=Good", "2=Poor"])

    # --- SECTION 8: OUTCOME & SURVIVAL ---
    st.divider()
    st.header("SECTION 8: OUTCOME & SURVIVAL DATA")
    col13, col14 = st.columns(2)
    with col13:
        cvd_event = st.selectbox("8.1. CVD Event Occurred?", ["1=Yes", "2=No"])
        # Branching for CVD Event
        event_type = st.selectbox("8.2. Type of CVD Event", ["1=Stroke", "2=MI", "3=Heart Failure"]) if "Yes" in cvd_event else "NA"
        event_date = st.text_input("8.3. Date of CVD Event (E.C.)") if "Yes" in cvd_event else "NA"
    with col14:
        censor_detail = st.selectbox("8.4. Censoring Details", ["1=Lost to Follow-up", "2=Died (Non-CVD)", "3=Study ended without event"])
        last_date = st.text_input("8.5. Date of Last Follow-up/Censoring (E.C.)")

    # Submission Logic
    submit_button = st.form_submit_button("Submit Data Record")

    if submit_button:
        # Construct DataFrame matching the Headers
        record = pd.DataFrame([{
            "Study_ID": study_id, "Facility_Name": facility, "Patient_MRN": mrn, "Cohort_Group": cohort,
            "Enrollment_Date_EC": enroll_date, "Followup_End_Date_EC": follow_end_date,
            "Age_Eligible_2_1": age_elig, "Pre_existing_CVD_2_2": pre_cvd, "Pregnancy_HTN_2_3": preg_htn,
            "Age_3_1": age, "Sex_3_2": sex, "Residence_3_3": residence, "Educational_Status_3_4": edu,
            "Occupational_Status_3_5": occ, "Occupation_Other_Detail": occ_other, "Marital_Status_3_6": marital,
            "Tobacco_Use_4_1": tobacco, "Alcohol_Consumption_4_2": alcohol, "Alcohol_Drinks_Per_Day": alc_qty,
            "Khat_Chewing_4_3": khat, "Physical_Activity_4_4": phys_act, "Salt_Intake_4_5": salt,
            "Baseline_SBP_5_1": sbp, "Baseline_DBP_5_1": dbp, "HTN_Stage_5_2": htn_stage,
            "Weight_kg_5_3": weight, "Height_cm_5_3": height, "Calculated_BMI_5_3": bmi_val,
            "BMI_Category_5_4": bmi_cat, "Duration_of_HTN_Months_5_5": htn_months, "Family_History_CVD_HTN_5_6": fam_hx,
            "Diabetes_Mellitus_6_1": dm, "Chronic_Kidney_Disease_6_2": ckd, "Proteinuria_6_3": proteinuria,
            "Total_Cholesterol_6_4": cholesterol, "Baseline_Complications_6_5": baseline_comp,
            "Type_of_Meds_7_1": tx_type, "Specific_Class_7_2": tx_class, "Medication_Adherence_7_3": adherence,
            "CVD_Event_Occurred_8_1": cvd_event, "Type_of_CVD_Event_8_2": event_type, "Date_of_CVD_Event_8_3": event_date,
            "Censoring_Details_8_4": censor_detail, "Date_of_Last_Followup_8_5": last_date,
            "Data_Collector": "Belay Melaku", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])

        try:
            # Get existing data and append
            existing_data = conn.read()
            updated_df = pd.concat([existing_data, record], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ Record successfully uploaded to Google Sheets!")
            st.balloons()
        except Exception as e:
            st.error(f"Error submitting data: {e}")

# Footer
st.markdown("---")
st.caption("Developed for CVD Event Research Project | © 2026")
