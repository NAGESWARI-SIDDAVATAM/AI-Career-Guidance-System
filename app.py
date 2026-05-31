import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Career Guidance System", page_icon="🎓")

SKILLS = [
    "Python","SQL","Machine Learning","Data Analysis","Power BI",
    "Excel","Java","Web Development","Communication","Leadership"
]

CAREERS = {
    "Data Scientist": {
        "skills":["Python","SQL","Machine Learning","Data Analysis"],
        "roadmap":["Learn Python","Learn Statistics","Build ML Projects","Study Deep Learning"]
    },
    "Data Analyst": {
        "skills":["SQL","Excel","Power BI","Data Analysis"],
        "roadmap":["Excel","SQL","Power BI","Dashboard Projects"]
    },
    "ML Engineer": {
        "skills":["Python","Machine Learning","SQL"],
        "roadmap":["Python","ML Algorithms","MLOps Basics","Deploy Models"]
    },
    "Software Developer": {
        "skills":["Java","Web Development"],
        "roadmap":["DSA","Projects","Git/GitHub","System Design Basics"]
    }
}

def extract_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_skills(text):
    found = []
    text = text.lower()
    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            found.append(skill)
    return found

st.title("🎓 AI Career Guidance System")

name = st.text_input("Enter your name")

st.subheader("Select Your Skills")
selected_skills = []
cols = st.columns(2)

for i, skill in enumerate(SKILLS):
    if cols[i % 2].checkbox(skill):
        selected_skills.append(skill)

st.subheader("📄 Upload Resume (Optional)")
resume = st.file_uploader("Upload PDF Resume", type=["pdf"])

resume_skills = []
if resume:
    text = extract_text(resume)
    resume_skills = extract_skills(text)
    st.success(f"Skills found in resume: {', '.join(resume_skills) if resume_skills else 'None'}")

all_skills = list(set(selected_skills + resume_skills))

if st.button("Get Career Recommendations"):
    if not all_skills:
        st.warning("Please select skills or upload a resume.")
    else:
        scores = {}
        for career, info in CAREERS.items():
            match = len(set(all_skills).intersection(info["skills"]))
            scores[career] = match

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        st.subheader("🚀 Recommended Careers")
        for career, score in ranked[:3]:
            st.write(f"### {career}")
            st.write(f"Skill Match Score: {score}")
            st.write("Roadmap:")
            for step in CAREERS[career]["roadmap"]:
                st.write(f"- {step}")

        st.subheader("📈 Your Skills")
        st.write(", ".join(all_skills))
