
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

auth_bp = Blueprint("auth", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "instance" / "database.db"


def get_db_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_auth_table():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO users (name, email, password)
                    VALUES (?, ?, ?)
                    """,
                    (name, email, password_hash),
                )

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "error")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db_connection() as connection:
            user = connection.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,),
            ).fetchone()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login successful.", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
