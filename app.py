from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    user_role = session.get("role", "tourist")
    return render_template("index.html", user_role=user_role)

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/session")
def check_session():
    return f"Current session data: {dict(session)}"

if __name__ == "__main__":
    app.run(debug=True)
