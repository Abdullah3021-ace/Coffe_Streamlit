# ☕ Coffee Sales EDA Dashboard

An interactive Streamlit dashboard for exploratory data analysis of coffee sales data.

## 📊 Features

| Page | What you get |
|---|---|
| 🏠 Overview | KPI cards, data types, statistical summary, missing values |
| ⏰ Time Analysis | Hourly distributions, time-of-day breakdown, filters |
| ☕ Product Analysis | Top coffees, market share pie, revenue per product, heatmap |
| 💳 Payment & Revenue | Payment methods, transaction distribution, revenue by method |
| 📅 Calendar Trends | Weekday/monthly trends, revenue lines, weekday × coffee heatmap |
| 🔗 Correlation | Correlation matrix, scatter explorer, numeric distributions |

## 🛠️ Local Setup (PyCharm)

### 1. Clone / open the project
Open this folder in **PyCharm**.

### 2. Create a virtual environment
```bash
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```
The app opens at **http://localhost:8501**.  
Upload your `3_Coffe_sales.csv` (or any compatible CSV) via the sidebar.

---

## 🐙 Push to GitHub

```bash
# Inside the project folder:
git init
git add .
git commit -m "Initial commit: Coffee Sales EDA Streamlit App"

# Create a repo on github.com, then:
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git branch -M main
git push -u origin main
```

---

## 🚀 Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **"New app"**.
3. Choose:
   - **Repository**: `<your-username>/<your-repo>`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"** → your app gets a public URL in ~1 minute.

> **Tip**: The `.streamlit/config.toml` file is already included — it sets the dark espresso theme automatically on Streamlit Cloud.

---

## 📂 Expected CSV Columns

| Column | Description |
|---|---|
| `hour_of_day` | Hour (0–23) |
| `Time_of_Day` | Morning / Afternoon / Evening / Night |
| `coffee_name` | Name of coffee item |
| `cash_type` | Payment method (Card / Cash) |
| `money` | Transaction amount |
| `Weekday` | Day name (Monday … Sunday) |
| `Month_name` | Month name (January … December) |

The app auto-detects columns, so minor name variations are handled gracefully.

---

## 🗂️ Project Structure

```
coffee_eda_app/
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── .streamlit/
    └── config.toml         ← Theme & server config
```
