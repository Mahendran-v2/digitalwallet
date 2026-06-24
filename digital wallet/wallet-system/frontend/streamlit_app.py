
def wallet_view() -> None:
    ok, wallet = api_request("GET", "/wallet")
    if not ok:
        st.error(wallet)
        return

    balance = Decimal(str(wallet["balance"]))
    st.metric("Wallet Balance", f"INR {balance:,.2f}")

    add_col, withdraw_col = st.columns(2)
    with add_col:
        st.subheader("Add Money")
        with st.form("add-money"):
            amount = st.number_input("Amount", min_value=1.0, step=100.0, key="add-amount")
            submitted = st.form_submit_button("Add", use_container_width=True)
        if submitted:
            ok, data = api_request("POST", "/wallet/add", {"amount": amount})
            st.success("Money added.") if ok else st.error(data)
            if ok:
                st.rerun()

    with withdraw_col:
        st.subheader("Withdraw Money")
        with st.form("withdraw-money"):
            amount = st.number_input("Amount", min_value=1.0, step=100.0, key="withdraw-amount")
            submitted = st.form_submit_button("Withdraw", use_container_width=True)
        if submitted:
            ok, data = api_request("POST", "/wallet/withdraw", {"amount": amount})
            st.success("Money withdrawn.") if ok else st.error(data)
            if ok:
                st.rerun()


def transfer_view() -> None:
    st.subheader("Send Money")
    with st.form("transfer-money"):
        receiver_id = st.number_input("Receiver User ID", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=1.0, step=100.0)
        submitted = st.form_submit_button("Transfer", use_container_width=True)

    if submitted:
        ok, data = api_request("POST", "/transfer", {"receiver_id": int(receiver_id), "amount": amount})
        if ok and isinstance(data, dict):
            if data["status"] == "flagged":
                st.warning(f"Transfer completed and flagged for review. Transaction ID: {data['transaction_id']}")
            else:
                st.success(f"Transfer complete. Transaction ID: {data['transaction_id']}")
        else:
            st.error(data)


def transactions_view() -> None:
    ok, rows = api_request("GET", "/transactions")
    if not ok:
        st.error(rows)
        return
    if not rows:
        st.info("No transactions yet.")
        return

    df = pd.DataFrame(rows)
    st.dataframe(
        df[["transaction_id", "sender_id", "receiver_id", "amount", "status", "timestamp"]],
        use_container_width=True,
        hide_index=True,
    )


def analytics_view() -> None:
    ok, summary = api_request("GET", "/analytics/summary")
    if not ok:
        st.error(summary)
        return

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Users", summary["total_users"])
    col2.metric("Transactions", summary["total_transactions"])
    col3.metric("Money Moved", f"INR {Decimal(str(summary['total_money_transferred'])):,.2f}")
    col4.metric("Fraud Alerts", summary["fraud_alerts"])
    col5.metric("Active Users", summary["active_users"])

    ok, transactions = api_request("GET", "/analytics/transactions")
    if ok and transactions:
        df = pd.DataFrame(transactions)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["amount"] = pd.to_numeric(df["amount"])

        trend = df.groupby(df["timestamp"].dt.date, as_index=False)["amount"].sum()
        trend.columns = ["date", "amount"]
        st.plotly_chart(px.line(trend, x="date", y="amount", markers=True, title="Transaction Trend"), use_container_width=True)

        top_senders = df.groupby("sender_id", as_index=False)["amount"].sum().sort_values("amount", ascending=False).head(10)
        st.plotly_chart(px.bar(top_senders, x="sender_id", y="amount", title="Top Users by Transfer Value"), use_container_width=True)

    ok, alerts = api_request("GET", "/analytics/fraud-alerts")
    if ok and alerts:
        alerts_df = pd.DataFrame(alerts)
        st.plotly_chart(px.histogram(alerts_df, x="risk_score", nbins=10, title="Risk Score Distribution"), use_container_width=True)
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)


def profile_view() -> None:
    ok, profile = api_request("GET", "/profile")
    if not ok:
        st.error(profile)
        return

    st.subheader("Profile")
    with st.form("profile-form"):
        name = st.text_input("Name", value=profile["name"])
        email = st.text_input("Email", value=profile["email"])
        password = st.text_input("New Password", type="password", placeholder="Leave blank to keep current password")
        submitted = st.form_submit_button("Update Profile", use_container_width=True)

    if submitted:
        payload = {"name": name, "email": email}
        if password:
            payload["password"] = password
        ok, data = api_request("PUT", "/profile", payload)
        if ok and isinstance(data, dict):
            st.session_state.user = data
            st.success("Profile updated.")
        else:
            st.error(data)


def main() -> None:
    init_state()
    st.title("Digital Wallet")

    if not st.session_state.token:
        login_view()
        return

    user = st.session_state.user or {}
    with st.sidebar:
        st.caption(f"Signed in as {user.get('name', 'User')} | ID {user.get('id', '-')}")
        page = st.radio("Navigation", ["Wallet", "Transfer", "Transactions", "Analytics", "Profile"])
        if st.button("Logout", use_container_width=True):
            st.session_state.token = ""
            st.session_state.user = None
            st.rerun()

    if page == "Wallet":
        wallet_view()
    elif page == "Transfer":
        transfer_view()
    elif page == "Transactions":
        transactions_view()
    elif page == "Analytics":
        analytics_view()
    else:
        profile_view()


if __name__ == "__main__":
    main()
