from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Heart Health Risk Check",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink:#10252d; --muted:#40545d; --teal:#087f75; --mint:#e8f5f1; color-scheme:light; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
    .stApp, .stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li, .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] p { color:var(--ink) !important; }
    .stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p { color:var(--muted) !important; }
    .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
    .stApp label, .stApp [data-testid="stRadio"] label, .stApp [data-testid="stCheckbox"] label { color:#142b34 !important; }
    .stApp input, .stApp textarea, .stApp [data-baseweb="select"] *,
    .stApp [data-baseweb="input"] input { color:#10252d !important; }
    .stApp [data-testid="stNumberInput"] input,
    .stApp [data-testid="stTextInput"] input,
    .stApp [data-testid="stTextArea"] textarea,
    .stApp div[data-baseweb="input"] input {
      color:#10252d !important; -webkit-text-fill-color:#10252d !important;
      background-color:#ffffff !important; opacity:1 !important; caret-color:#10252d !important;
    }
    .stApp div[data-baseweb="input"] > div { background-color:#ffffff !important; }
    .stApp [data-baseweb="select"],
    .stApp [data-baseweb="select"] > div,
    .stApp [data-baseweb="select"] div,
    .stApp [data-baseweb="select"] [role="combobox"],
    .stApp [data-baseweb="select"] [role="combobox"] > div,
    .stApp [data-baseweb="select"] [role="listbox"],
    .stApp [data-baseweb="select"] [role="option"] {
      background-color:#ffffff !important; background:#ffffff !important;
    }
    .stApp [data-baseweb="select"] svg { color:#40545d !important; fill:#40545d !important; }
    .stApp [data-baseweb="select"] path { fill:#40545d !important; }
    .stApp [data-baseweb="select"] [role="combobox"],
    .stApp [data-baseweb="select"] [role="combobox"] * {
      color:#10252d !important; -webkit-text-fill-color:#10252d !important;
    }
    .stApp .hero p { color:rgba(255,255,255,.92) !important; }
    .stApp div[data-baseweb="select"] [role="combobox"],
    .stApp div[data-baseweb="select"] [role="combobox"] *,
    .stApp div[data-baseweb="select"] [role="option"] {
      color:#10252d !important; -webkit-text-fill-color:#10252d !important; opacity:1 !important;
    }
    .stApp input::placeholder, .stApp textarea::placeholder { color:#52656e !important; -webkit-text-fill-color:#52656e !important; opacity:1 !important; }
    .stApp [data-testid="stSidebar"] { background:#edf4f3; }
    .stApp [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#10252d !important; }
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
    .panel { background:white; border:1px solid #e7edef; border-radius:20px; padding:1.45rem 1.55rem; box-shadow:0 8px 24px rgba(31,58,67,.045); margin-bottom:1rem; }
    .section-title { font:700 1.15rem 'Manrope',sans-serif; color:#162b35 !important; margin:0 0 .2rem; }
    .section-sub { color:#40545d !important; font-size:.9rem; margin:0 0 1rem; }
    .stApp label, .stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stSlider"] label, .stApp [data-testid="stNumberInput"] label,
    .stApp [data-testid="stSelectbox"] label { color:#243b45 !important; }
    .stApp [data-testid="stWidgetLabel"] p { font-weight:600 !important; }
    div[data-testid="stForm"] { border:0; padding:0; }
    div.stButton > button, div[data-testid="stFormSubmitButton"] button { background:#087f75 !important; color:#ffffff !important; -webkit-text-fill-color:#ffffff !important; border:0; border-radius:12px; padding:.72rem 1.2rem; font-weight:700; min-height:48px; }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover { background:#06665f !important; color:#ffffff !important; -webkit-text-fill-color:#ffffff !important; border:0; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-radius:10px; }
    .note { color:#40545d; font-size:.83rem; line-height:1.5; padding:.85rem 1rem; background:#f2f6f7; border-radius:12px; margin-top:1rem; }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


BASE_DIR = Path(__file__).resolve().parent

# The notebook ran df_encoded.astype(int), which cut Oldpeak (and the imputed
# values) down to whole numbers BEFORE the scaler/KNN were fitted. Doing the
# same here keeps app inputs on the same scale the model was trained on.
# Set to False if you retrain the model without that astype(int) step.
MATCH_TRAINING_OLDPEAK = True

# Ranges seen in the training data (from df.describe() in the notebook).
TRAINING_RANGES = {"age": (28, 77, "Age"), "max_hr": (60, 202, "Maximum heart rate")}

SEX = {"M": "Male", "F": "Female"}
CHEST = {"ATA": "Atypical angina", "NAP": "Non-anginal pain", "TA": "Typical angina", "ASY": "Asymptomatic"}
ECG = {"Normal": "Normal", "ST": "ST-T wave abnormality", "LVH": "Left ventricular hypertrophy"}
SLOPE = {"Up": "Upsloping", "Flat": "Flat", "Down": "Downsloping"}
YES_NO_YN = {"Y": "Yes", "N": "No"}

FIELD_ORDER = [
    ("age", "Age"), ("sex", "Sex"), ("chest_pain", "Chest pain type"),
    ("resting_bp", "Resting blood pressure"), ("cholesterol", "Cholesterol"),
    ("fasting_bs", "Fasting blood sugar > 120 mg/dL"), ("resting_ecg", "Resting ECG"),
    ("max_hr", "Maximum heart rate"), ("exercise_angina", "Exercise-induced angina"),
    ("oldpeak", "Oldpeak (ST depression)"), ("st_slope", "ST slope"),
]


def friendly(key, value):
    """Readable text for a stored input value."""
    if key == "age":
        return f"{value} years"
    if key == "sex":
        return SEX[value]
    if key == "chest_pain":
        return CHEST[value]
    if key == "resting_bp":
        return f"{value} mm Hg"
    if key == "cholesterol":
        return f"{value} mg/dL"
    if key == "fasting_bs":
        return "Yes" if value else "No"
    if key == "resting_ecg":
        return ECG[value]
    if key == "max_hr":
        return f"{value} bpm"
    if key == "exercise_angina":
        return YES_NO_YN[value]
    if key == "oldpeak":
        return f"{value:.1f}"
    if key == "st_slope":
        return SLOPE[value]
    return str(value)


@st.cache_resource
def load_artifacts():
    model = joblib.load(BASE_DIR / "knn_heart_model.pkl")
    scaler = joblib.load(BASE_DIR / "heart_scaler.pkl")
    columns = joblib.load(BASE_DIR / "heart_columns.pkl")
    return model, scaler, columns


def page_header(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">Heart health · Mini project</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def build_reminders(inputs, prediction):
    """Rule-based reminders from the last submitted form: list of (level, text)."""
    out = []
    if inputs["exercise_angina"] == "Y" or inputs["chest_pain"] in ("TA", "ATA"):
        out.append(("warning", "You entered chest-pain or exercise-related symptom information. Discuss it with a healthcare professional. Sudden or severe symptoms need urgent care."))
    if inputs["resting_bp"] >= 180:
        out.append(("error", "The blood pressure value entered is very high (180 or above). Contact a clinician promptly, and seek urgent care if you also have chest pain, severe headache, breathlessness or weakness."))
    elif inputs["resting_bp"] >= 140:
        out.append(("warning", "The blood pressure value entered is elevated. A single value does not diagnose a condition; discuss repeated high readings with a clinician."))
    if inputs["cholesterol"] >= 240:
        out.append(("warning", "The cholesterol value entered is high. Ask a clinician to interpret it with your full lipid results and health history."))
    elif inputs["cholesterol"] >= 200:
        out.append(("info", "The cholesterol value entered is in the borderline range (200–239 mg/dL). A clinician can tell you whether it needs follow-up."))
    if inputs["fasting_bs"] == 1:
        out.append(("warning", "You indicated fasting blood sugar above 120 mg/dL. Ask a healthcare professional how this result should be interpreted."))
    if inputs["oldpeak"] >= 2:
        out.append(("warning", "The ST depression (oldpeak) value entered is on the higher side. This comes from an exercise ECG, so ask a clinician to review it."))
    if inputs["st_slope"] in ("Flat", "Down") or inputs["resting_ecg"] != "Normal":
        out.append(("info", "Your ECG-related entries include a non-normal or flat/downsloping pattern. Only a clinician can say what this means for you."))
    if prediction == 1:
        out.append(("warning", "The model returned a higher-likelihood result. Arrange a discussion with a healthcare professional; this result is not a diagnosis."))
    return out


def show_message(level, text):
    {"error": st.error, "warning": st.warning, "info": st.info, "success": st.success}[level](text)


ACTION_TIPS = {
    "Ask a clinician about my blood pressure": [
        "Ask what blood pressure range is right for you.",
        "Ask how and when to measure it at home, and bring your readings to the visit.",
        "Ask whether salt intake, weight or medicines could be affecting it.",
    ],
    "Ask a clinician about cholesterol or blood sugar": [
        "Ask whether a full lipid profile or an HbA1c / fasting glucose test is due.",
        "Ask how often these should be repeated for you.",
        "Bring previous reports so trends can be compared.",
    ],
    "Plan a safe, regular activity routine": [
        "Ask a clinician what level of activity is safe for you, especially if you have symptoms.",
        "Start small and build up, for example short walks on most days.",
        "Stop and seek help if you get chest pain, severe breathlessness or dizziness.",
    ],
    "Add more heart-healthy foods to meals": [
        "Add vegetables, fruit, pulses, whole grains and nuts where you can.",
        "Go easy on salt, deep-fried food and sugary drinks.",
        "Change one meal a day first instead of everything at once.",
    ],
    "Ask for support to stop using tobacco": [
        "Tell a clinician or pharmacist you want to quit; support and medicines can double your chances.",
        "Pick a quit date and tell someone who can support you.",
        "Many regions have free quitline services; ask your clinician for local ones.",
    ],
    "Book or attend a routine health appointment": [
        "Write down your questions and any symptoms before the visit.",
        "Bring recent reports and a list of medicines.",
        "Ask when your next check-up should be.",
    ],
}

HABIT_TIPS = {
    "vegetables": ("Vegetables or fruit most days", "Add one extra serving of vegetables or fruit to a meal you already eat."),
    "activity": ("Regular, suitable physical activity", "Ask what is safe for you, then try a short daily walk."),
    "tobacco": ("Avoiding tobacco (or getting support to quit)", "A clinician or pharmacist can help you build a quit plan."),
    "appointments": ("Keeping up with checks and prescribed care", "Book the next routine check-up now so it is not forgotten."),
}

FOCUS_TIPS = {
    "Plan balanced meals": "Sketch three simple meals for this week that include vegetables and whole grains.",
    "Ask a clinician what activity is safe for me": "Write down your questions before the appointment, including any symptoms during exercise.",
    "Take a short activity break when appropriate": "Set a reminder to stand up and walk for a few minutes after long sitting, if it is safe for you.",
    "Ask for support with tobacco cessation": "Talk to a clinician or pharmacist about quit support options.",
    "Schedule a routine health check": "Choose a date this week and put it in your calendar.",
}

# Defaults live in session state (not in each widget) so a value can be kept
# when the user switches sections without Streamlit warning about two defaults.
DEFAULTS = {
    "w_page": "Heart Disease Prediction", "w_age": 40, "w_sex": "M", "w_chest_pain": "ATA",
    "w_resting_bp": 120, "w_cholesterol": 200, "w_fasting_bs": 0, "w_resting_ecg": "Normal",
    "w_max_hr": 150, "w_exercise_angina": "N", "w_oldpeak": 1.0, "w_st_slope": "Up",
    "w_actions": [], "w_field": "Age", "w_focus": next(iter(FOCUS_TIPS)),
    "w_habit_vegetables": False, "w_habit_activity": False, "w_habit_tobacco": False,
    "w_habit_appointments": False, "w_sym_chest": False, "w_sym_spread": False,
    "w_sym_breath": False, "w_sym_faint": False, "w_sym_sweat": False, "w_sym_other": False,
}
for _key, _val in DEFAULTS.items():
    st.session_state.setdefault(_key, _val)

# --- Keep widget values when the user switches sections ---------------------
# Streamlit forgets widgets that are not drawn on the current page. Re-saving
# every "w_" key on each run keeps entries and check-ins when navigating back.
for _key in [k for k in st.session_state if k.startswith("w_")]:
    st.session_state[_key] = st.session_state[_key]

PAGES = [
    "Heart Disease Prediction",
    "Suggestions",
    "Understand Your Inputs",
    "Heart Health Guide",
    "When to Seek Help",
]

with st.sidebar:
    st.markdown("## 💓 PulsePoint")
    st.caption("Heart health mini-project")
    page = st.radio("Choose a section", PAGES, key="w_page")
    st.markdown("---")
    st.caption("Educational project only. It cannot diagnose or treat a condition.")


# =============================================================== PREDICTION
if page == "Heart Disease Prediction":
    page_header(
        "A clearer view of your heart health",
        "Enter the clinical measurements below to see the result from the project’s prediction model.",
    )
    try:
        model, scaler, expected_columns = load_artifacts()
    except Exception as exc:
        st.error("The prediction files could not be loaded. Keep knn_heart_model.pkl, heart_scaler.pkl and heart_columns.pkl in the same folder as this app file, then restart the app.")
        st.caption(f"Details: {exc}")
        st.stop()

    st.markdown('<p class="section-title">Your information</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Use values from your report where available. If you are unsure, ask a healthcare professional.</p>', unsafe_allow_html=True)
    with st.form("prediction_form"):
        left, right = st.columns(2, gap="medium")
        with left:
            age = st.slider("Age", 18, 100, key="w_age")
            sex = st.selectbox("Sex", list(SEX), format_func=SEX.get, key="w_sex")
            chest_pain = st.selectbox("Chest pain type", list(CHEST), format_func=CHEST.get, key="w_chest_pain")
            resting_bp = st.number_input("Resting blood pressure (mm Hg)", 80, 200, key="w_resting_bp")
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, key="w_cholesterol")
        with right:
            fasting_bs = st.selectbox("Fasting blood sugar > 120 mg/dL", [0, 1], format_func=lambda x: "Yes" if x else "No", key="w_fasting_bs")
            resting_ecg = st.selectbox("Resting ECG", list(ECG), format_func=ECG.get, key="w_resting_ecg")
            max_hr = st.slider("Maximum heart rate", 60, 220, key="w_max_hr")
            exercise_angina = st.selectbox("Exercise-induced angina", list(YES_NO_YN), format_func=YES_NO_YN.get, key="w_exercise_angina")
            oldpeak = st.slider("Oldpeak (ST depression)", -3.0, 6.5, step=0.1, key="w_oldpeak")
            st_slope = st.selectbox("ST slope", list(SLOPE), format_func=SLOPE.get, key="w_st_slope")
        submitted = st.form_submit_button("Check prediction", use_container_width=True)

    if submitted:
        model_oldpeak = int(oldpeak) if MATCH_TRAINING_OLDPEAK else oldpeak  # int() truncates like astype(int)
        raw_input = {
            "Age": age,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs,
            "MaxHR": max_hr,
            "Oldpeak": model_oldpeak,
            "Sex_" + sex: 1,
            "ChestPainType_" + chest_pain: 1,
            "RestingECG_" + resting_ecg: 1,
            "ExerciseAngina_" + exercise_angina: 1,
            "ST_Slope_" + st_slope: 1,
        }
        # Dummy columns dropped during training (e.g. Sex_F, ChestPainType_ASY) are
        # discarded by reindex, which is exactly the "all zeros" baseline.
        input_df = pd.DataFrame([raw_input]).reindex(columns=expected_columns, fill_value=0)
        try:
            scaled = scaler.transform(input_df)
            prediction = int(model.predict(scaled)[0])
            disease_share = None
            if hasattr(model, "predict_proba") and 1 in list(model.classes_):
                disease_share = float(model.predict_proba(scaled)[0][list(model.classes_).index(1)])
            st.session_state["heart_prediction"] = prediction
            st.session_state["heart_disease_share"] = disease_share
            st.session_state["heart_k"] = getattr(model, "n_neighbors", None)
            st.session_state["heart_inputs"] = {
                "age": age,
                "sex": sex,
                "chest_pain": chest_pain,
                "resting_bp": resting_bp,
                "cholesterol": cholesterol,
                "fasting_bs": fasting_bs,
                "resting_ecg": resting_ecg,
                "max_hr": max_hr,
                "exercise_angina": exercise_angina,
                "oldpeak": oldpeak,
                "st_slope": st_slope,
            }
        except Exception as exc:
            st.error("The prediction could not be generated. Check that the input columns match the saved model.")
            st.caption(f"Details: {exc}")

    st.markdown("### Your result")
    if "heart_prediction" not in st.session_state:
        st.info("Complete the form and select **Check prediction** to see the model output.")
    else:
        if st.session_state["heart_prediction"] == 1:
            st.error("⚠️ The model indicates a higher likelihood of heart disease.")
            st.caption("This output is not a diagnosis. Please discuss health concerns and test results with a healthcare professional.")
        else:
            st.success("✅ The model indicates a lower likelihood of heart disease.")
            st.caption("A lower-likelihood result does not rule out heart disease. Seek medical advice if you have symptoms or concerns.")

        share = st.session_state.get("heart_disease_share")
        k = st.session_state.get("heart_k")
        if share is not None and k:
            st.progress(share, text=f"{round(share * k)} of the {k} most similar patients in the training data had heart disease")

        last = st.session_state["heart_inputs"]
        notes = []
        for key, (low, high, label) in TRAINING_RANGES.items():
            if not low <= last[key] <= high:
                notes.append(f"{label} ({last[key]}) is outside the {low}–{high} range in the training data, so the model is less reliable here.")
        for n in notes:
            st.warning(n)
        with st.expander("Values used for this result"):
            st.table(pd.DataFrame(
                [(label, friendly(key, last[key])) for key, label in FIELD_ORDER],
                columns=["Field", "Value"],
            ).set_index("Field"))
        st.caption("Changed something? Select **Check prediction** again to update the result.")
    st.markdown('<div class="note">This mini-project is for learning and demonstration. It cannot diagnose a condition or replace advice from a qualified healthcare professional.</div>', unsafe_allow_html=True)


# =============================================================== SUGGESTIONS
elif page == "Suggestions":
    page_header("Suggestions for your next steps", "Review simple reminders from the information you entered, then save practical actions for yourself.")
    inputs = st.session_state.get("heart_inputs")
    if inputs:
        st.markdown("### Reminders from your last submitted form")
        reminders = build_reminders(inputs, st.session_state.get("heart_prediction"))
        if reminders:
            for level, text in reminders:
                show_message(level, text)
        else:
            st.success("No specific reminder was triggered by these entered values. A lower-likelihood prediction does not rule out a health problem.")
    else:
        st.info("Submit the prediction form first to show reminders based on those entries.")

    st.markdown("### Choose your next steps")
    with st.form("suggestion_action_form"):
        chosen = st.multiselect("My next steps (pick one or more)", list(ACTION_TIPS), key="w_actions")
        submitted_action = st.form_submit_button("Save my next steps", use_container_width=True)
    if submitted_action:
        st.session_state["saved_heart_actions"] = list(chosen)
    saved = st.session_state.get("saved_heart_actions")
    if saved:
        st.success(f"Saved {len(saved)} next step{'s' if len(saved) != 1 else ''} for this session.")
        for action in saved:
            with st.expander(action, expanded=True):
                for tip in ACTION_TIPS[action]:
                    st.markdown(f"- {tip}")
    elif submitted_action:
        st.info("Nothing selected. Pick at least one step and save again.")
    st.caption("Suggestions are general reminders, not a treatment plan. This page uses simple rules and does not use a second prediction model.")


# =============================================================== UNDERSTAND
elif page == "Understand Your Inputs":
    page_header("Understand your prediction and inputs", "Explore what each form field means and see what you last entered. Your clinician should interpret clinical measurements.")
    fields = {
        "Age": ("Age in years.", "age"),
        "Sex": ("Sex category encoded in the training dataset.", "sex"),
        "Chest pain type": ("A category from the source dataset describing chest pain. It is not a self-diagnosis tool.", "chest_pain"),
        "Resting blood pressure": ("Blood pressure measured at rest, entered in mm Hg (the upper/systolic number). Many guidelines treat under 120 as normal, 130–139 as stage 1 and 140 or more as stage 2 high blood pressure, based on repeated readings.", "resting_bp"),
        "Cholesterol": ("The entered total cholesterol value in mg/dL. Under 200 is usually considered desirable, 200–239 borderline and 240 or more high. A complete lipid profile offers more context.", "cholesterol"),
        "Fasting blood sugar": ("Whether the value was above 120 mg/dL, as represented in this dataset.", "fasting_bs"),
        "Resting ECG": ("An ECG category from the dataset. Ask a clinician to explain your own report.", "resting_ecg"),
        "Maximum heart rate": ("Maximum heart rate recorded in the exercise test represented by the dataset.", "max_hr"),
        "Exercise-induced angina": ("Whether exercise-related angina was recorded. Any symptoms should be discussed with a clinician.", "exercise_angina"),
        "Oldpeak": ("A feature derived from an exercise ECG (ST depression). Enter it only if it is provided in your report.", "oldpeak"),
        "ST slope": ("A category from the exercise ECG in the source dataset; a clinician should interpret it.", "st_slope"),
    }
    inputs = st.session_state.get("heart_inputs")
    selected = st.selectbox("Select a field", list(fields.keys()), key="w_field")
    explanation, key = fields[selected]
    st.markdown(f"### {selected}")
    st.write(explanation)
    if inputs:
        st.info(f"Last submitted value: {friendly(key, inputs[key])}")
    else:
        st.info("No submitted prediction values are available in this session yet.")

    if inputs:
        with st.expander("Everything you last submitted"):
            st.table(pd.DataFrame(
                [(label, friendly(k, inputs[k])) for k, label in FIELD_ORDER],
                columns=["Field", "Value"],
            ).set_index("Field"))

    st.markdown("### What does the model result mean?")
    prediction = st.session_state.get("heart_prediction")
    if prediction is None:
        st.write("The app has not produced a prediction in this session. Submit the prediction form to see the model output here.")
    elif prediction == 1:
        st.warning("The KNN model returned class 1 (higher likelihood in its training labels). This is not a diagnosis and cannot estimate your complete personal risk.")
    else:
        st.success("The KNN model returned class 0 (lower likelihood in its training labels). This does not rule out disease or replace medical advice.")
    share = st.session_state.get("heart_disease_share")
    k = st.session_state.get("heart_k")
    if share is not None and k:
        st.write(f"K-Nearest Neighbours compares your entries with the {k} most similar patients in its training data and goes with the majority. Here, {round(share * k)} of {k} had heart disease.")
    try:
        n_features = len(load_artifacts()[2])
        feature_text = f"The model uses {n_features} encoded features and was"
    except Exception:
        feature_text = "The model was"
    st.caption(f"{feature_text} trained on a dataset of 918 records. It may be wrong, and its result depends on data quality and similarity to that dataset.")


# =============================================================== HABITS
elif page == "Heart Health Guide":
    page_header("Heart health habit check-in", "Mark the habits you are already working on and choose a small focus for this week.")

    def clear_checkin():
        for habit in HABIT_TIPS:
            st.session_state[f"w_habit_{habit}"] = False
        st.session_state["w_focus"] = list(FOCUS_TIPS)[0]
        st.session_state.pop("habit_checkin", None)

    with st.form("habit_checkin_form"):
        st.markdown("### Which habits are part of your routine?")
        st.checkbox("I include vegetables or fruit in meals most days", key="w_habit_vegetables")
        st.checkbox("I get regular physical activity that is suitable for me", key="w_habit_activity")
        st.checkbox("I avoid tobacco or am getting support to quit", key="w_habit_tobacco")
        st.checkbox("I keep up with health checks or prescribed care", key="w_habit_appointments")
        st.selectbox("My focus for this week", list(FOCUS_TIPS), key="w_focus")
        saved_checkin = st.form_submit_button("Save this check-in", use_container_width=True)
    if saved_checkin:
        st.session_state["habit_checkin"] = {
            "habits": {h: bool(st.session_state.get(f"w_habit_{h}", False)) for h in HABIT_TIPS},
            "focus": st.session_state["w_focus"],
        }
    checkin = st.session_state.get("habit_checkin")
    if checkin:
        count = sum(checkin["habits"].values())
        st.success(f"Check-in saved for this session: {count} of {len(HABIT_TIPS)} habits selected.")
        st.progress(count / len(HABIT_TIPS))
        st.info(f"Your focus: {checkin['focus']}. {FOCUS_TIPS[checkin['focus']]}")
        missing = [h for h, done in checkin["habits"].items() if not done]
        if missing:
            st.markdown("**Small ideas for habits not yet ticked**")
            for h in missing:
                name, tip = HABIT_TIPS[h]
                st.markdown(f"- **{name}:** {tip}")
        else:
            st.markdown("You ticked every habit. Keep it going, and keep your routine check-ups up to date.")
        st.button("Clear check-in", on_click=clear_checkin)
    else:
        st.caption("Your check-in will appear here after you save it. It is kept for this browser session only.")
    st.markdown("### Topics to discuss with a healthcare professional")
    st.write("Ask what blood pressure range is right for you, whether you need follow-up for cholesterol or blood sugar, what activity is appropriate, and whether your routine care is up to date.")
    st.caption("This check-in is for personal reflection, not a health score or medical assessment.")


# =============================================================== WHEN TO SEEK HELP
else:
    page_header("When to seek medical help", "Use this interactive reminder to decide whether to seek help. It cannot diagnose symptoms or confirm that you are safe.")
    st.markdown("### Are any of these happening now?")
    with st.form("symptom_check_form"):
        urgent_boxes = [
            st.checkbox("Severe, sudden, or persistent chest pain, pressure or tightness", key="w_sym_chest"),
            st.checkbox("Pain or discomfort spreading to the arm, shoulder, neck, jaw or back", key="w_sym_spread"),
            st.checkbox("Severe difficulty breathing", key="w_sym_breath"),
            st.checkbox("Fainting or feeling as if I may collapse", key="w_sym_faint"),
            st.checkbox("Cold sweat, nausea or vomiting together with chest discomfort", key="w_sym_sweat"),
            st.checkbox("Another symptom that feels immediately life-threatening", key="w_sym_other"),
        ]
        symptom_check = st.form_submit_button("Show guidance", use_container_width=True)
    if symptom_check:
        st.session_state["urgent_symptoms"] = any(urgent_boxes)
        st.session_state["symptom_check_done"] = True
    if st.session_state.get("symptom_check_done"):
        if st.session_state.get("urgent_symptoms"):
            st.error("Seek emergency medical help now. Contact your local emergency service or go to an emergency department. Do not wait for an app result, and do not drive yourself if you feel unwell.")
        else:
            st.info("You did not select one of the listed emergency symptoms. This does not confirm that everything is okay. Contact a healthcare professional for new, recurring, or worsening symptoms or any concern.")
    with st.expander("Emergency numbers"):
        st.markdown("- India: **112** (ambulance **108**)\n- United States / Canada: **911**\n- United Kingdom: **999**\n- European Union: **112**\n- Australia: **000**")
    st.markdown("### Also contact a healthcare professional")
    st.write("Ask for medical advice about new, recurring, worsening, or exercise-related chest discomfort, unusual breathlessness, or concerns about a measurement or prediction result.")
    st.caption("If you think this is an emergency, contact your local emergency service immediately. This checklist is not a diagnostic or triage tool.")

st.markdown("<div style='text-align:center;color:#829198;font-size:.8rem;margin-top:1.5rem'>Built by PulsePoint · Heart health prediction mini-project</div>", unsafe_allow_html=True)
