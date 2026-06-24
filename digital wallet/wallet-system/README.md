# Digital Wallet System

FastAPI, PostgreSQL, JWT authentication, Streamlit, NiceGUI, and a simple fraud detection engine.

## Project Structure

```text
wallet-system/
├── frontend/
│   ├── streamlit_app.py
│   └── nicegui_app.py
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── auth/
├── database/
│   └── schema.sql
├── fraud_engine/
│   └── rules.py
├── analytics/
│   ├── README.md
│   └── powerbi_queries.sql
├── .env.example
└── requirements.txt
```

## Run Locally

```powershell
cd outputs\wallet-system
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

For quick local testing, leave `DATABASE_URL` unset and the app will use SQLite. For PostgreSQL, create a database and use:

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/wallet_system"
```

Start the backend:

```powershell
uvicorn backend.main:app --reload
```

Start the Streamlit frontend:

```powershell
streamlit run frontend\streamlit_app.py
```

Optional NiceGUI frontend:

```powershell
python frontend\nicegui_app.py
```

## API Endpoints

- `POST /register`
- `POST /login`
- `GET /profile`
- `PUT /profile`
- `GET /wallet`
- `POST /wallet/add`
- `POST /wallet/withdraw`
- `POST /transfer`
- `GET /transactions`
- `GET /analytics/summary`
- `GET /analytics/transactions`
- `GET /analytics/fraud-alerts`

## Fraud Rules

- Transaction amount greater than INR 50,000
- More than 10 transfers from one user in one minute
- Transfer amount greater than 5x the user's average transfer amount

Flagged transfers still complete, but their transaction status becomes `flagged` and a fraud alert is recorded.
