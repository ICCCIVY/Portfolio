import os
from flask import Flask, redirect, url_for, session, request, render_template
from flask_session import Session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "something-random"  # 🔐 You can change this to something secure
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
    'scope': 'openid email profile',
    'prompt': 'consent'}

)

@app.route("/")
def index():
    user_role = session.get("role", "tourist")
    username = session.get("username", None)
    return render_template("index.html", user_role=user_role, username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "Qiyu" and password == "123456":
            session["role"] = "admin"
            session["username"] = "Qiyu"
            return redirect("/")
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")

@app.route("/login/google")
def login_google():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/login/google/authorized")
def authorize():
    token = google.authorize_access_token()
    user_info = google.get("https://openidconnect.googleapis.com/v1/userinfo").json()
    session["username"] = user_info["name"]
    session["role"] = "admin"  # or however you'd like to classify
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/session")
def check_session():
    return f"Current session data: {dict(session)}"

if __name__ == "__main__":
    app.run(debug=True)

