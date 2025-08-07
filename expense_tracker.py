import flet as ft  # type: ignore
import datetime
import json
import os
from collections import defaultdict

expenses = []
months = ["All", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
DATA_FILE = "expenses.json"

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump([
            {
                "title": e["title"],
                "amount": float(e["amount"]),
                "category": e["category"],
                "date": e["date"].strftime('%Y-%m-%d')
            } for e in expenses
        ], f)

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                expenses.append({
                    "title": item["title"],
                    "amount": float(item["amount"]),
                    "category": item["category"],
                    "date": datetime.datetime.strptime(item["date"], '%Y-%m-%d').date()
                })

def main(page: ft.Page):  # Removed 'async' to make it a regular function
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

    title = ft.Text("💰 Expense Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN)

    async def handle_dropdown_change(e):
        refresh_ui()
        update_pie_chart()

    dropdown = ft.Dropdown(
        label="Filter by Month",
        options=[ft.dropdown.Option(month) for month in months],
        value="All",
        on_change=handle_dropdown_change
    )

    amount_input = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER, width=120)
    title_input = ft.TextField(label="Title", width=160)
    category_input = ft.TextField(label="Category", width=140)

    date_picker = ft.DatePicker(
        first_date=datetime.date(2023, 1, 1),
        last_date=datetime.date.today()
    )
    page.overlay.append(date_picker)

    def on_pick_date_click(e):
        date_picker.open = True  # Open the date picker
        page.update()

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True
    )

    def update_pie_chart():
        month = dropdown.value
        category_totals = defaultdict(float)

        for exp in expenses:
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                category_totals[exp["category"]] += float(exp["amount"])

        pie_chart.sections = [
            ft.PieChartSection(
                value=amt,
                title=f"{cat}\n₹{amt:.2f}",
                color=ft.Colors.CYAN if i % 2 == 0 else ft.Colors.TEAL
            )
            for i, (cat, amt) in enumerate(category_totals.items())
        ]
        pie_chart.update()

    def refresh_ui():
        month = dropdown.value
        filtered = []
        total = 0
        chart_data = defaultdict(float)

        for idx, exp in enumerate(expenses):
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                filtered.append((idx, exp))
                total += float(exp["amount"])
                chart_data[exp["category"]] += float(exp["amount"])

        category_bars.controls.clear()
        for cat, amount in chart_data.items():
            percent = (amount / total) if total else 0
            category_bars.controls.append(
                ft.Column([
                    ft.Text(f"{cat} - ₹{amount:.2f} ({percent * 100:.1f}%)"),
                    ft.ProgressBar(value=percent, color=ft.Colors.LIGHT_BLUE_ACCENT)
                ])
            )

        expense_list.controls.clear()
        for idx, exp in filtered:
            card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(f"₹{exp['amount']} | {exp['category']} | {exp['date'].strftime('%d %b %Y')}",
                                    color=ft.Colors.GREY_400)
                        ], spacing=5),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=idx: delete_expense(i), icon_color=ft.Colors.RED_ACCENT)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=15
                ),
                elevation=3,
                color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=10)
            )
            expense_list.controls.append(card)

        total_text.value = f"Total for {month}: ₹{total:.2f}"
        page.update()

    def delete_expense(index):
        if 0 <= index < len(expenses):
            expenses.pop(index)
            save_expenses()
            refresh_ui()
            update_pie_chart()

    def add_expense(e):
        if not all([amount_input.value, title_input.value, category_input.value, date_picker.value]):
            return
        try:
            amount = float(amount_input.value)
        except ValueError:
            return

        expenses.append({
            "title": title_input.value,
            "amount": amount,
            "category": category_input.value,
            "date": date_picker.value
        })
        save_expenses()
        amount_input.value = title_input.value = category_input.value = ""
        refresh_ui()
        update_pie_chart()

    add_button = ft.ElevatedButton("➕ Add", on_click=add_expense, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
    input_row = ft.ResponsiveRow([
        title_input,
        amount_input,
        category_input,
        ft.ElevatedButton("📅 Pick Date", on_click=on_pick_date_click),
        add_button
    ], spacing=10, run_spacing=10)

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER)
    expense_list = ft.Column()
    category_bars = ft.Column()

    page.add(
        ft.Column([
            title,
            dropdown,
            input_row,
            total_text,
            ft.Container(content=pie_chart, width=400, height=400),
            ft.Divider(),
            category_bars,
            ft.Divider(),
            expense_list
        ])
    )

    refresh_ui()
    update_pie_chart()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000, host="0.0.0.0")