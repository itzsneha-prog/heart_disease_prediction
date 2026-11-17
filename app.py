import joblib
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Heart Health Risk Check",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink:#162b35; --muted:#61747c; --teal:#087f75; --mint:#e8f5f1; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    .stApp { background:linear-gradient(180deg,#f4faf8 0%,#f7f9fb 42%,#f5f7fa 100%); }
    .block-container { max-width:1120px; padding-top:2rem; padding-bottom:4rem; }
    h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:var(--ink); }
    .hero { background:linear-gradient(120deg,#103b43 0%,#087f75 65%,#20a18e 100%); color:white;
      padding:2.25rem 2.5rem; border-radius:24px; position:relative; overflow:hidden; margin-bottom:1.35rem;
      box-shadow:0 16px 40px rgba(8,82,77,.16); }
    .hero:after { content:'+'; position:absolute; right:8%; top:-58px; font-size:250px; font-weight:200; color:rgba(255,255,255,.08); }
    .eyebrow { text-transform:uppercase; letter-spacing:.16em; font-size:.76rem; font-weight:700; opacity:.8; }
    .hero h1 { color:white !important; font-size:2.35rem; margin:.35rem 0 .5rem; letter-spacing:-.04em; }
    .hero p { color:rgba(255,255,255,.84); margin:0; font-size:1.04rem; max-width:660px; }
    .panel { background:white; border:1px solid #e7edef; border-radius:20px; padding:1.45rem 1.55rem; box-shadow:0 8px 24px rgba(31,58,67,.045); }
    .section-title { font:700 1.15rem 'Manrope',sans-serif; color:#162b35 !important; margin:0 0 .2rem; }
    .section-sub { color:#61747c !important; font-size:.9rem; margin:0 0 1rem; }
    .stApp label, .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stSlider"] label, .stApp [data-testid="stNumberInput"] label,
    .stApp [data-testid="stSelectbox"] label { color:#243b45 !important; }
    .stApp [data-testid="stWidgetLabel"] p { font-weight:600 !important; }
    .step { display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:9px; background:var(--mint); color:var(--teal); font-weight:700; margin-right:.55rem; }
    div[data-testid="stForm"] { border:0; padding:0; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] button { background:#087f75; color:white; border:0; border-radius:12px; padding:.72rem 1.2rem; font-weight:700; min-height:48px; transition:.15s ease; }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover { background:#06665f; color:white; border:0; transform:translateY(-1px); }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-radius:10px; }
    .note { color:#65777f; font-size:.83rem; line-height:1.5; padding:.85rem 1rem; background:#f2f6f7; border-radius:12px; margin-top:1rem; }
    .result-label { font-size:.8rem; font-weight:700; text-transform:uppercase; letter-spacing:.12em; color:#61747c; }
    .stAlert { border-radius:14px; }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_artifacts():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    columns = joblib.load("heart_columns.pkl")
    return model, scaler, columns


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Heart health · Mini project</div>
      <h1>A clearer view of your heart health</h1>
      <p>Enter the clinical measurements below to see the result from the project’s prediction model.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    model, scaler, expected_columns = load_artifacts()
except Exception as exc:
    st.error("The prediction files could not be loaded. Keep the model, scaler, and columns files beside app.py, then restart the app.")
    st.caption(f"Details: {exc}")
    st.stop()

left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown('<p class="section-title"><span class="step">1</span>Your information</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Use the values from your report where available.</p>', unsafe_allow_html=True)

    with st.form("prediction_form"):
        a, b = st.columns(2, gap="medium")
        with a:
            age = st.slider("Age", 18, 100, 40)
            sex = st.selectbox("Sex", ["M", "F"], format_func=lambda x: {"M": "Male", "F": "Female"}[x])
            chest_pain = st.selectbox("Chest pain type", ["ATA", "NAP", "TA", "ASY"], format_func=lambda x: {"ATA": "Atypical angina", "NAP": "Non-anginal pain", "TA": "Typical angina", "ASY": "Asymptomatic"}[x])
            resting_bp = st.number_input("Resting blood pressure (mm Hg)", 80, 200, 120)
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        with b:
            fasting_bs = st.selectbox("Fasting blood sugar > 120 mg/dL", [0, 1], format_func=lambda x: "Yes" if x else "No")
            resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"], format_func=lambda x: {"Normal": "Normal", "ST": "ST-T wave abnormality", "LVH": "Left ventricular hypertrophy"}[x])
            max_hr = st.slider("Maximum heart rate", 60, 220, 150)
            exercise_angina = st.selectbox("Exercise-induced angina", ["Y", "N"], format_func=lambda x: "Yes" if x == "Y" else "No")
            oldpeak = st.slider("Oldpeak (ST depression)", 0.0, 6.0, 1.0, 0.1)
            st_slope = st.selectbox("ST slope", ["Up", "Flat", "Down"])
        submitted = st.form_submit_button("Check prediction", use_container_width=True)


with right:
    st.markdown('<p class="section-title"><span class="step">2</span>Your result</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Your prediction will appear here after you submit.</p>', unsafe_allow_html=True)

    if submitted:
        raw_input = {
            "Age": age,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs,
            "MaxHR": max_hr,
            "Oldpeak": oldpeak,
            "Sex_" + sex: 1,
            "ChestPainType_" + chest_pain: 1,
            "RestingECG_" + resting_ecg: 1,
            "ExerciseAngina_" + exercise_angina: 1,
            "ST_Slope_" + st_slope: 1,
        }
        input_df = pd.DataFrame([raw_input])
        input_df = input_df.reindex(columns=expected_columns, fill_value=0)
        try:
            scaled_input = scaler.transform(input_df)
            prediction = model.predict(scaled_input)[0]
            if prediction == 1:
                st.error("⚠️ The model indicates a higher likelihood of heart disease.")
            else:
                st.success("✅ The model indicates a lower likelihood of heart disease.")
            st.caption("This is an educational model output, not a diagnosis.")
        except Exception as exc:
            st.error("The prediction could not be generated. Check that the input columns match the saved model.")
            st.caption(f"Details: {exc}")
    else:
        st.info("Complete the form and select **Check prediction** to see the model output.")

    st.markdown('<div class="note">This mini-project is for learning and demonstration. It cannot diagnose a condition or replace advice from a qualified healthcare professional.</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align:center;color:#829198;font-size:.8rem;margin-top:1.5rem'>Built by PulsePoint · Heart health prediction mini-project</div>", unsafe_allow_html=True)






