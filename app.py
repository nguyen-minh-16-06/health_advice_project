import streamlit as st

from src.predictor import RiskPredictor
from src.recommendation_engine import RecommendationEngine


def load_engines():
    predictor = RiskPredictor()
    engine = RecommendationEngine()
    return predictor, engine
predictor, engine = load_engines()


def display_recommendations(metric_name, level, recs):
    if recs:
        with st.expander(f"Xem thêm gợi ý cho {metric_name} (Mức độ: {level.upper()})"):
            st.markdown(f"**Mô tả:** {recs['mo_ta']}")

            if 'goi_y_bai_tap' in recs:
                st.markdown("---")
                st.subheader("🏋️ BÀI TẬP GỢI Ý")
                for ex_type in recs['goi_y_bai_tap']:
                    st.markdown(f"**- {ex_type['loai_bai_tap']}:**")
                    for detail in ex_type['chi_tiet']:
                        st.markdown(f"  + {detail}")

            if 'che_do_dinh_duong' in recs:
                st.markdown("---")
                st.subheader("🥗 CHẾ ĐỘ DINH DƯỠNG")
                nutrition = recs['che_do_dinh_duong']
                st.markdown(f"**Nguyên tắc chung:** {nutrition['nguyen_tac_chung']}")
                if "nen_an" in nutrition and nutrition["nen_an"]:
                    st.markdown(f"**Nên ăn:** {', '.join(nutrition['nen_an'])}")
                if "nen_han_che" in nutrition and nutrition["nen_han_che"]:
                    st.markdown(f"**Nên hạn chế:** {', '.join(nutrition['nen_han_che'])}")

            if 'loi_song_sinh_hoat' in recs:
                st.markdown("---")
                st.subheader("🏃 LỐI SỐNG SINH HOẠT")
                lifestyle = recs['loi_song_sinh_hoat']
                st.markdown(f"**Giấc ngủ:** {lifestyle['giac_ngu']}")
                st.markdown(f"**Căng thẳng:** {lifestyle['quan_ly_cang_thang']}")
                if "thoi_quen_khac" in lifestyle and lifestyle["thoi_quen_khac"]:
                    st.markdown("**Thói quen khác:**")
                    for habit in lifestyle['thoi_quen_khac']:
                        st.markdown(f"- {habit}")


st.set_page_config(page_title = "Health Advice AI", layout = "wide")
st.title("TRỢ LÝ PHÂN TÍCH SỨC KHOẺ 👨🏻‍⚕️")

st.markdown("""
<style>
    div[data-testid="stAlert"] svg {
        display: none;
    }

    div[data-testid="stAlert"] {
        display: flex;
        align-items: center;
    }

    div[data-testid="stAlert"] h3 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("Nhập chỉ số của bạn")
sex = st.sidebar.selectbox("Giới tính", (1, 0), format_func=lambda x: "Nam" if x == 1 else "Nữ")
bmi = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0, step=0.1)
uric_acid = st.sidebar.number_input("Acid Uric (µmol/L)", min_value=100.0, max_value=1000.0, value=350.0, step=10.0)
cholesterol = st.sidebar.number_input("Cholesterol (mmol/L)", min_value=1.0, max_value=15.0, value=5.0, step=0.1)

if st.sidebar.button("PHÂN TÍCH"):
    if predictor.model is None or engine.recommendations is None:
        st.error("Lỗi: KHÔNG THỂ ĐƯA RA GỢI Ý.")
    else:
        user_data = {
            "sex": sex, "BMI": bmi,
            "TC (cholesterol)": cholesterol, "UA (uric acid)": uric_acid
        }
        overall_risk = predictor.predict_risk(user_data)

        st.header("Tình trạng sức khỏe tổng quan")
        col1, col2 = st.columns([1, 1])
        with col1:
            if overall_risk == "Thấp":
                st.success(f"#### Mức độ: {overall_risk.upper()}")
            elif overall_risk == "Trung bình":
                st.warning(f"#### Mức độ: {overall_risk.upper()}")
            else:  # Nguy cơ Cao
                st.error(f"#### Mức độ: {overall_risk.upper()}")

        st.markdown("---")

        st.header("Gợi ý rèn luyện và lối sống 🔎")

        bmi_level = engine.classify_bmi(bmi)
        bmi_recs = engine.get_specific_recommendations("BMI", bmi_level)
        display_recommendations("BMI", bmi_level, bmi_recs)

        uric_acid_level = engine.classify_uric_acid(uric_acid, sex)
        uric_acid_recs = engine.get_specific_recommendations("UricAcid", uric_acid_level)
        display_recommendations("UricAcid", uric_acid_level, uric_acid_recs)

        cholesterol_level = engine.classify_cholesterol(cholesterol)
        cholesterol_recs = engine.get_specific_recommendations("Cholesterol", cholesterol_level)
        display_recommendations("Cholesterol", cholesterol_level, cholesterol_recs)

        st.markdown("---")
        if "Disclaimer" in engine.recommendations:
            st.warning(f"**Lưu ý:** {engine.recommendations['Disclaimer']}")
else:
    st.info("Vui lòng nhập các chỉ số vào thanh bên trái và nhấn nút 'Phân Tích'.")