import streamlit as st
import pickle
import numpy as np

# Load models
with open('random_forest_model.pkl', 'rb') as reg_model_file:
    regression_model = pickle.load(reg_model_file)

with open('final_lightgbmmodel.pkl', 'rb') as class_model_file:
    classification_model = pickle.load(class_model_file)

def predict_regression(features):
    return regression_model.predict([features])[0]

def predict_classification(features):
    return classification_model.predict([features])[0]

def regression_model_ui():
    st.header("Predict Incurred Cost")

    # Initialize session state
    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None

    # Input fields
    age = st.number_input("Age", min_value=0, max_value=120, step=1, value=30)
    weekly_rate = st.number_input("Weekly Rate", min_value=0.0, step=0.1, value=500.0)
    gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
    marital_status = st.selectbox(
        "Marital Status", 
        options=["S", "M", "U"], 
        format_func=lambda x: {"S": "S", "M": "M", "U": "U"}[x]
    )
    marital_status_mapping = {
        "S": 1, "M": 0, "U": 2
    }
    marital_status_value = marital_status_mapping[marital_status]
    dependent_children = st.number_input("Dependent Children", min_value=0, max_value=10, step=1, value=0)
    dependents_other = st.number_input("Dependents Other", min_value=0, max_value=10, step=1, value=0)
    part_time_full_time = st.selectbox("Part-Time/Full-Time", options=[0, 1], format_func=lambda x: "Full-Time" if x == 1 else "Part-Time")
    initial_case_estimate = st.number_input("Initial Case Estimate", min_value=0, step=1, value=1000)

    accident_month = st.selectbox(
        "Accident Month", 
        options=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
        format_func=lambda x: {
            "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "May": "May", "Jun": "Jun",
            "Jul": "Jul", "Aug": "Aug", "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dec"
        }[x]
    )
    accident_month_mapping = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    accident_month_value = accident_month_mapping[accident_month]

    accident_day = st.selectbox("Accident Day", options=list(range(1, 32)))
    accident_year = st.number_input("Accident Year", min_value=1900, max_value=2100, step=1, value=2023)

    # Predict button
    if st.button("Predict Incurred Cost"):
        features = [
            age, weekly_rate, gender, marital_status_value, dependent_children, dependents_other,
            part_time_full_time, initial_case_estimate, accident_month_value, accident_day, accident_year
        ]
        st.session_state['prediction'] = predict_regression(features)
        st.success(f"Predicted Incurred Cost: {st.session_state['prediction']:.2f}")

    # Check Status button
    if st.button("Check Claim Status"):
        if st.session_state['prediction'] is not None:
            if st.session_state['prediction'] > 500:
                st.error("⚠️ Claim Status: URGENT")
            else:
                st.info("✅ Claim Status: NOT URGENT")
        else:
            st.warning("Please predict the incurred cost first before checking the claim status.")

def classification_model_ui():
    st.header("Predict Fraud")

    # Input fields
    months_as_customer = st.number_input("Months as Customer", min_value=0, step=1, value=12)
    age = st.number_input("Age", min_value=0, max_value=120, step=1, value=30)
    policy_state = st.selectbox(
        "Policy State", 
        options=["OH", "IL", "IN"], 
        format_func=lambda x: {"OH": "Ohio", "IL": "Illinois", "IN": "Indiana"}[x]
    )
    policy_state_mapping = {"OH": 2, "IL": 1, "IN": 0}
    policy_state_value = policy_state_mapping[policy_state]

    policy_csl = st.number_input("Policy CSL", min_value=0, step=1, value=100000)
    policy_deductable = st.number_input("Policy Deductable", min_value=0, step=1, value=500)
    policy_annual_premium = st.number_input("Policy Annual Premium", min_value=0.0, step=0.1, value=1000.0)
    umbrella_limit = st.number_input("Umbrella Limit", min_value=0, step=1, value=0)
    insured_zip = st.number_input("Insured Zip", min_value=0, step=1, value=12345)
    insured_sex = st.selectbox("Insured Sex", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
    # insured_education_level = st.selectbox(
    #     "Insured Education Level", 
    #     options=["JD", "High School", "Associate", "MD", "Masters", "PhD", "College"], 
    #     format_func=lambda x: {
    #         "JD": "JD", "High School": "High School", "Associate": "Associate",
    #         "MD": "MD", "Masters": "Masters", "PhD": "PhD", "College": "College"
    #     }[x]
    # )
    # insured_education_mapping = {
    #     "JD": 3, "High School": 2, "Associate": 0, "MD": 4, "Masters": 5, "PhD": 6, "College": 1
    # }
    # insured_education_value = insured_education_mapping[insured_education_level]

    insured_relationship = st.selectbox(
    "Insured Relationship",
    options=["own-child", "other-relative", "not-in-family", "husband", "wife", "unmarried"],
    format_func=lambda x: {
        "own-child": "Own Child",
        "other-relative": "Other Relative",
        "not-in-family": "Not in Family",
        "husband": "Husband",
        "wife": "Wife",
        "unmarried": "Unmarried"
    }[x]
    )
    insured_relationship_mapping = {
        "own-child": 3,
        "other-relative": 2,
        "not-in-family": 1,
        "husband": 0,
        "wife": 5,
        "unmarried": 4
    }
    insured_relationship_value = insured_relationship_mapping[insured_relationship]

    capital_gains = st.number_input("Capital Gains", min_value=0, step=1, value=0)
    capital_loss = st.number_input("Capital Loss", min_value=0, step=1, value=0)

    incident_type = st.selectbox(
        "Incident Type", 
        options=["Multi-vehicle Collision", "Single Vehicle Collision", "Vehicle Theft", "Parked Car"], 
        format_func=lambda x: {
            "Multi-vehicle Collision": "Multi-vehicle Collision",
            "Single Vehicle Collision": "Single Vehicle Collision",
            "Vehicle Theft": "Vehicle Theft",
            "Parked Car": "Parked Car"
        }[x]
    )
    incident_type_mapping = {
            "Multi-vehicle Collision": 0,
            "Single Vehicle Collision": 2,
            "Vehicle Theft": 3,
            "Parked Car": 1
    }
    incident_type_value = incident_type_mapping[incident_type]

    collision_type = st.selectbox(
        "Collision Type", 
        options=["Rear Collision", "Side Collision", "Front Collision", "Other"], 
        format_func=lambda x: {
            "Rear Collision": "Rear Collision",
            "Side Collision": "Side Collision",
            "Front Collision": "Front Collision",
            "Other": "Other"
        }[x]
    )
    collision_type_mapping = {
            "Rear Collision": 2,
            "Side Collision": 3,
            "Front Collision": 1,
            "Other": 0
    }
    collision_type_value = collision_type_mapping[collision_type]

    incident_severity = st.selectbox(
        "Incident Severity", 
        options=["Minor Damage", "Total Loss","Major Damage", "Trivial Damage"], 
        format_func=lambda x: {
            "Minor Damage": "Minor Damage",
            "Total Loss": "Total Loss",
            "Major Damage": "Major Damage",
            "Trivial Damage": "Trivial Damage"
        }[x]
    )
    incident_severity_mapping = {
            "Minor Damage": 1,
            "Total Loss": 2,
            "Major Damage": 0,
            "Trivial Damage": 3
    }
    incident_severity_value = incident_severity_mapping[incident_severity]

    authorities_contacted = st.selectbox(
        "Authorities Contacted", 
        options=["Police", "Fire","Other", "Ambulance"], 
        format_func=lambda x: {
            "Police": "Police",
            "Fire": "Fire",
            "Other": "Other",
            "Ambulance": "Ambulance"
        }[x]
    )
    authorities_contacted_mapping = {
            "Police": 1,
            "Fire": 2,
            "Other": 0,
            "Ambulance": 3
    }
    authorities_contacted_value = authorities_contacted_mapping[authorities_contacted]

    incident_state = st.selectbox(
        "Incident State", 
        options=["NY", "SC","WV", "VA","NC","PA","OH"], 
        format_func=lambda x: {
            "NY": "NY",
            "SC": "SC",
            "WV": "WV",
            "VA": "VA",
            "NC": "NC",
            "PA": "PA",
            "OH": "OH"
        }[x]
    )
    incident_state_mapping = {
            "NY": 1,
            "SC": 4,
            "WV": 6,
            "VA": 5,
            "NC": 0,
            "PA": 3,
            "OH": 2
    }
    incident_state_value = incident_state_mapping[incident_state]

    incident_city = st.selectbox(
        "Incident City", 
        options=["Springfield", "Arlington","Columbus","Northbend", "Hillsdale","Riverwood","Northbrook"], 
        format_func=lambda x: {
            "Springfield": "Springfield",
            "Arlington": "Arlington",
            "Columbus": "Columbus",
            "Northbend": "Northbend",
            "Hillsdale": "Hillsdale",
            "Riverwood": "Riverwood",
            "Northbrook": "Northbrook"
        }[x]
    )
    incident_city_mapping = {
            "Springfield": 6,
            "Arlington": 0,
            "Columbus": 1,
            "Northbend": 3,
            "Hillsdale": 2,
            "Riverwood": 5,
            "Northbrook": 4
    }
    incident_city_value = incident_city_mapping[incident_city]

    #incident_hour_of_the_day = st.number_input("Incident Hour of the Day", min_value=0, max_value=23, step=1, value=12)
    number_of_vehicles_involved = st.number_input("Number of Vehicles Involved", min_value=0, step=1, value=1)

    property_damage = st.selectbox(
        "Property Damage", 
        options=["?", "YES", "NO"], 
        format_func=lambda x: {"?": "Dont Know", "YES": "YES", "NO": "NO"}[x]
    )
    property_damage_mapping = {"?": 0, "YES": 2, "NO": 1}
    property_damage_value = property_damage_mapping[property_damage]

    bodily_injuries = st.number_input("Bodily Injuries", min_value=0, step=1, value=0)
    witnesses = st.number_input("Witnesses", min_value=0, step=1, value=0)

    police_report_available = st.selectbox(
        "Police Report Available", 
        options=["?", "YES", "NO"], 
        format_func=lambda x: {"?": "Dont Know", "YES": "YES", "NO": "NO"}[x]
    )
    police_report_available_mapping = {"?": 0, "YES": 2, "NO": 1}
    police_report_available_value = police_report_available_mapping[police_report_available]

    total_claim_amount = st.number_input("Total Claim Amount", min_value=0, step=1, value=0)
    injury_claim = st.number_input("Injury Claim", min_value=0, step=1, value=0)
    property_claim = st.number_input("Property Claim", min_value=0, step=1, value=0)
    vehicle_claim = st.number_input("Vehicle Claim", min_value=0, step=1, value=0)

    auto_make = st.selectbox(
        "Auto Make", 
        options=["Saab", "Dodge","Suburu","Nissan", "Cheverolet","Ford","BMW","Toyota","Audi","Accura","Volkswagen","Jeep","Mercedes","Honda"], 
        format_func=lambda x: {
            "Saab": "Saab",
            "Dodge": "Dodge",
            "Suburu": "Suburu",
            "Nissan": "Nissan",
            "Cheverolet": "Cheverolet",
            "Ford": "Ford",
            "BMW": "BMW",
            "Toyota": "Toyota",
            "Audi": "Audi",
            "Accura": "Accura",
            "Volkswagen": "Volkswagen",
            "Jeep": "Jeep",
            "Mercedes": "Mercedes",
            "Honda": "Honda"
            
        }[x]
    )
    auto_make_mapping = {
            "Saab": 10,
            "Dodge": 4,
            "Suburu": 11,
            "Nissan": 9,
            "Cheverolet": 3,
            "Ford": 5,
            "BMW": 2,
            "Toyota": 12,
            "Audi": 1,
            "Accura": 0,
            "Volkswagen": 13,
            "Jeep": 7,
            "Mercedes": 8,
            "Honda": 6
    }
    auto_make_value = auto_make_mapping[auto_make]

    auto_year = st.number_input("Auto Year", min_value=1900, max_value=2100, step=1, value=2020)
    # insured_hobbies_other = st.selectbox("Insured Hobbies Other", options=[True, False], format_func=lambda x: "Yes" if x else "No")

    # Predict
    if st.button("Predict Fraud"):
        features = [
            months_as_customer, age, policy_state_value, policy_csl, policy_deductable,
            policy_annual_premium, umbrella_limit, insured_zip, insured_sex,
            insured_relationship_value, capital_gains, capital_loss,incident_type_value,collision_type_value,
            incident_severity_value, authorities_contacted_value, incident_state_value, incident_city_value,
            number_of_vehicles_involved, property_damage_value, bodily_injuries,
            witnesses, police_report_available_value, total_claim_amount, injury_claim, property_claim,
            vehicle_claim,auto_make_value, auto_year
        ]
        prediction = predict_classification(features)
        st.success(f"Fraud Prediction: {'Fraud' if prediction == 1 else 'No Fraud'}")

def main():
    st.title("Claims Triage")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose Model", ["Claims Triage Incurred Cost Prediction", "Claims Triage Fraud Detection"])

    if app_mode == "Claims Triage Incurred Cost Prediction":
        regression_model_ui()
    elif app_mode == "Claims Triage Fraud Detection":
        classification_model_ui()

if __name__ == "__main__":
    main()

