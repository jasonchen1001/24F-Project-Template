import streamlit as st
import requests

st.title("Review Internship Applications")

# View Applications
if st.button("View Applications"):
    response = requests.get("http://localhost:5000/hr/applications")
    if response.status_code == 200:
        applications = response.json()
        st.table(applications)
    else:
        st.error("Failed to fetch applications.")

# Accept or Reject Application
st.subheader("Manage Applications")
application_id = st.number_input("Application ID", min_value=1, step=1)
decision = st.selectbox("Decision", ["Accept", "Reject"])

if st.button("Submit Decision"):
    decision_data = {"status": decision}
    response = requests.put(f"http://localhost:5000/hr/applications/{application_id}", json=decision_data)
    if response.status_code == 200:
        st.success("Application status updated successfully!")
    else:
        st.error("Failed to update application status.")