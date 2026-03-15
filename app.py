# -----------------------------------------
# CGPA Calculator with Performance Graph
# Run using: streamlit run app.py
# -----------------------------------------

import streamlit as st
import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


st.set_page_config(page_title="CGPA Calculator", page_icon="📊")

# Grade mapping
grade_to_point = {
    "O":10,
    "A+":9,
    "A":8,
    "B+":7,
    "B":6,
    "C":5,
    "RA":0
}

grades = list(grade_to_point.keys())

# ---------------- CGPA CALCULATION ----------------

def calculate_cgpa(grade_points, credits):
    total_points = sum(g*c for g,c in zip(grade_points,credits))
    total_credits = sum(credits)

    if total_credits == 0:
        return 0

    return total_points / total_credits

# ---------------- QUOTES ----------------

def show_quote(cgpa):
    st.subheader("Motivation")

    if cgpa >= 9:
        st.success("🌟 Excellent! Your hard work is paying off!")
    elif cgpa >= 8:
        st.success("👏 Great job! Keep pushing higher!")
    elif cgpa >= 7:
        st.info("👍 Good work! A little more effort can push you higher!")
    elif cgpa >= 6:
        st.warning("⚡ You can improve. Stay focused!")
    else:
        st.error("💡 Don't give up! Work harder next semester!")

# ---------------- CGPA GRAPH (Bar Chart) ----------------

def plot_cgpa_progress(grade_points, credits):
    cumulative_cgpa=[]
    cumulative_points=0
    cumulative_credits=0

    for g,c in zip(grade_points,credits):
        cumulative_points += g*c
        cumulative_credits += c
        cumulative_cgpa.append(cumulative_points/cumulative_credits)

    subjects = list(range(1,len(cumulative_cgpa)+1))

    fig, ax = plt.subplots()

    # Bar chart
    ax.bar(subjects, cumulative_cgpa, color='royalblue', alpha=0.7)

    # Add value labels on top of each bar
    for i, v in enumerate(cumulative_cgpa):
        ax.text(i+1, v + 0.1, f"{v:.2f}", ha='center', fontweight='bold')

    ax.set_xlabel("Number of Subjects Completed")
    ax.set_ylabel("CGPA")
    ax.set_title("CGPA Performance Progress")
    ax.set_ylim(0,10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # Footer
    st.markdown("<p style='text-align:right; color:gray;'>Made by SABARI GIRI</p>", unsafe_allow_html=True)

# ---------------- UI ----------------

st.title("📊 CGPA Calculator")
st.write("Calculate CGPA manually or upload a marksheet image.")

option = st.radio(
    "Choose Input Method",
    ["Enter Grades Manually","Upload Marksheet Image"]
)

# ================= MANUAL =================

if option == "Enter Grades Manually":
    subjects = int(
        st.number_input(
            "Number of Subjects",
            min_value=1,
            max_value=12,
            value=5
        )
    )

    grades_selected=[]
    credits=[]

    for i in range(subjects):
        st.subheader(f"Subject {i+1}")
        col1,col2 = st.columns(2)

        grade = col1.selectbox("Grade",grades,key=i)
        credit = col2.number_input(
            "Credit",
            min_value=1.0,
            max_value=10.0,
            step=0.5,
            value=3.0,
            key=f"c{i}"
        )

        grades_selected.append(grade)
        credits.append(credit)

    if st.button("Calculate CGPA"):
        grade_points=[grade_to_point[g] for g in grades_selected]
        cgpa = calculate_cgpa(grade_points,credits)
        st.success(f"CGPA: {cgpa:.2f}")
        show_quote(cgpa)
        st.subheader("📊 CGPA Performance Graph")
        plot_cgpa_progress(grade_points,credits)

# ================= IMAGE UPLOAD =================

if option == "Upload Marksheet Image":
    uploaded_image = st.file_uploader(
        "Upload Marksheet Image",
        type=["png","jpg","jpeg"]
    )

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image,width=400)
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        st.subheader("Detected Text")
        st.text(text)

        grades_found=[]
        credits_found=[]
        words = text.split()

        # detect grades
        for word in words:
            if word in grade_to_point:
                grades_found.append(word)

        # detect credits
        for word in words:
            if word.isdigit():
                credits_found.append(int(word))

        if len(grades_found)>0 and len(credits_found)>0:
            credits_found = credits_found[:len(grades_found)]
            grade_points=[grade_to_point[g] for g in grades_found]
            cgpa = calculate_cgpa(grade_points,credits_found)
            st.success(f"Calculated CGPA: {cgpa:.2f}")
            show_quote(cgpa)
            st.subheader("📊 CGPA Performance Graph")
            plot_cgpa_progress(grade_points,credits_found)
        else:
            st.error("Could not detect grades or credits properly.")

            # Footer with LinkedIn
# Footer with LinkedIn + GitHub
st.markdown(
    """
    <hr>
    <div style='text-align:center; font-size:16px;'>

    Made by <b>SABARI GIRI ❤️</b><br><br>

    <a href="https://www.linkedin.com/in/sabari-giri-57728032a" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25">
        LinkedIn
    </a>

    &nbsp;&nbsp;&nbsp;

    <a href="https://github.com/24243086-ai" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" width="25">
        GitHub
    </a>

    </div>
    """,
    unsafe_allow_html=True
)
