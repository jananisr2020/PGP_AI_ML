import os
import requests
import pandas as pd
import streamlit as st

# Backend base URL - overridden by an environment variable when run via Docker network
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:7860")

st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")
st.title("SuperKart Store-Product Sales Forecast")
st.write(
    "Predict the total sales revenue of a product in a store using the "
    "tuned XGBoost model deployed behind a Flask API."
)

tab1, tab2 = st.tabs(["Single (Online) Prediction", "Batch Prediction"])

with tab1:
    st.subheader("Enter product & store details")
    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
        product_sugar_content = st.selectbox(
            "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
        )
        product_allocated_area = st.number_input(
            "Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f"
        )
        product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
        product_id_char = st.selectbox("Product Id Prefix", ["FD", "DR", "NC"])

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_location_city_type = st.selectbox(
            "Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"]
        )
        store_type = st.selectbox(
            "Store Type",
            ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"],
        )
        store_age_years = st.number_input("Store Age (Years)", min_value=0, value=16)
        product_type_category = st.selectbox(
            "Product Type Category", ["Perishables", "Non Perishables"]
        )

    if st.button("Predict Sales"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age_years,
            "Product_Type_Category": product_type_category,
        }
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
            response.raise_for_status()
            result = response.json()
            st.success(
                f"Predicted Total Sales: Rs. {result['predicted_Product_Store_Sales_Total']:.2f}"
            )
        except Exception as exc:
            st.error(f"Prediction failed: {exc}")

with tab2:
    st.subheader("Upload a CSV for batch prediction")
    st.caption(
        "The CSV must contain columns: Product_Weight, Product_Sugar_Content, "
        "Product_Allocated_Area, Product_MRP, Store_Size, Store_Location_City_Type, "
        "Store_Type, Product_Id_char, Store_Age_Years, Product_Type_Category"
    )
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        preview_df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(preview_df.head())

        if st.button("Run Batch Prediction"):
            uploaded_file.seek(0)
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
                response.raise_for_status()
                predictions = response.json()
                pred_series = pd.Series(predictions, name="Predicted_Sales")
                pred_series.index = pred_series.index.astype(int)
                result_df = preview_df.copy()
                result_df["Predicted_Sales"] = pred_series.sort_index().values
                st.write("Predictions:")
                st.dataframe(result_df)
            except Exception as exc:
                st.error(f"Batch prediction failed: {exc}")
