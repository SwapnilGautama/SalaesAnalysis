"""
AAL Sales Dashboard — Q4 2020
Australian Apparel Limited: Interactive Sales Analysis & Visualization
Built with Streamlit, Pandas, Plotly, and Seaborn
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AAL Sales Dashboard — Q4 2020",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card h3 { margin: 0; font-size: 14px; opacity: 0.85; }
    .metric-card h1 { margin: 5px 0 0 0; font-size: 28px; }
    .card-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .card-orange { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }
    .card-pink { background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); }
    .card-blue { background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%); }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Data loading & wrangling
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/AusApparalSales4thQrt2020.csv")

    # Clean whitespace
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Parse dates and add time columns
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%Y")
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%B")
    df["DayOfWeek"] = df["Date"].dt.day_name()

    # Normalize
    for col in ["Unit", "Sales"]:
        cmin, cmax = df[col].min(), df[col].max()
        df[f"{col}_norm"] = (df[col] - cmin) / (cmax - cmin)

    return df


df = load_data()

# ──────────────────────────────────────────────
# Sidebar filters
# ──────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/fluency/96/shopping-bag.png", width=64
)
st.sidebar.title("Filters")

selected_states = st.sidebar.multiselect(
    "States",
    options=sorted(df["State"].unique()),
    default=sorted(df["State"].unique()),
)
selected_groups = st.sidebar.multiselect(
    "Demographic Groups",
    options=sorted(df["Group"].unique()),
    default=sorted(df["Group"].unique()),
)
selected_times = st.sidebar.multiselect(
    "Time of Day",
    options=["Morning", "Afternoon", "Evening"],
    default=["Morning", "Afternoon", "Evening"],
)
selected_months = st.sidebar.multiselect(
    "Months",
    options=["October", "November", "December"],
    default=["October", "November", "December"],
)

# Apply filters
mask = (
    df["State"].isin(selected_states)
    & df["Group"].isin(selected_groups)
    & df["Time"].isin(selected_times)
    & df["MonthName"].isin(selected_months)
)
filtered = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**Showing {len(filtered):,} of {len(df):,} records** "
    f"({len(filtered)/len(df)*100:.1f}%)"
)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.title("🛍️ AAL Sales Dashboard — Q4 2020")
st.markdown(
    "Interactive analysis of **Australian Apparel Limited** sales data across "
    "states, demographic groups, and time periods."
)

# ──────────────────────────────────────────────
# KPI cards
# ──────────────────────────────────────────────
if len(filtered) == 0:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_units = filtered["Unit"].sum()
avg_sale = filtered["Sales"].mean()
num_transactions = len(filtered)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="metric-card"><h3>Total Revenue</h3>'
        f'<h1>${total_sales/1e6:.1f}M</h1></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="metric-card card-green"><h3>Units Sold</h3>'
        f'<h1>{total_units:,}</h1></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="metric-card card-orange"><h3>Avg Sale</h3>'
        f'<h1>${avg_sale:,.0f}</h1></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="metric-card card-pink"><h3>Transactions</h3>'
        f'<h1>{num_transactions:,}</h1></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Tab layout
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🗺️ State Analysis",
        "👥 Group Analysis",
        "⏰ Time-of-Day",
        "📈 Trends & Reports",
    ]
)

# ======== TAB 1: Overview ========
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        # Revenue by state — pie
        state_totals = (
            filtered.groupby("State")["Sales"].sum().reset_index()
        )
        fig = px.pie(
            state_totals,
            values="Sales",
            names="State",
            title="Revenue Share by State",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4,
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue by group — bar
        group_totals = (
            filtered.groupby("Group")["Sales"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        fig = px.bar(
            group_totals,
            x="Sales",
            y="Group",
            orientation="h",
            title="Total Sales by Demographic Group",
            color="Group",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(showlegend=False, xaxis_title="Total Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap: State × Group
    pivot = filtered.pivot_table(
        values="Sales", index="State", columns="Group", aggfunc="sum"
    ).fillna(0)
    fig = px.imshow(
        pivot,
        text_auto=",.0f",
        color_continuous_scale="YlOrRd",
        title="Sales Heatmap: State × Demographic Group",
        labels=dict(color="Sales ($)"),
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

# ======== TAB 2: State Analysis ========
with tab2:
    st.subheader("State-wise Sales Breakdown")

    # Grouped bar: state × group
    sg = filtered.groupby(["State", "Group"])["Sales"].sum().reset_index()
    fig = px.bar(
        sg,
        x="State",
        y="Sales",
        color="Group",
        barmode="group",
        title="Sales by State & Demographic Group",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(yaxis_title="Total Sales ($)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Box plot by state
        fig = px.box(
            filtered,
            x="State",
            y="Sales",
            color="State",
            title="Sales Distribution by State",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # State ranking table
        state_rank = (
            filtered.groupby("State")
            .agg(
                Total_Sales=("Sales", "sum"),
                Total_Units=("Unit", "sum"),
                Avg_Sale=("Sales", "mean"),
                Transactions=("Sales", "count"),
            )
            .sort_values("Total_Sales", ascending=False)
        )
        state_rank["Revenue Share %"] = (
            state_rank["Total_Sales"] / state_rank["Total_Sales"].sum() * 100
        ).round(1)
        state_rank["Total_Sales"] = state_rank["Total_Sales"].apply(
            lambda x: f"${x:,.0f}"
        )
        state_rank["Avg_Sale"] = state_rank["Avg_Sale"].apply(
            lambda x: f"${x:,.0f}"
        )
        st.markdown("**State Rankings**")
        st.dataframe(state_rank, use_container_width=True)

# ======== TAB 3: Group Analysis ========
with tab3:
    st.subheader("Demographic Group Analysis")

    col1, col2 = st.columns(2)
    with col1:
        # Group totals
        gt = (
            filtered.groupby("Group")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig = px.bar(
            gt,
            x="Group",
            y="Sales",
            color="Group",
            title="Total Sales by Group",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(showlegend=False, yaxis_title="Total Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            filtered,
            x="Group",
            y="Sales",
            color="Group",
            title="Sales Distribution by Group",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Per-group state breakdown (faceted)
    sg2 = filtered.groupby(["Group", "State"])["Sales"].sum().reset_index()
    fig = px.bar(
        sg2,
        x="State",
        y="Sales",
        color="State",
        facet_col="Group",
        facet_col_wrap=2,
        title="Each Group's Sales Across States",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(showlegend=False, height=500)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig, use_container_width=True)

# ======== TAB 4: Time-of-Day ========
with tab4:
    st.subheader("Peak & Off-Peak Analysis")

    time_order = ["Morning", "Afternoon", "Evening"]

    col1, col2 = st.columns(2)
    with col1:
        ts = (
            filtered.groupby("Time")["Sales"]
            .sum()
            .reindex(time_order)
            .reset_index()
        )
        fig = px.bar(
            ts,
            x="Time",
            y="Sales",
            color="Time",
            title="Total Sales by Time of Day",
            color_discrete_sequence=["#2196F3", "#FF9800", "#9C27B0"],
        )
        fig.update_layout(showlegend=False, yaxis_title="Total Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

        # Summary
        peak = ts.loc[ts["Sales"].idxmax(), "Time"]
        offpeak = ts.loc[ts["Sales"].idxmin(), "Time"]
        st.success(f"**Peak period:** {peak}")
        st.error(f"**Off-peak period:** {offpeak}")

    with col2:
        tg = (
            filtered.groupby(["Time", "Group"])["Sales"]
            .mean()
            .reset_index()
        )
        tg["Time"] = pd.Categorical(tg["Time"], categories=time_order, ordered=True)
        tg = tg.sort_values("Time")
        fig = px.bar(
            tg,
            x="Time",
            y="Sales",
            color="Group",
            barmode="group",
            title="Avg Sales by Time & Demographic Group",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(yaxis_title="Average Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    # Time × State heatmap
    ts_pivot = filtered.pivot_table(
        values="Sales", index="Time", columns="State", aggfunc="sum"
    )
    ts_pivot = ts_pivot.reindex(time_order)
    fig = px.imshow(
        ts_pivot,
        text_auto=",.0f",
        color_continuous_scale="Viridis",
        title="Sales Heatmap: Time of Day × State",
        labels=dict(color="Sales ($)"),
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

# ======== TAB 5: Trends & Reports ========
with tab5:
    st.subheader("Trend Analysis & Periodic Reports")

    # Daily trend
    daily = filtered.groupby("Date")["Sales"].sum().reset_index()
    daily["7-Day MA"] = daily["Sales"].rolling(7).mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["Date"],
            y=daily["Sales"],
            mode="lines",
            name="Daily Sales",
            line=dict(color="#2196F3", width=1.2),
            opacity=0.6,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily["Date"],
            y=daily["7-Day MA"],
            mode="lines",
            name="7-Day Moving Avg",
            line=dict(color="#FF5722", width=2.5),
        )
    )
    fig.update_layout(
        title="Daily Sales Trend with 7-Day Moving Average",
        yaxis_title="Sales ($)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Weekly
        weekly = (
            filtered.groupby("Week")["Sales"].sum().reset_index()
        )
        fig = px.bar(
            weekly,
            x="Week",
            y="Sales",
            title="Weekly Sales",
            color="Sales",
            color_continuous_scale="Blues",
        )
        fig.update_layout(yaxis_title="Total Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Monthly
        monthly = (
            filtered.groupby("MonthName")["Sales"]
            .sum()
            .reindex(["October", "November", "December"])
            .reset_index()
        )
        fig = px.bar(
            monthly,
            x="MonthName",
            y="Sales",
            title="Monthly Sales",
            color="MonthName",
            color_discrete_sequence=["#4ECDC4", "#45B7D1", "#FF6B6B"],
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="Month",
            yaxis_title="Total Sales ($)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Descriptive statistics table
    st.markdown("### Descriptive Statistics")
    desc = filtered[["Sales", "Unit"]].describe().T
    desc["IQR"] = desc["75%"] - desc["25%"]
    desc["skew"] = filtered[["Sales", "Unit"]].skew()
    desc["kurtosis"] = filtered[["Sales", "Unit"]].kurtosis()
    st.dataframe(desc.round(2), use_container_width=True)

    # Quarterly summary
    st.markdown("### Q4 2020 Quarterly Summary")
    q4_data = {
        "Metric": [
            "Total Revenue",
            "Total Units Sold",
            "Average Sale",
            "Average Units/Transaction",
            "Total Transactions",
            "Highest Single Sale",
            "Lowest Single Sale",
        ],
        "Value": [
            f"${filtered['Sales'].sum():,.0f}",
            f"{filtered['Unit'].sum():,}",
            f"${filtered['Sales'].mean():,.2f}",
            f"{filtered['Unit'].mean():.2f}",
            f"{len(filtered):,}",
            f"${filtered['Sales'].max():,.0f}",
            f"${filtered['Sales'].min():,.0f}",
        ],
    }
    st.table(pd.DataFrame(q4_data))

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:13px'>"
    "AAL Sales Dashboard &mdash; Built with Streamlit &amp; Plotly &mdash; "
    "Data: Q4 2020 Australian Apparel Sales"
    "</div>",
    unsafe_allow_html=True,
)
