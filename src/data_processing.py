import pandas as pd
import json
import os

def load_thresholds(filepath="data/thresholds.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def bmi_risk(bmi, thresholds):
    if bmi >= thresholds['bmi']['thua_can']:
        return 2 # Cao
    elif bmi >= thresholds['bmi']['binh_thuong']:
        return 1 # Trung bình
    elif bmi < thresholds['bmi']['thieu_can']:
        return 1 # Trung bình
    else:
        return 0 # Thấp

def cholesterol_risk(tc, thresholds):
    if tc < thresholds['cholesterol_mmoll']['binh_thuong']:
        return 0  # Thấp
    elif tc <= thresholds['cholesterol_mmoll']['tang_nhe']:
        return 1  # Trung bình
    else:
        return 2  # Cao


def uric_risk(row, thresholds):
    ua, sex = row["UA (uric acid)"], row["sex"]
    if sex == 1:  # Nam
        return 0 if ua <= thresholds['uric_acid_umoll']['nam_binh_thuong'] else 2
    else:  # Nữ
        return 0 if ua <= thresholds['uric_acid_umoll']['nu_binh_thuong'] else 2


def final_risk(row):
    levels = []
    for score in [row["BMI_risk"], row["Cholesterol_risk"], row["Uric_risk"]]:
        if score == 0:
            levels.append("Thấp")
        elif score == 1:
            levels.append("Trung bình")
        else:
            levels.append("Cao")

    high_count = levels.count("Cao")
    low_count = levels.count("Thấp")

    if high_count >= 2:
        return "Cao"
    elif low_count >= 2:
        return "Thấp"
    else:
        return "Trung bình"

def process_file(input_path, output_path, thresholds):
    df = pd.read_csv(input_path)

    df["BMI_risk"] = df["BMI"].apply(lambda x: bmi_risk(x, thresholds))
    df["Cholesterol_risk"] = df["TC (cholesterol)"].apply(lambda x: cholesterol_risk(x, thresholds))
    df["Uric_risk"] = df.apply(lambda row: uric_risk(row, thresholds), axis=1)

    df["risk_level"] = df.apply(final_risk, axis=1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Đã xử lý và lưu file tại: {output_path}")

if __name__ == '__main__':
    threshold_config = load_thresholds()

    process_file("data/train_dataset.csv", "data/processed/train_cleaned.csv", threshold_config)