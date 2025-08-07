import flet as ft
import datetime
import json
import os
from collections import defaultdict

# Global variables
expenses = []
months = ["All", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
DATA_FILE = "expenses.json"

def save_expenses():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump([
                {
                    "title": e["title"],
                    "amount": float(e["amount"]),
                    "category": e["category"],
                    "date": e["date"].strftime('%Y-%m-%d') if isinstance(e["date"], datetime.date) else e["date"]
                } for e in expenses
            ], f)
    except Exception as e:
        print(f"Error saving expenses: {e}")

def load_expenses():
    global expenses
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                expenses.clear()
                for item in data:
                    expenses.append({
                        "title": item["title"],
                        "amount": float(item["amount"]),
                        "category": item["category"],
                        "date": datetime.datetime.strptime(item["date"], '%Y-%m-%d').date()
                    })
    except Exception as e:
        print(f"Error loading expenses: {e}")
        expenses = []

def main(page: ft.Page):
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Load expenses at startup
    load_expenses()

    title = ft.Text("💰 Expense Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)

    def handle_dropdown_change(e):
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

    # Initialize date picker with today's date
    date_picker = ft.DatePicker(
        first_date=datetime.date(2023, 1, 1),
        last_date=datetime.date.today(),
        value=datetime.date.today()  # Set default value
    )
    page.overlay.append(date_picker)

    def on_pick_date_click(e):
        date_picker.open = True
        page.update()

    def on_date_change(e):
        page.update()

    date_picker.on_change = on_date_change

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True
    )

    def update_pie_chart():
        try:
            month = dropdown.value
            category_totals = defaultdict(float)

            for exp in expenses:
                if isinstance(exp["date"], datetime.date):
                    exp_month = exp["date"].strftime('%B')
                    if month == "All" or exp_month == month:
                        category_totals[exp["category"]] += float(exp["amount"])

            colors = [ft.colors.CYAN, ft.colors.TEAL, ft.colors.AMBER, ft.colors.PURPLE, 
                     ft.colors.GREEN, ft.colors.ORANGE, ft.colors.PINK, ft.colors.INDIGO]
            
            pie_chart.sections = [
                ft.PieChartSection(
                    value=amt,
                    title=f"{cat}\n₹{amt:.2f}",
                    color=colors[i % len(colors)]
                )
                for i, (cat, amt) in enumerate(category_totals.items())
            ]
            page.update()
        except Exception as e:
            print(f"Error updating pie chart: {e}")

    def refresh_ui():
        try:
            month = dropdown.value
            filtered = []
            total = 0
            chart_data = defaultdict(float)

            for idx, exp in enumerate(expenses):
                if isinstance(exp["date"], datetime.date):
                    exp_month = exp["date"].strftime('%B')
                    if month == "All" or exp_month == month:
                        filtered.append((idx, exp))
                        total += float(exp["amount"])
                        chart_data[exp["category"]] += float(exp["amount"])

            category_bars.controls.clear()
            for cat, amount in chart_data.items():
                percent = (amount / total) if total > 0 else 0
                category_bars.controls.append(
                    ft.Column([
                        ft.Text(f"{cat} - ₹{amount:.2f} ({percent * 100:.1f}%)", 
                                color=ft.colors.WHITE),
                        ft.ProgressBar(value=percent, color=ft.colors.LIGHT_BLUE_ACCENT)
                    ])
                )

            expense_list.controls.clear()
            for idx, exp in filtered:
                card = ft.Card(
                    ft.Container(
                        ft.Row([
                            ft.Column([
                                ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text(f"₹{exp['amount']} | {exp['category']} | {exp['date'].strftime('%d %b %Y') if isinstance(exp['date'], datetime.date) else exp['date']}",
                                        color=ft.colors.GREY_400)
                            ], spacing=5),
                            ft.IconButton(
                                icon="delete", 
                                on_click=lambda e, i=idx: delete_expense(i), 
                                icon_color=ft.colors.RED_ACCENT
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15
                    ),
                    elevation=3,
                    color=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
                expense_list.controls.append(card)

            total_text.value = f"Total for {month}: ₹{total:.2f}"
            page.update()
        except Exception as e:
            print(f"Error refreshing UI: {e}")

    def delete_expense(index):
        try:
            if 0 <= index < len(expenses):
                expenses.pop(index)
                save_expenses()
                refresh_ui()
                update_pie_chart()
        except Exception as e:
            print(f"Error deleting expense: {e}")

    def add_expense(e):
        try:
            # Validate inputs
            if not title_input.value or not title_input.value.strip():
                show_snack_bar("Please enter a title")
                return
            
            if not amount_input.value:
                show_snack_bar("Please enter an amount")
                return
                
            if not category_input.value or not category_input.value.strip():
                show_snack_bar("Please enter a category")
                return

            try:
                amount = float(amount_input.value)
                if amount <= 0:
                    show_snack_bar("Amount must be greater than 0")
                    return
            except ValueError:
                show_snack_bar("Please enter a valid amount")
                return

            # Use date picker value or today's date
            expense_date = date_picker.value if date_picker.value else datetime.date.today()

            expenses.append({
                "title": title_input.value.strip(),
                "amount": amount,
                "category": category_input.value.strip(),
                "date": expense_date
            })
            
            save_expenses()
            
            # Clear inputs
            amount_input.value = ""
            title_input.value = ""
            category_input.value = ""
            
            refresh_ui()
            update_pie_chart()
            show_snack_bar("Expense added successfully!")
            
        except Exception as e:
            print(f"Error adding expense: {e}")
            show_snack_bar("Error adding expense")

    def show_snack_bar(message):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # UI Components
    add_button = ft.ElevatedButton(
        "➕ Add Expense", 
        on_click=add_expense, 
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE
        )
    )
    
    date_button = ft.ElevatedButton(
        "📅 Pick Date", 
        on_click=on_pick_date_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12)
        )
    )

    input_row = ft.ResponsiveRow([
        title_input,
        amount_input,
        category_input,
        date_button,
        add_button
    ], spacing=10, run_spacing=10)

    total_text = ft.Text("Total: ₹0.00", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)
    expense_list = ft.Column(spacing=10)
    category_bars = ft.Column(spacing=10)

    # Main layout
    page.add(
        ft.Column([
            title,
            dropdown,
            input_row,
            total_text,
            ft.Container(
                content=pie_chart, 
                width=400, 
                height=400,
                border_radius=10,
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE)
            ),
            ft.Divider(color=ft.colors.GREY_700),
            ft.Text("Category Breakdown", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN),
            category_bars,
            ft.Divider(color=ft.colors.GREY_700),
            ft.Text("Expenses", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN),
            expense_list
        ], spacing=20)
    )

    # Initial UI refresh
    refresh_ui()
    update_pie_chart()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")