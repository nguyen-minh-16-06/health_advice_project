import joblib
import pandas as pd

MODEL_PATH = "models/risk_model.joblib"


class RiskPredictor:
    def __init__(self):
        try:
            self.model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            self.model = None

    def predict_risk(self, user_data):
        if self.model is None:
            return "Lỗi: Mô hình chưa được tải."

        try:
            input_df = pd.DataFrame([user_data])

            features_in_order = ["sex", "BMI", "TC (cholesterol)", "UA (uric acid)"]
            input_df_ordered = input_df[features_in_order]

            # Đưa ra dự đoán
            prediction = self.model.predict(input_df_ordered)
            return prediction[0]

        except Exception as e:
            return f"Lỗi dự đoán: {e}"