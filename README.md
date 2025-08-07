# 💰 Expense Tracker

A modern, user-friendly expense tracking application built with Python and Flet. Track your expenses with an intuitive dark-themed interface, visualize spending patterns with interactive charts, and filter expenses by month.

<img width="953" height="503" alt="image" src="https://github.com/user-attachments/assets/7d4efc98-8a3e-48a1-bd2c-ef207ec02798" />
<img width="954" height="504" alt="image" src="https://github.com/user-attachments/assets/24f809f1-595d-4a49-871f-94321a8f292f" />



## ✨ Features

- **💸 Easy Expense Management**: Add, view, and delete expenses with a clean interface
- **📊 Visual Analytics**: Interactive pie chart and progress bars to visualize spending by category
- **🗓️ Date Filtering**: Filter expenses by month or view all expenses
- **📱 Responsive Design**: Clean, modern dark theme that works across different screen sizes
- **💾 Persistent Storage**: Automatic saving to JSON file - your data persists between sessions
- **🌙 Dark Theme**: Easy on the eyes with a beautiful dark interface
- **📈 Category Insights**: See spending breakdown by category with percentages

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Install required dependencies**
   ```bash
   pip install flet
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

### Adding Expenses
1. Fill in the expense details:
   - **Title**: Description of the expense
   - **Amount**: Cost in your currency (₹)
   - **Category**: Type of expense (Food, Transport, etc.)
   - **Date**: Click "📅 Pick Date" to select the expense date
2. Click "➕ Add" to save the expense

### Viewing and Filtering
- Use the **month dropdown** to filter expenses by specific months or view all
- The **pie chart** shows visual breakdown of spending by category
- **Progress bars** display category-wise spending with percentages
- **Expense cards** show detailed information for each expense

### Managing Expenses
- Click the **🗑️ delete icon** on any expense card to remove it
- Total spending for the selected period is displayed prominently
- All changes are automatically saved to `expenses.json`

## 📁 Project Structure

```
expense-tracker/
│
├── main.py              # Main application file
├── expenses.json        # Data storage (auto-generated)
└── README.md           # Project documentation
```

## 🛠️ Technical Details

### Built With
- **[Flet](https://flet.dev/)**: Modern Python framework for building multi-platform applications
- **Python Standard Library**: JSON for data persistence, datetime for date handling

### Data Storage
- Expenses are stored in `expenses.json` in the following format:
```json
[
  {
    "title": "Lunch",
    "amount": 250.0,
    "category": "Food",
    "date": "2024-01-15"
  }
]
```

### Key Components
- **Responsive UI**: Adapts to different screen sizes
- **Date Picker**: Built-in calendar widget for date selection
- **Interactive Charts**: Real-time updating pie chart and progress bars
- **Auto-save**: Automatic persistence of all expense data

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contributions
- Add expense categories dropdown with predefined options
- Implement export functionality (CSV, PDF)
- Add budget setting and tracking features
- Include more chart types (bar charts, line graphs)
- Add expense search functionality
- Implement data backup and restore

## 🐛 Bug Reports

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your Python and Flet versions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flet](https://flet.dev/) - An amazing Python framework for building beautiful apps
- Icons from the Flet icon library
- Inspired by modern expense tracking applications

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

⭐ **Star this repository** if you found it helpful!
