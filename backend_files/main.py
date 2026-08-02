import io
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Loading the serialized model pipeline (preprocessing + tuned XGBoost regressor)
MODEL_PATH = "superkart_model.joblib"
model = joblib.load(MODEL_PATH)

# Feature columns expected by the model, in the order the pipeline was trained on
FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]

superkart_api = Flask(__name__)


@superkart_api.get("/")
def home():
    return jsonify({"message": "SuperKart Sales Prediction API is up and running."})


@superkart_api.post("/v1/predict")
def predict_single():
    """Online inference: accepts a single JSON record and returns one prediction."""
    payload = request.get_json(force=True)
    input_df = pd.DataFrame([payload], columns=FEATURE_COLUMNS)
    prediction = model.predict(input_df)[0]
    return jsonify({"predicted_Product_Store_Sales_Total": round(float(prediction), 2)})


@superkart_api.post("/v1/predictbatch")
def predict_batch():
    """Batch inference: accepts a CSV file upload and returns predictions keyed by row index."""
    file = request.files["file"]
    batch_df = pd.read_csv(io.BytesIO(file.read()))
    batch_df = batch_df[FEATURE_COLUMNS]
    predictions = model.predict(batch_df)
    result = {str(idx): round(float(pred), 2) for idx, pred in enumerate(predictions)}
    return jsonify(result)


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
