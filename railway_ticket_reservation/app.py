from datetime import datetime
from pathlib import Path
import sqlite3
from flask import Flask, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
BASE_DIR = Path(__file__).resolve().parent
app.config["DATABASE"] = str(BASE_DIR / "railway.db")

TRAINS = [
    {
        "id": 1,
        "number": "12952",
        "name": "Mumbai Rajdhani Express",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure": "06:30",
        "arrival": "20:15",
        "fare": 1450,
    },
    {
        "id": 2,
        "number": "12015",
        "name": "Ajmer Shatabdi Express",
        "source": "Delhi",
        "destination": "Jaipur",
        "departure": "08:00",
        "arrival": "12:20",
        "fare": 650,
    },
    {
        "id": 3,
        "number": "12051",
        "name": "Jan Shatabdi Express",
        "source": "Mumbai",
        "destination": "Goa",
        "departure": "09:45",
        "arrival": "18:00",
        "fare": 920,
    },
    {
        "id": 4,
        "number": "12027",
        "name": "KSR Bengaluru Shatabdi",
        "source": "Chennai",
        "destination": "Bengaluru",
        "departure": "07:15",
        "arrival": "13:10",
        "fare": 780,
    },
    {
        "id": 5,
        "number": "12301",
        "name": "Howrah Rajdhani Express",
        "source": "Kolkata",
        "destination": "Delhi",
        "departure": "05:50",
        "arrival": "22:30",
        "fare": 1600,
    },
    {
        "id": 6,
        "number": "12724",
        "name": "Telangana Express",
        "source": "Hyderabad",
        "destination": "Pune",
        "departure": "10:10",
        "arrival": "18:40",
        "fare": 870,
    },
    {
        "id": 7,
        "number": "12627",
        "name": "Karnataka Express",
        "source": "Delhi",
        "destination": "Bengaluru",
        "departure": "20:20",
        "arrival": "06:40",
        "fare": 1950,
    },
    {
        "id": 8,
        "number": "12295",
        "name": "Sanghamitra Express",
        "source": "Bengaluru",
        "destination": "Patna",
        "departure": "09:10",
        "arrival": "07:35",
        "fare": 2100,
    },
    {
        "id": 9,
        "number": "12616",
        "name": "Grand Trunk Express",
        "source": "Chennai",
        "destination": "Delhi",
        "departure": "19:15",
        "arrival": "06:35",
        "fare": 2050,
    },
    {
        "id": 10,
        "number": "12839",
        "name": "Howrah Chennai Mail",
        "source": "Kolkata",
        "destination": "Chennai",
        "departure": "23:55",
        "arrival": "03:50",
        "fare": 1725,
    },
    {
        "id": 11,
        "number": "12423",
        "name": "Dibrugarh Rajdhani",
        "source": "Delhi",
        "destination": "Guwahati",
        "departure": "16:10",
        "arrival": "09:35",
        "fare": 2250,
    },
    {
        "id": 12,
        "number": "16346",
        "name": "Netravati Express",
        "source": "Thiruvananthapuram",
        "destination": "Mumbai",
        "departure": "09:25",
        "arrival": "13:35",
        "fare": 1880,
    },
    {
        "id": 13,
        "number": "16127",
        "name": "Muthunagar Express",
        "source": "Chennai",
        "destination": "Coimbatore",
        "departure": "14:30",
        "arrival": "21:45",
        "fare": 580,
    },
    {
        "id": 14,
        "number": "16729",
        "name": "Rockfort Express",
        "source": "Trichy",
        "destination": "Chennai",
        "departure": "08:15",
        "arrival": "11:30",
        "fare": 420,
    },
    {
        "id": 15,
        "number": "16855",
        "name": "Uzhavan Express",
        "source": "Coimbatore",
        "destination": "Madurai",
        "departure": "18:45",
        "arrival": "22:20",
        "fare": 490,
    },
    {
        "id": 16,
        "number": "12664",
        "name": "Thirukkural Express",
        "source": "Chennai",
        "destination": "Tirupati",
        "departure": "06:00",
        "arrival": "10:15",
        "fare": 350,
    },
    {
        "id": 17,
        "number": "12640",
        "name": "Tamil Nadu Express",
        "source": "Chennai",
        "destination": "Bengaluru",
        "departure": "22:45",
        "arrival": "07:00",
        "fare": 690,
    },
    {
        "id": 18,
        "number": "16722",
        "name": "Pandian Express",
        "source": "Madurai",
        "destination": "Chennai",
        "departure": "20:30",
        "arrival": "05:45",
        "fare": 510,
    },
    {
        "id": 19,
        "number": "16857",
        "name": "Cholan Express",
        "source": "Trichy",
        "destination": "Bengaluru",
        "departure": "16:20",
        "arrival": "22:15",
        "fare": 620,
    },
    {
        "id": 20,
        "number": "12664",
        "name": "Pallavan Express",
        "source": "Chennai",
        "destination": "Ambur",
        "departure": "10:30",
        "arrival": "13:50",
        "fare": 280,
    },
    {
        "id": 21,
        "number": "16856",
        "name": "Vaigai Express",
        "source": "Madurai",
        "destination": "Chennai",
        "departure": "07:25",
        "arrival": "14:40",
        "fare": 520,
    },
    {
        "id": 22,
        "number": "16853",
        "name": "Nellai Express",
        "source": "Nagercoil",
        "destination": "Bengaluru",
        "departure": "18:10",
        "arrival": "09:30",
        "fare": 780,
    },
    {
        "id": 23,
        "number": "16352",
        "name": "Ananthapuri Express",
        "source": "Thiruvananthapuram",
        "destination": "Bengaluru",
        "departure": "12:05",
        "arrival": "22:45",
        "fare": 850,
    },
    {
        "id": 24,
        "number": "16861",
        "name": "Silambu Express",
        "source": "Coimbatore",
        "destination": "Chennai",
        "departure": "15:35",
        "arrival": "22:10",
        "fare": 420,
    },
    {
        "id": 25,
        "number": "16857",
        "name": "Kaveri Express",
        "source": "Bengaluru",
        "destination": "Chennai",
        "departure": "11:40",
        "arrival": "16:55",
        "fare": 510,
    },
]

TRACKING_UPDATES = {
    "12952": {
        "status": "Running On Time",
        "current_station": "Kota Junction",
        "next_station": "Ratlam Junction",
        "delay_minutes": 0,
        "platform": "2",
    },
    "12015": {
        "status": "Running Late",
        "current_station": "Gurgaon",
        "next_station": "Rewari Junction",
        "delay_minutes": 18,
        "platform": "4",
    },
    "12051": {
        "status": "Arrived",
        "current_station": "Madgaon Junction",
        "next_station": "Trip Completed",
        "delay_minutes": 0,
        "platform": "1",
    },
    "12027": {
        "status": "Running On Time",
        "current_station": "Katpadi Junction",
        "next_station": "Bengaluru Cantonment",
        "delay_minutes": 0,
        "platform": "3",
    },
    "12301": {
        "status": "Departed",
        "current_station": "Howrah Junction",
        "next_station": "Asansol Junction",
        "delay_minutes": 6,
        "platform": "9",
    },
    "12724": {
        "status": "Scheduled",
        "current_station": "Hyderabad Deccan",
        "next_station": "Vikarabad Junction",
        "delay_minutes": 0,
        "platform": "5",
    },
    "12627": {
        "status": "Running On Time",
        "current_station": "Jhansi Junction",
        "next_station": "Bhopal Junction",
        "delay_minutes": 0,
        "platform": "6",
    },
    "12295": {
        "status": "Running Late",
        "current_station": "Vijayawada Junction",
        "next_station": "Visakhapatnam",
        "delay_minutes": 22,
        "platform": "7",
    },
    "12616": {
        "status": "Departed",
        "current_station": "Chennai Central",
        "next_station": "Nellore",
        "delay_minutes": 4,
        "platform": "4",
    },
    "12839": {
        "status": "Running On Time",
        "current_station": "Kharagpur Junction",
        "next_station": "Balasore",
        "delay_minutes": 0,
        "platform": "10",
    },
    "12423": {
        "status": "Scheduled",
        "current_station": "New Delhi",
        "next_station": "Kanpur Central",
        "delay_minutes": 0,
        "platform": "16",
    },
    "16346": {
        "status": "Running Late",
        "current_station": "Mangaluru Junction",
        "next_station": "Udupi",
        "delay_minutes": 14,
        "platform": "2",
    },
    "16127": {
        "status": "Running On Time",
        "current_station": "Chengalpattu",
        "next_station": "Ranipet",
        "delay_minutes": 0,
        "platform": "3",
    },
    "16729": {
        "status": "Running Late",
        "current_station": "Ariyalur",
        "next_station": "Villupuram",
        "delay_minutes": 12,
        "platform": "2",
    },
    "16855": {
        "status": "Scheduled",
        "current_station": "Coimbatore",
        "next_station": "Podanur",
        "delay_minutes": 0,
        "platform": "4",
    },
    "12664": {
        "status": "Running On Time",
        "current_station": "Chennai Central",
        "next_station": "Chengalpattu",
        "delay_minutes": 0,
        "platform": "7",
    },
    "12640": {
        "status": "Departed",
        "current_station": "Katpadi",
        "next_station": "Krishnarajapuram",
        "delay_minutes": 8,
        "platform": "5",
    },
    "16722": {
        "status": "Running On Time",
        "current_station": "Madurai Junction",
        "next_station": "Virudunagar",
        "delay_minutes": 0,
        "platform": "6",
    },
    "16857": {
        "status": "Running Late",
        "current_station": "Tiruchirappalli",
        "next_station": "Namakkal",
        "delay_minutes": 15,
        "platform": "8",
    },
    "16852": {
        "status": "Running On Time",
        "current_station": "Ambur",
        "next_station": "Ranipet",
        "delay_minutes": 0,
        "platform": "1",
    },
    "16856": {
        "status": "Scheduled",
        "current_station": "Madurai",
        "next_station": "Sivaganga",
        "delay_minutes": 0,
        "platform": "9",
    },
    "16853": {
        "status": "Running Late",
        "current_station": "Nagercoil",
        "next_station": "Tirunelveli",
        "delay_minutes": 20,
        "platform": "3",
    },
    "16352": {
        "status": "Running On Time",
        "current_station": "Thiruvananthapuram",
        "next_station": "Attingal",
        "delay_minutes": 0,
        "platform": "2",
    },
    "16861": {
        "status": "Running On Time",
        "current_station": "Salem",
        "next_station": "Krishnagiri",
        "delay_minutes": 0,
        "platform": "4",
    },
}


def get_tracking_info(train: dict):
    update = TRACKING_UPDATES.get(
        train["number"],
        {
            "status": "Status Not Available",
            "current_station": train["source"],
            "next_station": train["destination"],
            "delay_minutes": 0,
            "platform": "TBD",
        },
    )

    return {
        "train_number": train["number"],
        "train_name": train["name"],
        "route": f"{train['source']} to {train['destination']}",
        "take_in_time": train["departure"],
        "take_out_time": train["arrival"],
        "status": update["status"],
        "current_station": update["current_station"],
        "next_station": update["next_station"],
        "delay_minutes": update["delay_minutes"],
        "platform": update["platform"],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            train_number TEXT NOT NULL,
            train_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            travel_class TEXT NOT NULL,
            passenger_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            seats INTEGER NOT NULL,
            total_fare REAL NOT NULL,
            booked_at TEXT NOT NULL
        )
        """
    )

    columns = {row["name"] for row in db.execute("PRAGMA table_info(reservations)").fetchall()}
    if "train_number" not in columns:
        db.execute("ALTER TABLE reservations ADD COLUMN train_number TEXT NOT NULL DEFAULT ''")

    db.commit()


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    today = datetime.today().strftime("%Y-%m-%d")
    stations = sorted({t["source"] for t in TRAINS}.union({t["destination"] for t in TRAINS}))
    return render_template("index.html", stations=stations, today=today)


@app.post("/search")
def search_trains():
    source = request.form.get("source", "").strip()
    destination = request.form.get("destination", "").strip()
    travel_date = request.form.get("travel_date", "").strip()
    travel_class = request.form.get("travel_class", "Sleeper").strip()

    if not source or not destination or not travel_date:
        flash("Please fill all fields before searching.", "error")
        return redirect(url_for("index"))

    if source == destination:
        flash("Source and destination cannot be the same.", "error")
        return redirect(url_for("index"))

    matches = [
        t for t in TRAINS if t["source"].lower() == source.lower() and t["destination"].lower() == destination.lower()
    ]

    return render_template(
        "results.html",
        trains=matches,
        source=source,
        destination=destination,
        travel_date=travel_date,
        travel_class=travel_class,
    )


@app.route("/book/<int:train_id>", methods=["GET", "POST"])
def book_train(train_id: int):
    train = next((t for t in TRAINS if t["id"] == train_id), None)
    if train is None:
        flash("Selected train was not found.", "error")
        return redirect(url_for("index"))

    travel_date = request.args.get("travel_date", "") if request.method == "GET" else request.form.get("travel_date", "")
    travel_class = request.args.get("travel_class", "Sleeper") if request.method == "GET" else request.form.get("travel_class", "Sleeper")

    if request.method == "POST":
        passenger_name = request.form.get("passenger_name", "").strip()
        age_text = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        seats_text = request.form.get("seats", "").strip()

        if not all([passenger_name, age_text, gender, seats_text, travel_date, travel_class]):
            flash("Please complete all booking details.", "error")
            return render_template("book.html", train=train, travel_date=travel_date, travel_class=travel_class)

        try:
            age = int(age_text)
            seats = int(seats_text)
        except ValueError:
            flash("Age and seats must be numeric values.", "error")
            return render_template("book.html", train=train, travel_date=travel_date, travel_class=travel_class)

        if age < 1 or age > 120:
            flash("Please enter a valid age between 1 and 120.", "error")
            return render_template("book.html", train=train, travel_date=travel_date, travel_class=travel_class)

        if seats < 1 or seats > 6:
            flash("You can book between 1 and 6 seats in one reservation.", "error")
            return render_template("book.html", train=train, travel_date=travel_date, travel_class=travel_class)

        class_multiplier = {"Sleeper": 1.0, "AC 3 Tier": 1.4, "AC 2 Tier": 1.8, "First Class": 2.3}
        total_fare = round(train["fare"] * class_multiplier.get(travel_class, 1.0) * seats, 2)

        db = get_db()
        db.execute(
            """
            INSERT INTO reservations (
                train_id, train_number, train_name, source, destination, travel_date, travel_class,
                passenger_name, age, gender, seats, total_fare, booked_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                train["id"],
                train["number"],
                train["name"],
                train["source"],
                train["destination"],
                travel_date,
                travel_class,
                passenger_name,
                age,
                gender,
                seats,
                total_fare,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        db.commit()

        return render_template("success.html", train=train, total_fare=total_fare, seats=seats, travel_class=travel_class)

    return render_template("book.html", train=train, travel_date=travel_date, travel_class=travel_class)


@app.route("/reservations")
def reservations():
    db = get_db()
    rows = db.execute(
        """
         SELECT id, train_number, train_name, source, destination, travel_date, travel_class,
               passenger_name, age, gender, seats, total_fare, booked_at
        FROM reservations
        ORDER BY id DESC
        """
    ).fetchall()
    return render_template("reservations.html", reservations=rows)


@app.route("/tracking", methods=["GET", "POST"])
def tracking():
    selected_number = request.values.get("train_number", "").strip()
    tracking_info = None

    if selected_number:
        selected_train = next((t for t in TRAINS if t["number"] == selected_number), None)
        if selected_train is None:
            flash("Train number not found. Please select a valid train.", "error")
        else:
            tracking_info = get_tracking_info(selected_train)

    return render_template(
        "tracking.html",
        trains=TRAINS,
        selected_number=selected_number,
        tracking_info=tracking_info,
    )


@app.route("/manage")
def manage():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, train_number, train_name, source, destination, travel_date, travel_class,
               passenger_name, age, gender, seats, total_fare, booked_at
        FROM reservations
        ORDER BY id DESC
        """
    ).fetchall()
    return render_template("manage.html", reservations=rows)


@app.route("/update/<int:res_id>", methods=["GET", "POST"])
def update_reservation(res_id: int):
    db = get_db()
    reservation = db.execute(
        "SELECT * FROM reservations WHERE id = ?", (res_id,)
    ).fetchone()

    if reservation is None:
        flash("Reservation not found.", "error")
        return redirect(url_for("manage"))

    if request.method == "POST":
        passenger_name = request.form.get("passenger_name", "").strip()
        age_text = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        seats_text = request.form.get("seats", "").strip()
        travel_class = request.form.get("travel_class", "").strip()

        if not all([passenger_name, age_text, gender, seats_text, travel_class]):
            flash("Please fill all fields.", "error")
            return render_template("update.html", reservation=reservation)

        try:
            age = int(age_text)
            seats = int(seats_text)
        except ValueError:
            flash("Age and seats must be numeric.", "error")
            return render_template("update.html", reservation=reservation)

        if age < 1 or age > 120:
            flash("Age must be between 1 and 120.", "error")
            return render_template("update.html", reservation=reservation)

        if seats < 1 or seats > 6:
            flash("Seats must be between 1 and 6.", "error")
            return render_template("update.html", reservation=reservation)

        class_multiplier = {"Sleeper": 1.0, "AC 3 Tier": 1.4, "AC 2 Tier": 1.8, "First Class": 2.3}
        base_fare = next(
            (t["fare"] for t in TRAINS if t["number"] == reservation["train_number"]), 1000
        )
        total_fare = round(base_fare * class_multiplier.get(travel_class, 1.0) * seats, 2)

        db.execute(
            """
            UPDATE reservations
            SET passenger_name = ?, age = ?, gender = ?, seats = ?, travel_class = ?, total_fare = ?
            WHERE id = ?
            """,
            (passenger_name, age, gender, seats, travel_class, total_fare, res_id),
        )
        db.commit()
        flash("Reservation updated successfully.", "success")
        return redirect(url_for("manage"))

    return render_template("update.html", reservation=reservation)


@app.route("/delete/<int:res_id>", methods=["POST"])
def delete_reservation(res_id: int):
    db = get_db()
    reservation = db.execute(
        "SELECT * FROM reservations WHERE id = ?", (res_id,)
    ).fetchone()

    if reservation is None:
        flash("Reservation not found.", "error")
        return redirect(url_for("manage"))

    db.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
    db.commit()
    flash("Reservation deleted successfully.", "success")
    return redirect(url_for("manage"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
