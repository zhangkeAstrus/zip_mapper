import streamlit as st
import pandas as pd
import requests


STATE_ABBREVIATIONS = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
}

# Using API to get state info from ZIP code
def get_state_info(zip_code):
    try:
        response = requests.get(f"http://api.zippopotam.us/us/{zip_code}")
        if response.status_code == 200:
            state_name = response.json()['places'][0]['state']
            state_abbr = STATE_ABBREVIATIONS.get(state_name, "N/A")
            return state_name, state_abbr
        else:
            return "Invalid ZIP", "Invalid ZIP"
    except:
        return "Error", "Error"

st.title("📍 ZIP Code to State Mapper")

# Choose method
option = st.radio("Choose an option", ["🔎 Single ZIP code", "📤 Upload file with ZIPs"])

# Single ZIP lookup
if option == "🔎 Single ZIP code":
    zip_code = st.text_input("Enter ZIP Code:")
    if st.button("Get State"):
        state_name, state_abbr = get_state_info(zip_code)
        st.success(f"State: {state_name} ({state_abbr})")

# Batch ZIP lookup
else:
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Preview of uploaded file:")
        st.dataframe(df.head())

        zip_column = st.selectbox("Select the column with ZIP codes", df.columns)

        if st.button("Map ZIP codes to States"):
            df["State Name"], df["State Code"] = zip(*df[zip_column].astype(str).apply(get_state_info))
            st.success("Mapping completed!")
            st.dataframe(df.head())

            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV with States",
                data=csv,
                file_name="zip_to_state_output.csv",
                mime="text/csv"
            )
