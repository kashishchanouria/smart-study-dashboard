import os
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from utils import init_db, save_history, load_history, smart_suggestion, logical_adjustment

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="AI Study Planner", page_icon="📘", layout="wide")
init_db()

# -------------------------
# Load model
# -------------------------
MODEL_PATH = "model/study_model.pkl"
FEATURE_PATH = "model/feature_columns.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURE_PATH):
    st.error("Model files not found. Please run train_model.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURE_PATH)

# -------------------------
# Demo login
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

DEMO_USERS = {
    "student1": "1234",
    "student2": "1234",
    "admin": "admin123"
}

def login_view():
    st.title("🔐 Login")
    st.write("login system for project presentation")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if username in DEMO_USERS and DEMO_USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

if not st.session_state.logged_in:
    login_view()
    st.stop()

# -------------------------
# Sidebar
# -------------------------
st.sidebar.success(f"Logged in as: {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.title("📘 AI-Powered Study Planner")
st.caption("Predict score, save history, get smart study plan, and track progress")

tabs = st.tabs(["🎯 Prediction", "📝 Daily Tracker", "🧠 Smart Suggestions", "📊 Graph & History"])

# -------------------------
# TAB 1: Prediction
# -------------------------
with tabs[0]:
    st.subheader("Predict Study Score")

    col1, col2 = st.columns(2)

    with col1:
        sleep = st.number_input("Sleep Hours", min_value=1, max_value=12, value=7, step=1)
        focus = st.number_input("Focus Score", min_value=1, max_value=10, value=5, step=1)

    with col2:
        study_hours = st.number_input("Study Hours", min_value=0, max_value=12, value=3, step=1)
        breaks = st.number_input("Breaks", min_value=0, max_value=10, value=1, step=1)

    if st.button("Predict Score"):
        input_data = pd.DataFrame([{
            "sleep": sleep,
            "focus": focus,
            "study_hours": study_hours,
            "breaks": breaks
        }])

        raw_pred = model.predict(input_data)[0]
        final_pred = logical_adjustment(raw_pred, sleep, focus, study_hours, breaks)

        st.success(f"Predicted Study Score: {final_pred}/100")
        st.progress(int(final_pred))

        save_history(
            username=st.session_state.username,
            sleep=sleep,
            focus=focus,
            study_hours=study_hours,
            breaks=breaks,
            predicted_score=final_pred
        )

        st.info("Prediction saved in tracker.")

# -------------------------
# TAB 2: Daily Tracker
# -------------------------
with tabs[1]:
    st.subheader("Daily Tracker")

    history = load_history(st.session_state.username)

    if history.empty:
        st.warning("No history found yet. Make a prediction first.")
    else:
        show_df = history[["created_at", "sleep", "focus", "study_hours", "breaks", "predicted_score"]]
        st.dataframe(show_df, use_container_width=True)

        csv_data = show_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download History CSV",
            csv_data,
            file_name="study_history.csv",
            mime="text/csv"
        )

# -------------------------
# TAB 3: Smart Suggestions
# -------------------------
with tabs[2]:
    st.subheader("Smart AI Suggestions")

    c1, c2 = st.columns(2)
    with c1:
        subject = st.selectbox("Subject", ["Math", "Physics", "CS", "History", "Accounts"])
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    with c2:
        days_left = st.number_input("Days Left for Exam", min_value=1, max_value=365, value=10, step=1)
        daily_hours = st.number_input("Daily Study Hours", min_value=1, max_value=24, value=4, step=1)

    focus2 = st.number_input("Current Focus Score", min_value=1, max_value=10, value=5, step=1, key="focus2")
    sleep2 = st.number_input("Current Sleep Hours", min_value=1, max_value=12, value=7, step=1, key="sleep2")

    if st.button("Generate Study Plan"):
        plan = smart_suggestion(
            subject=subject,
            difficulty=difficulty,
            days_left=days_left,
            daily_hours=daily_hours,
            focus=focus2,
            sleep=sleep2,
            username=st.session_state.username
        )
        st.text_area("Your Personalized Study Plan", plan, height=280)

        save_history(
            username=st.session_state.username,
            sleep=sleep2,
            focus=focus2,
            study_hours=daily_hours,
            breaks=1,
            predicted_score=0,
            subject=subject,
            difficulty=difficulty,
            plan=plan
        )

# -------------------------
# TAB 4: Graph & History
# -------------------------
with tabs[3]:
    st.subheader("Progress Graph")

    graph_history = load_history(st.session_state.username)

    if graph_history.empty:
        st.warning("No data available yet.")
    else:
        graph_history = graph_history.sort_values("id")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(graph_history["id"], graph_history["study_hours"], marker="o", label="Study Hours")
        ax.plot(graph_history["id"], graph_history["predicted_score"], marker="o", label="Predicted Score")
        ax.set_xlabel("Entry")
        ax.set_ylabel("Value")
        ax.set_title("Study Hours and Predicted Score Trend")
        ax.legend()
        st.pyplot(fig)

        st.subheader("Recent Entries")
        st.dataframe(
            graph_history[["created_at", "subject", "difficulty", "study_hours", "predicted_score", "plan"]],
            use_container_width=True
        )