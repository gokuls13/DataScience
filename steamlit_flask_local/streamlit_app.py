import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:5000/predict"
BULK_API_URL = "http://localhost:5000/bulk_predict"

st.title("Car Selling Price Prediction")

st.subheader("Please enter the values:")

with st.form(key="prediction_form"):
    car_name = st.text_input("Car Name")
    year = st.number_input("Year", min_value=1900, max_value=2024, step=1)
    present_price = st.number_input("Current Price (in Lakhs)", step=0.01)
    kms_driven = st.number_input("KMS Driven", step=1)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission Type", ["Manual", "Automatic"])
    owner = st.number_input("Owner", min_value=1, step=1)
    submit_button = st.form_submit_button(label='Predict')

if submit_button:
    user_input = {
        "Car_Name": car_name,
        "Year": year,
        "Present_Price": present_price,
        "Kms_Driven": kms_driven,
        "Fuel_Type": fuel_type,
        "Seller_Type": seller_type,
        "Transmission": transmission,
        "Owner": owner
    }
    response = requests.post(API_URL, json=user_input)
    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"The Predicted Price is: {prediction} Lakhs")
    else:
        st.error("Prediction failed. Please check the server.")

st.subheader("Please Upload a CSV/XLSX file for Bulk Predictions:")
upload_file = st.file_uploader("Choose a CSV or Excel File", type=['csv', 'xlsx', 'xls'])

if upload_file is not None:
    if upload_file.name.endswith("csv"):
        df = pd.read_csv(upload_file)
    else:
        df = pd.read_excel(upload_file)

    st.write("File Uploaded Successfully!")
    st.write(df.head())

    if st.button("Predict for uploaded File"):
        response = requests.post(BULK_API_URL, json={"data": df.to_dict(orient='records')})
        if response.status_code == 200:
            result_df = pd.read_json(response.text)
            st.write("Prediction Completed!")
            st.write(result_df.head())
            st.download_button(
                label="Download Predictions as CSV",
                data=result_df.to_csv(index=False),
                file_name="predictions.csv",
                mime="text/csv"
            )
        else:
            st.error("Bulk prediction failed. Please check the server.")