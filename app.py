from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a real secret key

# In-memory storage for demonstration purposes
users = {}
user_details = {}


@app.route("/")
def home():
    return render_template("templates/home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users[username] = password
        return redirect(url_for("details"))
    return render_template("templates/register.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    if request.method == "POST":
        session["username"] = request.form["username"]
        user_details[session["username"]] = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
        }
        return redirect(url_for("display_info"))
    return render_template("templates/details.html", username=session.get("username"))


@app.route("/info")
def display_info():
    username = session.get("username")
    if not username or username not in user_details:
        return redirect(url_for("templates/register"))
    return render_template("templates/info.html", details=user_details[username])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("templates/info"))
        else:
            return "Invalid username or password", 401
    return render_template("templates/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
