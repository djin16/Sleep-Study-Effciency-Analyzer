import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Page Setting
# -----------------------------
st.set_page_config(
    page_title="Sleep & Study Efficiency Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sleep & Study Efficiency Analyzer")
st.write(
    "This project analyzes how sleep hours, sleep quality, study hours, "
    "and screen time before bed may affect student study efficiency."
)


# -----------------------------
# Sample Data Generator
# -----------------------------
def generate_sample_data():
    np.random.seed(42)

    students = [f"Student_{i}" for i in range(1, 31)]

    sleep_hours = np.random.normal(7, 1.2, 30).round(1)
    sleep_hours = np.clip(sleep_hours, 4, 10)

    sleep_quality = np.random.randint(4, 11, 30)
    study_hours = np.random.normal(3.5, 1.2, 30).round(1)
    study_hours = np.clip(study_hours, 1, 7)

    screen_time = np.random.normal(2.5, 1.0, 30).round(1)
    screen_time = np.clip(screen_time, 0, 6)

    # Simple formula to simulate study efficiency
    efficiency = (
        sleep_hours * 8
        + sleep_quality * 4
        + study_hours * 6
        - screen_time * 5
        + np.random.normal(0, 6, 30)
    )

    efficiency = np.clip(efficiency, 40, 100).round(1)

    df = pd.DataFrame({
        "Student": students,
        "Sleep Hours": sleep_hours,
        "Sleep Quality": sleep_quality,
        "Study Hours": study_hours,
        "Screen Time Before Bed": screen_time,
        "Study Efficiency Score": efficiency
    })

    return df


# -----------------------------
# Analysis Functions
# -----------------------------
def classify_efficiency(score):
    if score >= 85:
        return "High"
    elif score >= 70:
        return "Medium"
    else:
        return "Low"


def give_recommendation(row):
    recommendations = []

    if row["Sleep Hours"] < 6:
        recommendations.append("Try to sleep at least 7 hours.")
    if row["Sleep Quality"] < 6:
        recommendations.append("Improve sleep quality by keeping a regular sleep schedule.")
    if row["Screen Time Before Bed"] > 2:
        recommendations.append("Reduce screen time before bed.")
    if row["Study Hours"] < 2:
        recommendations.append("Increase daily study time.")

    if not recommendations:
        return "Current habits look balanced."

    return " ".join(recommendations)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Options")

data_option = st.sidebar.radio(
    "Choose data source:",
    ["Use Sample Data", "Upload CSV"]
)


# -----------------------------
# Load Data
# -----------------------------
if data_option == "Use Sample Data":
    df = generate_sample_data()
else:
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file or choose sample data.")
        st.stop()


# -----------------------------
# Add Classification and Recommendation
# -----------------------------
df["Efficiency Level"] = df["Study Efficiency Score"].apply(classify_efficiency)
df["Recommendation"] = df.apply(give_recommendation, axis=1)


# -----------------------------
# Show Dataset
# -----------------------------
st.subheader("Dataset")
st.dataframe(df)


# -----------------------------
# Key Metrics
# -----------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Sleep Hours", round(df["Sleep Hours"].mean(), 2))

with col2:
    st.metric("Average Study Hours", round(df["Study Hours"].mean(), 2))

with col3:
    st.metric("Average Screen Time", round(df["Screen Time Before Bed"].mean(), 2))

with col4:
    st.metric("Average Efficiency Score", round(df["Study Efficiency Score"].mean(), 2))


# -----------------------------
# Correlation Analysis
# -----------------------------
st.subheader("Correlation Analysis")

numeric_df = df[
    [
        "Sleep Hours",
        "Sleep Quality",
        "Study Hours",
        "Screen Time Before Bed",
        "Study Efficiency Score"
    ]
]

correlation = numeric_df.corr()

st.write("This table shows how each variable is related to study efficiency.")
st.dataframe(correlation)


# -----------------------------
# Charts
# -----------------------------
st.subheader("Visual Analysis")

chart_option = st.selectbox(
    "Choose a chart:",
    [
        "Sleep Hours vs Study Efficiency",
        "Sleep Quality vs Study Efficiency",
        "Study Hours vs Study Efficiency",
        "Screen Time vs Study Efficiency",
        "Efficiency Level Count"
    ]
)

if chart_option == "Sleep Hours vs Study Efficiency":
    fig, ax = plt.subplots()
    ax.scatter(df["Sleep Hours"], df["Study Efficiency Score"])
    ax.set_xlabel("Sleep Hours")
    ax.set_ylabel("Study Efficiency Score")
    ax.set_title("Sleep Hours vs Study Efficiency")
    st.pyplot(fig)

elif chart_option == "Sleep Quality vs Study Efficiency":
    fig, ax = plt.subplots()
    ax.scatter(df["Sleep Quality"], df["Study Efficiency Score"])
    ax.set_xlabel("Sleep Quality")
    ax.set_ylabel("Study Efficiency Score")
    ax.set_title("Sleep Quality vs Study Efficiency")
    st.pyplot(fig)

elif chart_option == "Study Hours vs Study Efficiency":
    fig, ax = plt.subplots()
    ax.scatter(df["Study Hours"], df["Study Efficiency Score"])
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Study Efficiency Score")
    ax.set_title("Study Hours vs Study Efficiency")
    st.pyplot(fig)

elif chart_option == "Screen Time vs Study Efficiency":
    fig, ax = plt.subplots()
    ax.scatter(df["Screen Time Before Bed"], df["Study Efficiency Score"])
    ax.set_xlabel("Screen Time Before Bed")
    ax.set_ylabel("Study Efficiency Score")
    ax.set_title("Screen Time Before Bed vs Study Efficiency")
    st.pyplot(fig)

else:
    level_counts = df["Efficiency Level"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(level_counts.index, level_counts.values)
    ax.set_xlabel("Efficiency Level")
    ax.set_ylabel("Number of Students")
    ax.set_title("Study Efficiency Level Count")
    st.pyplot(fig)


# -----------------------------
# Student Prediction Section
# -----------------------------
st.subheader("Personal Study Efficiency Estimator")

st.write("Enter your own study habits to estimate your study efficiency score.")

col1, col2 = st.columns(2)

with col1:
    user_sleep_hours = st.slider("Your Sleep Hours", 4.0, 10.0, 7.0, 0.5)
    user_sleep_quality = st.slider("Your Sleep Quality", 1, 10, 7)

with col2:
    user_study_hours = st.slider("Your Study Hours", 1.0, 8.0, 3.0, 0.5)
    user_screen_time = st.slider("Your Screen Time Before Bed", 0.0, 6.0, 2.0, 0.5)


if st.button("Estimate My Study Efficiency"):
    estimated_score = (
        user_sleep_hours * 8
        + user_sleep_quality * 4
        + user_study_hours * 6
        - user_screen_time * 5
    )

    estimated_score = max(40, min(100, estimated_score))
    estimated_score = round(estimated_score, 1)

    level = classify_efficiency(estimated_score)

    st.success(f"Estimated Study Efficiency Score: {estimated_score}")
    st.info(f"Efficiency Level: {level}")

    user_data = pd.DataFrame({
        "Sleep Hours": [user_sleep_hours],
        "Sleep Quality": [user_sleep_quality],
        "Study Hours": [user_study_hours],
        "Screen Time Before Bed": [user_screen_time],
        "Study Efficiency Score": [estimated_score]
    })

    user_data["Recommendation"] = user_data.apply(give_recommendation, axis=1)

    st.write("Recommendation:")
    st.write(user_data["Recommendation"].iloc[0])


# -----------------------------
# Insights
# -----------------------------
st.subheader("Project Insights")

avg_sleep = df["Sleep Hours"].mean()
avg_screen = df["Screen Time Before Bed"].mean()
avg_efficiency = df["Study Efficiency Score"].mean()

st.write(
    f"The average sleep duration in this dataset is **{avg_sleep:.2f} hours**, "
    f"and the average study efficiency score is **{avg_efficiency:.2f}**."
)

st.write(
    "Based on this analysis, students with better sleep quality and lower screen time before bed "
    "tend to have higher study efficiency scores. This suggests that study performance is not only "
    "related to how long students study, but also to their sleep habits and daily routine."
)


# -----------------------------
# Download Results
# -----------------------------
st.subheader("Download Analyzed Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Results",
    data=csv,
    file_name="sleep_study_efficiency_results.csv",
    mime="text/csv"
)


# -----------------------------
# Resume Description
# -----------------------------
st.subheader("Resume Description")

st.code(
    "Built a Sleep & Study Efficiency Analyzer using Python and Streamlit to analyze "
    "how sleep hours, sleep quality, study time, and screen time before bed affect student "
    "learning efficiency. Created visualizations, correlation analysis, personalized recommendations, "
    "and an interactive efficiency estimator.",
    language="text"
)
