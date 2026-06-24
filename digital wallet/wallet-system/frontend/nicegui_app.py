    with ui.row().classes("w-full max-w-5xl mx-auto mt-10 gap-6 items-start"):
        with ui.card().classes("w-96"):
            ui.label("Login").classes("text-lg font-semibold")
            email = ui.input("Email").classes("w-full")
            password = ui.input("Password", password=True).classes("w-full")

            def login():
                try:
                    data = request_api("POST", "/login", {"email": email.value, "password": password.value})
                    app.storage.user["token"] = data["access_token"]
                    app.storage.user["user"] = data["user"]
                    ui.navigate.to("/")
                except RuntimeError as exc:
                    ui.notify(str(exc), type="negative")

            ui.button("Login", on_click=login).classes("w-full")

        with ui.card().classes("w-96"):
            ui.label("Register").classes("text-lg font-semibold")
            name = ui.input("Name").classes("w-full")
            email = ui.input("Email").classes("w-full")
            password = ui.input("Password", password=True).classes("w-full")

            def register():
                try:
                    request_api("POST", "/register", {"name": name.value, "email": email.value, "password": password.value})
                    ui.notify("Account created", type="positive")
                except RuntimeError as exc:
                    ui.notify(str(exc), type="negative")

            ui.button("Create Account", on_click=register).classes("w-full")


def dashboard():
    user = app.storage.user.get("user", {})
    with ui.column().classes("w-full max-w-6xl mx-auto mt-6 gap-4"):
        ui.label(f"Welcome, {user.get('name', 'User')}").classes("text-lg font-medium")
        with ui.tabs().classes("w-full") as tabs:
            wallet_tab = ui.tab("Wallet")
            transfer_tab = ui.tab("Transfer")
            history_tab = ui.tab("Transactions")
            analytics_tab = ui.tab("Analytics")

        with ui.tab_panels(tabs, value=wallet_tab).classes("w-full"):
            with ui.tab_panel(wallet_tab):
                wallet_panel()
            with ui.tab_panel(transfer_tab):
                transfer_panel()
            with ui.tab_panel(history_tab):
                transactions_panel()
            with ui.tab_panel(analytics_tab):
                analytics_panel()


def wallet_panel():
    wallet_box = ui.column().classes("gap-3")

    def refresh():
        wallet_box.clear()
        wallet = request_api("GET", "/wallet")
        with wallet_box:
            ui.label(f"Balance: INR {float(wallet['balance']):,.2f}").classes("text-2xl font-semibold")

    amount = ui.number("Amount", min=1, step=100).classes("w-64")

    def add_money():
        try:
            request_api("POST", "/wallet/add", {"amount": amount.value})
            refresh()
            ui.notify("Money added", type="positive")
        except RuntimeError as exc:
            ui.notify(str(exc), type="negative")

    def withdraw_money():
        try:
            request_api("POST", "/wallet/withdraw", {"amount": amount.value})
            refresh()
            ui.notify("Money withdrawn", type="positive")
        except RuntimeError as exc:
            ui.notify(str(exc), type="negative")

    with ui.row().classes("gap-2"):
        ui.button("Add", on_click=add_money)
        ui.button("Withdraw", on_click=withdraw_money).props("outline")
    refresh()


def transfer_panel():
    receiver = ui.number("Receiver User ID", min=1, step=1).classes("w-64")
    amount = ui.number("Amount", min=1, step=100).classes("w-64")

    def transfer():
        try:
            data = request_api("POST", "/transfer", {"receiver_id": int(receiver.value), "amount": amount.value})
            message = f"Transaction {data['transaction_id']} created with status {data['status']}"
            ui.notify(message, type="warning" if data["status"] == "flagged" else "positive")
        except RuntimeError as exc:
            ui.notify(str(exc), type="negative")

    ui.button("Send Money", on_click=transfer)


def transactions_panel():
    table = ui.table(
        columns=[
            {"name": "transaction_id", "label": "ID", "field": "transaction_id"},
            {"name": "sender_id", "label": "Sender", "field": "sender_id"},
            {"name": "receiver_id", "label": "Receiver", "field": "receiver_id"},
            {"name": "amount", "label": "Amount", "field": "amount"},
            {"name": "status", "label": "Status", "field": "status"},
            {"name": "timestamp", "label": "Time", "field": "timestamp"},
        ],
        rows=[],
    ).classes("w-full")

    def refresh():
        table.rows = request_api("GET", "/transactions")
        table.update()

    ui.button("Refresh", on_click=refresh).props("outline")
    refresh()


def analytics_panel():
    try:
        summary = request_api("GET", "/analytics/summary")
    except RuntimeError as exc:
        ui.notify(str(exc), type="negative")
        return

    with ui.row().classes("gap-4"):
        for label, key in [
            ("Users", "total_users"),
            ("Transactions", "total_transactions"),
            ("Money Moved", "total_money_transferred"),
            ("Fraud Alerts", "fraud_alerts"),
            ("Active Users", "active_users"),
        ]:
            with ui.card().classes("w-44"):
                ui.label(label).classes("text-slate-500")
                ui.label(str(summary[key])).classes("text-xl font-semibold")


ui.run(title="Digital Wallet", storage_secret=os.getenv("NICEGUI_STORAGE_SECRET", "change-me"))
