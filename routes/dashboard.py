
from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)


def login_required(view_function):
    """Redirect users to login if they are not authenticated."""
    from functools import wraps

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapped_view


@dashboard_bp.route("/dashboard")
@login_required
def index():
    """Display the logged-in user's dashboard."""
    user_name = session.get("user_name", "User")

    return render_template(
        "dashboard.html",
        user_name=user_name
    )
