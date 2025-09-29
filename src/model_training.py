import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_and_evaluate_model(data_filepath, model_save_path):
    df = pd.read_csv(data_filepath)

    features = ["sex", "BMI", "TC (cholesterol)", "UA (uric acid)"]
    target = "risk_level"
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 16, stratify=y)
    print(f"Đã chia dữ liệu: {len(X_train)} mẫu huấn luyện, {len(X_test)} mẫu kiểm tra.")

    model = RandomForestClassifier(
        n_estimators = 1000,
        random_state = 16,
        class_weight = "balanced"
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n--- KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, labels = ["Cao", "Trung bình", "Thấp"]))
    print("---------------------------------")

    # Lưu lại mô hình
    os.makedirs(os.path.dirname(model_save_path), exist_ok = True)
    joblib.dump(model, model_save_path)

if __name__ == '__main__':
    cleaned_data_file = "data/processed/train_cleaned.csv"
    model_path = "models/risk_model.joblib"
    train_and_evaluate_model(cleaned_data_file, model_path)