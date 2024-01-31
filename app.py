from flask import Flask, request, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = str(os.urandom(24))

# In-memory storage for demonstration purposes
users = {}
user_details = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users[username] = password
        session["username"] = username  # Set the username in the session
        return redirect(url_for("details"))
    return render_template("register.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        # No need to set session["username"] here since it should already be set during registration
        user_details[session["username"]] = {
            "username": session["username"],  # Include the username in the user_details
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
        }
        return redirect(url_for("info"))
    # You might want to ensure that the user is logged in or redirect to the login page
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("details.html", username=session.get("username"))


@app.route("/info")
def info():
    username = session.get("username")
    if not username or username not in user_details:
        return redirect(url_for("register"))
    # Pass both the details and the username to the template
    return render_template(
        "info.html", details=user_details[username], username=username
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("info"))
        else:
            return "Invalid username or password", 401
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
