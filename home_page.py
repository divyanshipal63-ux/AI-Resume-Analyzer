
import streamlit as st


def show_home():

    st.markdown("""
    <style>
    .stApp {
        background-color: #F5F8FF;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    .hero {
        background: linear-gradient(135deg, #E5EDFF, #FFFFFF);
        border: 1px solid #D8E4FA;
        border-radius: 22px;
        padding: 45px 35px;
        margin: 20px 0;
    }

    .hero h1 {
        color: #18366D;
        font-size: 46px;
        line-height: 1.2;
    }

    .hero p {
        color: #526582;
        font-size: 17px;
        line-height: 1.7;
    }

    .feature {
        background: white;
        border: 1px solid #DCE6F8;
        border-radius: 15px;
        padding: 22px;
        min-height: 170px;
        margin-bottom: 14px;
    }

    .feature h3 {
        color: #2458D3;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📄 ResumeAI")

    st.markdown("""
    <div class="hero">
        <p><b>YOUR CAREER, YOUR NEXT STEP</b></p>
        <h1>Build a Resume That Gets Noticed.</h1>
        <p>
        Analyze your resume, compare it with your target job,
        discover missing skills, and get AI-powered suggestions
        to improve your resume.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "✨ Get Started — Analyze My Resume",
        type="primary",
        use_container_width=True
    ):
        st.session_state["page"] = "analyzer"
        st.rerun()

    st.subheader("Everything You Need")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature">
            <h3>📊 Resume Match</h3>
            <p>Compare your resume with a job description.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature">
            <h3>🎯 Skill Gap Analysis</h3>
            <p>Identify missing skills for your target role.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature">
            <h3>🤖 AI Insights</h3>
            <p>Understand your strengths and weaknesses.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature">
            <h3>💡 Improvement Tips</h3>
            <p>Get suggestions to improve your resume.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("How It Works")

    a, b, c = st.columns(3)

    a.markdown("### 1. Upload")
    a.write("Upload your resume in PDF format.")

    b.markdown("### 2. Compare")
    b.write("Paste your target job description.")

    c.markdown("### 3. Improve")
    c.write("Review scores and AI suggestions.")

    st.divider()

    st.caption(
        "ResumeAI | AI-assisted resume analysis"
    )
