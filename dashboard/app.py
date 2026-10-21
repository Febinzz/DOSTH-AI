from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from array import array
import math
import tempfile
import wave
import os
import hmac
from flask import jsonify


app = Flask(__name__)
app.secret_key = os.environ.get("CAREMATE_SECRET_KEY") or os.urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("dhost.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS interaction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            emotion TEXT,
            second_emotion TEXT,
            user_text TEXT NOT NULL,
            assistant_reply TEXT NOT NULL
        )
    """)
    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(interaction_logs)").fetchall()
    }
    if "second_emotion" not in columns:
        conn.execute("ALTER TABLE interaction_logs ADD COLUMN second_emotion TEXT")
    conn.commit()
    conn.close()


# ---------------- USER ----------------

class User(UserMixin):

    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone


@login_manager.user_loader
def load_user(user_id):

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if user:
        return User(
            user["id"],
            user["name"],
            user["email"],
            user["phone"]
        )

    return None


# ---------------- HOME / CAREMATE DASHBOARD ----------------


@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    try:
        item = conn.execute("""
            SELECT id, created_at, emotion, second_emotion, user_text, assistant_reply
            FROM interaction_logs
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()
    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        name="CareMate",
        interaction=dict(item) if item else None,
        is_demo=False
    )


@app.route("/demo")
def demo():
    interaction = {
        "id": 1,
        "created_at": "Sample interaction · Demo data",
        "emotion": "Calm",
        "second_emotion": "Happy",
        "user_text": "Could you remind me about my afternoon appointment?",
        "assistant_reply": "Of course. I can remind you about your appointment this afternoon."
    }
    return render_template(
        "dashboard.html",
        name="CareMate",
        interaction=interaction,
        is_demo=True
    )



@app.route("/api/latest-interaction", methods=["GET"])
def latest_interaction():
    conn = get_db()
    try:
        item = conn.execute("""
            SELECT id, created_at, emotion, second_emotion, user_text, assistant_reply
            FROM interaction_logs
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()
    finally:
        conn.close()

    return jsonify({
        "interaction": dict(item) if item else None
    })





# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if os.environ.get("CAREMATE_ALLOW_SIGNUP") != "1":
        return "Signup is disabled.", 403

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash("Passwords do not match.")
            return redirect(url_for("signup"))

        conn = get_db()

        existing_user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_user:

            conn.close()

            flash("Email already registered.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        conn.execute("""
            INSERT INTO users (name, email, phone, password)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            hashed_password
        ))

        conn.commit()
        conn.close()

        flash("Account created successfully!")

        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            user_obj = User(
                user["id"],
                user["name"],
                user["email"],
                user["phone"]
            )

            login_user(user_obj)

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------



@app.post("/api/log-interaction")
def log_interaction():
    expected_token = os.environ.get("CAREMATE_DASHBOARD_TOKEN")

    if not expected_token:
        return jsonify({"error": "Dashboard token is not configured"}), 503

    supplied_token = request.headers.get("X-CareMate-Token", "")

    if not hmac.compare_digest(supplied_token, expected_token):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}

    user_text = data.get("user_text")
    assistant_reply = data.get("assistant_reply")
    emotion = data.get("emotion")
    second_emotion = data.get("second_emotion")

    if not isinstance(user_text, str) or not user_text.strip():
        return jsonify({"error": "Missing user text"}), 400

    if not isinstance(assistant_reply, str) or not assistant_reply.strip():
        return jsonify({"error": "Missing assistant reply"}), 400

    if emotion is not None and not isinstance(emotion, str):
        return jsonify({"error": "Invalid emotion"}), 400

    if second_emotion is not None and not isinstance(second_emotion, str):
        return jsonify({"error": "Invalid second emotion"}), 400

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO interaction_logs
                (emotion, second_emotion, user_text, assistant_reply)
            VALUES (?, ?, ?, ?)
        """, (
            (emotion or "Not detected")[:100],
            (second_emotion or "").strip()[:100] or None,
            user_text.strip()[:5000],
            assistant_reply.strip()[:5000]
        ))

        conn.commit()
    finally:
        conn.close()

    return jsonify({"success": True}), 201

# ---------------- SPEECH EMOTION ----------------

def _speech_features(audio_path):
    with wave.open(audio_path, "rb") as audio:
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        frames = audio.readframes(audio.getnframes())

    if sample_width != 2 or not frames:
        raise ValueError("Please provide a 16-bit WAV recording.")

    samples = array("h")
    samples.frombytes(frames)
    if channels > 1:
        samples = array("h", [
            sum(samples[index:index + channels]) // channels
            for index in range(0, len(samples), channels)
        ])
    if not samples or sample_rate <= 0:
        raise ValueError("The recording does not contain usable audio.")

    peak = max(abs(sample) for sample in samples) or 1
    rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples)) / 32768
    crossings = sum(
        1 for previous, current in zip(samples, samples[1:])
        if (previous < 0 <= current) or (previous >= 0 > current)
    )
    return rms, crossings / (len(samples) / sample_rate), peak / 32768


@app.post("/analyze-speech")
@login_required
def analyze_speech():
    recording = request.files.get("audio")
    if recording is None or not recording.filename:
        return {"error": "Record some speech before analyzing it."}, 400

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temporary_file:
            temporary_path = temporary_file.name
            recording.save(temporary_path)

        rms, zero_crossing_rate, peak = _speech_features(temporary_path)
        if peak < 0.01:
            return {"error": "The recording is silent. Please speak closer to the microphone."}, 422

        if rms >= 0.18 and zero_crossing_rate >= 180:
            emotion, confidence = "excited", 0.74
        elif rms >= 0.16:
            emotion, confidence = "angry", 0.68
        elif rms < 0.045:
            emotion, confidence = "sad", 0.63
        elif zero_crossing_rate < 90:
            emotion, confidence = "calm", 0.66
        else:
            emotion, confidence = "neutral", 0.58

        return {
            "emotion": emotion,
            "confidence": confidence,
            "features": {
                "volume": round(rms, 3),
                "pitch_activity": round(zero_crossing_rate, 1),
            },
        }
    except (EOFError, OSError, ValueError, wave.Error) as error:
        return {"error": f"Could not analyze this recording: {error}"}, 422
    finally:
        if temporary_path:
            import os
            os.unlink(temporary_path)


# ---------------- LOGOUT ----------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("home"))

# ---------------- START ----------------

if __name__ == "__main__":

    create_database()

    app.run(host="0.0.0.0", port=5000, debug=False)