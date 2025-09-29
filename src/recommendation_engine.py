import json
import random


class RecommendationEngine:
    def __init__(self, thresholds_path="data/thresholds.json", recs_path="data/recommendations.json"):
        try:
            with open(thresholds_path, 'r', encoding='utf-8') as f:
                self.thresholds = json.load(f)
            with open(recs_path, 'r', encoding='utf-8') as f:
                self.recommendations = json.load(f)
        except FileNotFoundError as e:
            self.thresholds = None
            self.recommendations = None

    def classify_bmi(self, bmi):
        if bmi >= self.thresholds['bmi']['thua_can']:
            return "Cao"
        elif bmi >= self.thresholds['bmi']['binh_thuong']:
            return "Trung bình"
        elif bmi < self.thresholds['bmi']['thieu_can']:
            return "Trung bình"
        else:
            return "Thấp"

    def classify_cholesterol(self, tc):
        if tc > self.thresholds['cholesterol_mmoll']['tang_nhe']:
            return "Cao"
        elif tc >= self.thresholds['cholesterol_mmoll']['binh_thuong']:
            return "Trung bình"
        else:
            return "Thấp"

    def classify_uric_acid(self, ua, sex):
        if sex == 1:  # Nam
            if ua > self.thresholds['uric_acid_umoll']['nam_binh_thuong']:
                return "Cao"
        else:  # Nữ
            if ua > self.thresholds['uric_acid_umoll']['nu_binh_thuong']:
                return "Cao"
        return "Thấp"

    def get_specific_recommendations(self, metric_name, level, num_items=5):
        if not self.recommendations:
            return None

        try:
            # Lấy một bản sao của dữ liệu để không làm thay đổi dữ liệu gốc
            original_data = self.recommendations[metric_name][level]
            data_copy = {key: value for key, value in original_data.items()}

            def sample_list(lst):
                if len(lst) > num_items:
                    return random.sample(lst, num_items)
                return lst

            # Xử lý phần bài tập
            if "goi_y_bai_tap" in data_copy:
                new_exercise_list = []
                for exercise_type in data_copy["goi_y_bai_tap"]:
                    new_type = exercise_type.copy()
                    new_type["chi_tiet"] = sample_list(new_type["chi_tiet"])
                    new_exercise_list.append(new_type)
                data_copy["goi_y_bai_tap"] = new_exercise_list

            # Xử lý phần dinh dưỡng
            if "che_do_dinh_duong" in data_copy:
                new_nutrition = data_copy["che_do_dinh_duong"].copy()
                if "nen_an" in new_nutrition:
                    new_nutrition["nen_an"] = sample_list(new_nutrition["nen_an"])
                if "nen_han_che" in new_nutrition:
                    new_nutrition["nen_han_che"] = sample_list(new_nutrition["nen_han_che"])
                data_copy["che_do_dinh_duong"] = new_nutrition

            # Xử lý phần lối sống
            if "loi_song_sinh_hoat" in data_copy and "thoi_quen_khac" in data_copy["loi_song_sinh_hoat"]:
                new_lifestyle = data_copy["loi_song_sinh_hoat"].copy()
                new_lifestyle["thoi_quen_khac"] = sample_list(new_lifestyle["thoi_quen_khac"])
                data_copy["loi_song_sinh_hoat"] = new_lifestyle

            return data_copy

        except KeyError:
            return None