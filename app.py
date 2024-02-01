from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    session,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"txt"}

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # Set the UPLOAD_FOLDER in app config


# In-memory storage for demonstration purposes
users = {}
user_details = {}
file_details = {}  # Store the file details
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
        # Handle file upload
        f = request.files.get("file")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            # Read the content of the file
            contents = f.read().decode("utf-8")  # Assuming the file is UTF-8 encoded
            words = contents.split()
            word_count = len(words)

            # Append the word count to the content
            updated_contents = f"{contents}\nWord Count: {word_count}"

            # Save the updated content back to the file
            with open(file_path, "w") as f:
                f.write(updated_contents)

            # Store file details
            file_details[session["username"]] = {
                "filename": filename,
                "word_count": word_count,
            }
        user_details[session["username"]] = {
            "username": session["username"],  # Include the username in the user_details
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
        }
        return redirect(url_for("info"))
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("details.html", username=session.get("username"))


@app.route("/info")
def info():
    username = session.get("username")
    if not username or username not in user_details:
        return redirect(url_for("register"))
    # Get file details if available
    file_info = file_details.get(username, {})
    # Pass both the details and the username to the template
    return render_template(
        "info.html",
        details=user_details[username],
        username=username,
        file_info=file_info,
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


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
