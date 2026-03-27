# AAL Sales Dashboard — Q4 2020

Interactive sales analysis dashboard for **Australian Apparel Limited (AAL)**, built with Streamlit and Plotly.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **KPI Cards** — Total revenue, units sold, average sale, and transaction count at a glance
- **State Analysis** — Grouped bar charts, box plots, heatmaps, and ranking tables across 7 Australian states
- **Demographic Breakdown** — Sales comparison across Kids, Men, Women, and Seniors with faceted charts
- **Time-of-Day Insights** — Peak and off-peak period identification for targeted marketing strategies
- **Trend Analysis** — Daily sales with 7-day moving average, weekly and monthly bar charts
- **Interactive Filters** — Filter by state, demographic group, time of day, and month via the sidebar
- **Descriptive Statistics** — Mean, median, std, IQR, skewness, and kurtosis for Sales and Unit columns

## Quick Start

```bash
# Clone the repo
git clone https://github.com/<your-username>/aal-sales-dashboard.git
cd aal-sales-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and select `app.py` as the main file
4. Click **Deploy**

## Project Structure

```
aal-sales-dashboard/
├── app.py                  # Main Streamlit application
├── data/
│   └── AusApparalSales4thQrt2020.csv   # Q4 2020 sales data
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

## Data

The dataset contains 7,560 sales transactions from October–December 2020 across 7 Australian states (NSW, NT, QLD, SA, TAS, VIC, WA), 4 demographic groups (Kids, Men, Women, Seniors), and 3 time periods (Morning, Afternoon, Evening).

| Column | Description |
|--------|-------------|
| Date   | Transaction date (Oct–Dec 2020) |
| Time   | Time of day (Morning, Afternoon, Evening) |
| State  | Australian state |
| Group  | Demographic group |
| Unit   | Units sold |
| Sales  | Sale amount in AUD |

## License

MIT
