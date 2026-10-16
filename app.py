import os
from flask import Flask, jsonify
from models import db
from models import User, Resume, Analysis

app = Flask(__name__)

# Database configuration
os.makedirs(app.instance_path, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(app.instance_path, "database.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>AI Resume Analyzer</title>
            <meta name="viewport"
                  content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #eef4ff;
                    text-align: center;
                    padding: 60px 15px;
                }
                .card {
                    max-width: 550px;
                    margin: auto;
                    padding: 30px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 4px 20px #d5deee;
                }
                h1 { color: #2563eb; }
                p { color: #475569; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>AI Resume Analyzer</h1>
                <p>Your smart resume analysis project starts here!</p>
                <p>Resume analysis features are coming next.</p>
            </div>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "project": "AI Resume Analyzer"
    })


if __name__ == "__main__":
    app.run(debug=True)
