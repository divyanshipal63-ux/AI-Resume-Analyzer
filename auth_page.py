
import streamlit as st
import sqlite3
import hashlib
import secrets
import hmac

DB_PATH = "users.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        200000
    ).hex()


def register_user(email, password):
    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (email, salt, password_hash) VALUES (?, ?, ?)",
                (email, salt, password_hash)
            )
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(email, password):
    with sqlite3.connect(DB_PATH) as conn:
        user = conn.execute(
            "SELECT salt, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

    if user is None:
        return False

    salt, saved_hash = user
    entered_hash = hash_password(password, salt)

    return hmac.compare_digest(entered_hash, saved_hash)


def show_auth():
    init_db()

    st.markdown("""
    <style>
    .auth-heading {
        text-align: center;
        color: #18366D;
        font-size: 34px;
        font-weight: 700;
    }
    .auth-subtitle {
        text-align: center;
        color: #526582;
        margin-bottom: 24px;
    }
    .stApp {
        background-color: #F5F8FF;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="auth-heading">Welcome to ResumeAI</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="auth-subtitle">Sign in or create an account to continue.</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.5, 1])

    with center:
        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            st.subheader("Welcome Back!")

            with st.form("login_form"):
                login_email = st.text_input(
                    "Email Address",
                    key="login_email"
                ).strip().lower()

                login_password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )

                login_submit = st.form_submit_button(
                    "Login",
                    type="primary",
                    use_container_width=True
                )

            if login_submit:
                if not login_email or not login_password:
                    st.error("Please enter your email and password.")
                elif verify_user(login_email, login_password):
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = login_email
                    st.session_state["page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        with register_tab:
            st.subheader("Create Your Account")

            with st.form("register_form"):
                register_email = st.text_input(
                    "Email Address",
                    key="register_email"
                ).strip().lower()

                register_password = st.text_input(
                    "Create Password",
                    type="password",
                    key="register_password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                register_submit = st.form_submit_button(
                    "Create Account",
                    type="primary",
                    use_container_width=True
                )

            if register_submit:
                if not register_email or not register_password:
                    st.error("Please fill in all fields.")
                elif "@" not in register_email or "." not in register_email:
                    st.error("Please enter a valid email address.")
                elif len(register_password) < 8:
                    st.error("Password must be at least 8 characters.")
                elif register_password != confirm_password:
                    st.error("Passwords do not match.")
                elif register_user(register_email, register_password):
                    st.success("Account created! Please open the Login tab.")
                else:
                    st.error("An account with this email already exists.")

        st.divider()

        if st.button("← Back to Home", use_container_width=True):
            st.session_state["page"] = "home"
            st.rerun()
