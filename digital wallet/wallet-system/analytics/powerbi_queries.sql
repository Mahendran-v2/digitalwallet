-- Total users
SELECT COUNT(*) AS total_users
FROM users;

-- Total transactions and money transferred
SELECT
    COUNT(*) AS total_transactions,
    COALESCE(SUM(amount), 0) AS total_money_transferred
FROM transactions;

-- Fraud alerts
SELECT COUNT(*) AS fraud_alerts
FROM fraud_alerts;

-- Transaction trend: Date vs Amount
SELECT
    DATE(timestamp) AS transaction_date,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY transaction_date;

-- Top users: User vs Total Transfer
SELECT
    u.id AS user_id,
    u.name,
    SUM(t.amount) AS total_sent
FROM users u
JOIN transactions t ON t.sender_id = u.id
GROUP BY u.id, u.name
ORDER BY total_sent DESC
LIMIT 10;

-- Risk score distribution
SELECT risk_score, COUNT(*) AS alert_count
FROM fraud_alerts
GROUP BY risk_score
ORDER BY risk_score;

-- Daily transaction count
SELECT
    DATE(timestamp) AS transaction_date,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY transaction_date;