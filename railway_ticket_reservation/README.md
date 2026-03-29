# Railway Ticket Reservation Web App

A simple Python + Flask web application for railway ticket reservation.

## Features

- Search trains by source, destination, and travel date
- View available trains and fares
- Reserve seats for a selected train
- Store reservations in a SQLite database
- View all reservations

## Project Structure

- `app.py` - Flask backend application
- `templates/` - HTML pages
- `static/css/style.css` - Stylesheet
- `railway.db` - SQLite database (auto-created on first run)

## Setup and Run (Windows PowerShell)

1. Create and activate virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run application:

   ```powershell
   python app.py
   ```

4. Open browser:

   `http://127.0.0.1:5000`

## Notes

- This is a demo project intended for learning and basic reservation flow.
- For production, add login/auth, payment gateway integration, validation hardening, and seat inventory controls.
