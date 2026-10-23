
import streamlit as st


def show_dashboard():
    st.markdown("""
    <style>
    .stApp {
        background-color: #F5F8FF;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }

    .dash-hero {
        background: linear-gradient(135deg, #E5EDFF, #FFFFFF);
        border: 1px solid #D8E4FA;
        border-radius: 22px;
        padding: 32px;
        margin: 15px 0 25px 0;
    }

    .dash-hero h1 {
        color: #18366D;
        font-size: 36px;
    }

    .dash-hero p {
        color: #526582;
        font-size: 16px;
    }

    .dash-card {
        background: white;
        border: 1px solid #DCE6F8;
        border-radius: 15px;
        padding: 22px;
        min-height: 150px;
        margin-bottom: 12px;
    }

    .dash-card h3 {
        color: #2458D3;
    }
    </style>
    """, unsafe_allow_html=True)

    email = st.session_state.get("user_email", "User")

    st.title("📄 ResumeAI Dashboard")

    st.markdown(f"""
    <div class="dash-hero">
        <h1>Welcome back!</h1>
        <p>Logged in as: {email}</p>
        <p>Analyze your resume, check your job match, and discover ways to improve your career profile.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Workspace")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="dash-card">
            <h3>📊 Resume Analysis</h3>
            <p>Upload your resume and review your ATS and job match scores.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Resume Analysis", type="primary",
                     use_container_width=True):
            st.session_state["page"] = "analyzer"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="dash-card">
            <h3>💡 Improve Your Resume</h3>
            <p>Get AI-powered feedback, missing skills, and improvement tips.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Improvement Tips", use_container_width=True):
            st.session_state["page"] = "analyzer"
            st.rerun()

    st.divider()

    st.subheader("Quick Guide")

    a, b, c = st.columns(3)

    a.markdown("### 1. Upload")
    a.write("Select your resume in PDF format.")

    b.markdown("### 2. Analyze")
    b.write("Compare it with your target job description.")

    c.markdown("### 3. Improve")
    c.write("Use the scores and suggestions to refine your resume.")

    st.divider()

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("user_email", None)
        st.session_state["page"] = "auth"
        st.rerun()

    st.caption("ResumeAI | AI-assisted resume analysis")
