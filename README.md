# 🎯 Superstore Sales Performance Analytics Dashboard

A modern, interactive analytics dashboard built using **Streamlit + Pandas + Plotly**.

---

## 📌 Project Overview

This project is an end-to-end **Sales Performance Analytics Dashboard** built using:

- **Streamlit** – for interactive UI  
- **Pandas** – for data cleaning and processing  
- **Plotly** – for high-quality interactive charts  
- **Superstore Dataset** – as the primary source of sales insights  

The dashboard provides dynamic filtering and real-time data visualizations to help analyze **sales**, **profit**, **customer behavior**, and **regional performance**.

---

## 🚀 Features

### ✓ 1. Interactive Filters
- Category  
- Sub-Category  
- Region  
- Segment  
- Date Range  
- Real-time updates across all charts  

---

### ✓ 2. KPI Cards
- **Total Sales**  
- **Total Profit**  
- **Total Quantity Sold**  
- **Average Discount**  

---

### ✓ 3. Interactive Visualizations (Plotly)
- Sales vs Profit (Scatter Chart)  
- Sales Trend Over Time (Line Chart)  
- Top Performing Products (Bar Chart)  
- Regional Performance (Map / Bar Chart)  
- Category-wise Sales (Pie / Donut Chart)  

All charts are interactive and hover-enabled.

---

### ✓ 4. Data Cleaning & Pre-Processing
The app automatically:

- Handles missing values  
- Converts numeric columns (**Sales, Profit, Discount, Quantity**)  
- Parses date columns  
- Removes duplicates  
- Ensures dataset consistency before visualization  

---

### ✓ 5. Export Functionality
Users can export:

- Cleaned dataset  
- Filtered dataset  
- Dashboard results as CSV  

---

### ✓ 6. Deployable on Streamlit Cloud
Fully compatible with **Streamlit Community Cloud** — push to GitHub → Deploy.

---

## 📂 Project Structure

```
📁 Global Sales Performance Analytics Dashboard
│
└── 📁 data/
    │── Superstore.csv
│
│── app.py
│── requirements.txt
│── README.md
```

---

## 🛠️ Tech Stack

| Tool          | Purpose              |
|---------------|----------------------|
| **Python**    | Core programming     |
| **Streamlit** | UI & Web App         |
| **Pandas**    | Data cleaning        |
| **Plotly**    | Interactive charts   |

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2️⃣ (Optional) Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App
```bash
streamlit run app.py
```

The app will run at:

```
http://localhost:8501
```

---

## 🌐 Deploying on Streamlit Cloud (Free)

1. Push your project to GitHub  
2. Go to **https://share.streamlit.io**  
3. Click **New App**  
4. Choose your repo → branch → file (`app.py`)  
5. Click **Deploy**  

Your app will get a **public online URL** 🚀

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, open an issue to discuss what you'd like to modify.

---

## 📧 Contact

**Project:** Superstore Sales Performance Dashboard  
**Platform:** GitHub / Streamlit  

---

## ⭐ If you found this project helpful, please give it a star on GitHub! ⭐
