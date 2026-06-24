Digital Wallet System
FastAPI, PostgreSQL, JWT authentication, Streamlit, NiceGUI, and a simple fraud detection engine.

Project Structure
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

python frontend\nicegui_app.py
API Endpoints
POST /register
POST /login
GET /profile
PUT /profile
GET /wallet
POST /wallet/add
POST /wallet/withdraw
POST /transfer
GET /transactions
GET /analytics/summary
GET /analytics/transactions
GET /analytics/fraud-alerts
Fraud Rules
Transaction amount greater than INR 50,000
More than 10 transfers from one user in one minute
Transfer amount greater than 5x the user's average transfer amount
Flagged transfers still complete, but their transaction status becomes flagged and a fraud alert is recorded.
