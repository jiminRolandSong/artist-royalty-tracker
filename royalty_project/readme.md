# 🎵 Artist Royalty Tracker

A full-stack backend system for managing music royalty payouts to artists, built with Django and PostgreSQL. This project simulates a real-world payout workflow — from tracking streaming data to generating and disbursing payments.

---

## Features

- Artist, Track, and RoyaltyRecord modeling
- Automated royalty payment generation (`generate_payments`)
- Secure artist dashboard with per-user access control
- REST API endpoints for payments and summaries
- Unit-tested business logic and endpoints
- Simple, styled homepage with login/logout

---

## Tech Stack

- **Backend**: Django 5, Python 3.12
- **Database**: PostgreSQL
- **Auth**: Django built-in login/logout system
- **Testing**: `TestCase`, `call_command`, API tests
- **Frontend**: Django templates, optionally Chart.js (future)

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/jiminRolandSong
artist-royalty-tracker.git
cd artist-royalty-tracker
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` file

```env
DB_NAME=royalty_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run database setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Load mock data

```bash
python manage.py populate_mock_data
python manage.py generate_payments
```

---

## Login Access

- Visit: `http://localhost:8000/accounts/login/`
- Use credentials from your `createsuperuser` or linked artist account
- Upon login, you'll be redirected to your personalized dashboard

---

## Key Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with options & API links |
| `/accounts/login/` | Login screen |
| `/dashboard/` | Redirect to logged-in artist’s dashboard |
| `/artist/<id>/dashboard/` | Royalty summary & payment history |
| `/api/payments/pending/` | JSON: All pending payments |
| `/api/artist/<id>/summary/` | JSON: Total earnings, paid & unpaid |
| `/api/payments/<id>/mark_paid/` | PATCH to mark a payment as disbursed |

---

##  Running Tests

```bash
python manage.py test royalties
```

- Tests business logic: `generate_payments`
- Tests API behavior: `/mark_paid/`
- Covers payout flow and access logic

---