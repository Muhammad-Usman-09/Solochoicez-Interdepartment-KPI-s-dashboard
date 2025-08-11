# Solochoicez-Interdepartment-KPI-s-dashboard
---

Interactive Python + Streamlit dashboard for SoloChoicez Pvt. Ltd. to track and visualize departmental KPIs (IT, HR, Consulting, Data) with charts, filters, export options, and support for both real and sample datasets.

Departments covered:
- **IT**
- **HR Staffing**
- **Business Consulting**
- **Data Digitization**

  The solution eliminates the need for manual Excel-based tracking and provides a **centralized, real-time, and visual reporting tool**.

----

## 🎯 Objectives
- Provide a **user-friendly dashboard** for management to monitor KPIs.
- Visualize **departmental activities and trends** in a clear and interactive way.
- Enable **quick filtering and analysis** of data.
- Support **real and sample datasets** for demonstration and scalability.

----
## 🛠️ Features
- **Real-Time Visualization** using Streamlit
- Department-Wise **KPIs & Activity Tracking**
- **Interactive Charts** (Bar, Line, Pie, etc.)
- **Search & Filter Options** for better data exploration
- **Export Options** for reports
- Modular code structure for **easy maintenance & scalability**

----

## 📂 Project Structure
solochoicez-interdepartment-kpi-dashboard/
│-- app.py # Main dashboard application
│-- requirements.txt # Python dependencies
│-- README.md # Project documentation
│-- config/
│ └── settings.py # Application settings & configuration
│-- data/
│ ├── it_dataset.csv
│ ├── hr_dataset.csv
│ ├── consulting_dataset.csv
│ └── data_dataset.csv
│-- utils/
│ ├── data_loader.py # Data loading logic
│ └── charts.py # Chart creation functions


---


---

## 📊 Tech Stack
- **Python**
- **Streamlit** – Web app framework for interactive dashboards
- **Pandas** – Data processing
- **Plotly / Matplotlib** – Data visualization
- **OpenPyXL** – Excel file handling

---

## 🚀 How to Run Locally
1. **Clone the repository** (or download ZIP)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

---
Run the app:

streamlit run app.py

which opens in your browser
---
---
