import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="☕ Coffee Sales EDA",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main { background-color: #1a0f00; }

    h1, h2, h3 { font-family: 'Playfair Display', serif; }

    .stApp { background: linear-gradient(135deg, #1a0f00 0%, #2d1a00 50%, #1a0f00 100%); }

    .metric-card {
        background: linear-gradient(135deg, #3d2000 0%, #5c3300 100%);
        border: 1px solid #8B4513;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(139,69,19,0.3);
    }
    .metric-card h3 { color: #FFD700; font-size: 2rem; margin: 0; }
    .metric-card p  { color: #D2B48C; margin: 4px 0 0 0; font-size: 0.85rem; }

    .section-header {
        background: linear-gradient(90deg, #8B4513, #D2691E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        border-bottom: 2px solid #8B4513;
        padding-bottom: 8px;
        margin-top: 20px;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d1a00 0%, #1a0f00 100%);
        border-right: 1px solid #8B4513;
    }

    .sidebar-title {
        color: #FFD700;
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        text-align: center;
        padding: 15px 0;
    }

    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #D2B48C !important;
        font-weight: 500;
    }

    .upload-area {
        background: rgba(139,69,19,0.15);
        border: 2px dashed #8B4513;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        color: #D2B48C;
    }

    div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">☕ Coffee Sales<br>EDA Dashboard</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("**📊 Navigation**")
    page = st.radio("", [
        "🏠 Overview",
        "⏰ Time Analysis",
        "☕ Product Analysis",
        "💳 Payment & Revenue",
        "📅 Calendar Trends",
        "🔗 Correlation",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**🎨 Chart Theme**")
    theme = st.selectbox("", ["Dark Espresso", "Light Latte", "Mocha Brown"],
                         label_visibility="collapsed")

    PALETTE = {
        "Dark Espresso": px.colors.sequential.Oranges[::-1],
        "Light Latte":   px.colors.sequential.YlOrBr,
        "Mocha Brown":   px.colors.sequential.Oryel,
    }[theme]

    PLOTLY_TEMPLATE = "plotly_dark" if theme == "Dark Espresso" else "plotly_white"

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("~/Downloads/datasets/3_Coffe_sales.csv")

df = load_data()

# ── Helpers ───────────────────────────────────────────────────────────────────
def section(title):
    st.markdown(f'<p class="section-header">{title}</p>', unsafe_allow_html=True)

def metric_card(col, label, value, delta=None):
    delta_html = f"<p>{delta}</p>" if delta else ""
    col.markdown(f"""
    <div class="metric-card">
        <h3>{value}</h3>
        <p>{label}</p>
        {delta_html}
    </div>""", unsafe_allow_html=True)

# ── Column detection helpers ──────────────────────────────────────────────────
def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

col_hour   = find_col(df, ["hour_of_day", "hour", "Hour"])
col_tod    = find_col(df, ["Time_of_Day", "time_of_day", "TimeOfDay"])
col_coffee = find_col(df, ["coffee_name", "Coffee_Name", "item", "product"])
col_pay    = find_col(df, ["cash_type", "payment_method", "Payment", "payment"])
col_money  = find_col(df, ["money", "amount", "price", "revenue"])
col_wday   = find_col(df, ["Weekday", "weekday", "day_of_week"])
col_month  = find_col(df, ["Month_name", "month_name", "Month", "month"])

# ── PAGES ─────────────────────────────────────────────────────────────────────

# ─── 1. Overview ──────────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>☕ Coffee Sales Dashboard</h1>", unsafe_allow_html=True)

    # KPI row
    total_orders  = len(df)
    total_revenue = df[col_money].sum() if col_money else 0
    avg_order     = df[col_money].mean() if col_money else 0
    unique_items  = df[col_coffee].nunique() if col_coffee else 0

    c1, c2, c3, c4 = st.columns(4)
    metric_card(c1, "Total Orders",       f"{total_orders:,}")
    metric_card(c2, "Total Revenue",      f"${total_revenue:,.2f}")
    metric_card(c3, "Avg Order Value",    f"${avg_order:.2f}")
    metric_card(c4, "Unique Coffee Types", str(unique_items))

    st.markdown("<br>", unsafe_allow_html=True)

    # Raw data preview
    with st.expander("📋 Preview Raw Data", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        section("📊 Dataset Shape & Types")
        info_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype":  df.dtypes.values,
            "Non-Null": df.notnull().sum().values,
            "Nulls": df.isnull().sum().values,
        })
        st.dataframe(info_df, use_container_width=True)

    with col_b:
        section("📈 Statistical Summary")
        st.dataframe(df.describe().T.style.background_gradient(cmap="YlOrBr"), use_container_width=True)

    # Missing value heatmap
    if df.isnull().sum().sum() > 0:
        section("🔍 Missing Values")
        miss = df.isnull().sum().reset_index()
        miss.columns = ["Column", "Missing"]
        miss = miss[miss["Missing"] > 0]
        fig = px.bar(miss, x="Column", y="Missing", color="Missing",
                     color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE,
                     title="Missing Values per Column")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No missing values found in the dataset!")


# ─── 2. Time Analysis ─────────────────────────────────────────────────────────
elif page == "⏰ Time Analysis":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>⏰ Time Analysis</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    if col_hour:
        with c1:
            section("📊 Sales Distribution by Hour")
            fig = px.histogram(df, x=col_hour, nbins=24, color_discrete_sequence=[PALETTE[3]],
                               template=PLOTLY_TEMPLATE, labels={col_hour: "Hour of Day"},
                               title="Number of Orders per Hour")
            fig.update_layout(bargap=0.05)
            st.plotly_chart(fig, use_container_width=True)

    if col_tod:
        with c2:
            section("🌅 Sales by Time of Day")
            tod_counts = df[col_tod].value_counts().reset_index()
            tod_counts.columns = ["Time of Day", "Orders"]
            fig = px.bar(tod_counts, x="Time of Day", y="Orders",
                         color="Orders", color_continuous_scale="Oranges",
                         template=PLOTLY_TEMPLATE, title="Orders by Time of Day")
            st.plotly_chart(fig, use_container_width=True)

    if col_hour:
        section("🕐 Hourly Revenue Trend")
        if col_money:
            hourly = df.groupby(col_hour)[col_money].agg(["sum","mean","count"]).reset_index()
            hourly.columns = ["Hour", "Total Revenue", "Avg Revenue", "Orders"]
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=hourly["Hour"], y=hourly["Total Revenue"],
                                 name="Total Revenue", marker_color=PALETTE[2]), secondary_y=False)
            fig.add_trace(go.Scatter(x=hourly["Hour"], y=hourly["Orders"],
                                     name="Orders", mode="lines+markers",
                                     line=dict(color="#FFD700", width=2)), secondary_y=True)
            fig.update_layout(template=PLOTLY_TEMPLATE, title="Revenue & Orders by Hour")
            fig.update_yaxes(title_text="Revenue", secondary_y=False)
            fig.update_yaxes(title_text="Orders",  secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

    # Filters
    if col_tod and col_hour:
        section("🔍 Filter by Time of Day")
        selected_tod = st.multiselect("Select Time of Day",
                                      df[col_tod].unique().tolist(),
                                      default=df[col_tod].unique().tolist())
        filtered = df[df[col_tod].isin(selected_tod)]
        fig = px.histogram(filtered, x=col_hour, color=col_tod, nbins=24,
                           template=PLOTLY_TEMPLATE, barmode="overlay",
                           title="Hourly Distribution by Time of Day",
                           color_discrete_sequence=px.colors.sequential.Oranges[2:])
        st.plotly_chart(fig, use_container_width=True)


# ─── 3. Product Analysis ──────────────────────────────────────────────────────
elif page == "☕ Product Analysis":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>☕ Product Analysis</h1>", unsafe_allow_html=True)

    if not col_coffee:
        st.warning("No coffee name column found."); st.stop()

    c1, c2 = st.columns(2)

    with c1:
        section("🏆 Most Popular Coffee Types")
        top_n = st.slider("Show Top N Coffees", 3, df[col_coffee].nunique(), 10)
        coffee_counts = df[col_coffee].value_counts().head(top_n).reset_index()
        coffee_counts.columns = ["Coffee", "Orders"]
        fig = px.bar(coffee_counts, x="Orders", y="Coffee", orientation="h",
                     color="Orders", color_continuous_scale="Oranges",
                     template=PLOTLY_TEMPLATE, title=f"Top {top_n} Coffee Types")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section("🍩 Market Share by Coffee")
        pie_data = df[col_coffee].value_counts().head(top_n)
        fig = px.pie(values=pie_data.values, names=pie_data.index,
                     color_discrete_sequence=px.colors.sequential.Oranges[::-1],
                     template=PLOTLY_TEMPLATE, title="Order Share by Coffee Type",
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    if col_money:
        section("💰 Revenue & Avg Price per Coffee Type")
        rev = df.groupby(col_coffee)[col_money].agg(total="sum", avg="mean", count="count").reset_index()
        rev.columns = ["Coffee", "Total Revenue", "Avg Price", "Orders"]
        rev = rev.sort_values("Total Revenue", ascending=False).head(top_n)

        fig = make_subplots(1, 2, subplot_titles=("Total Revenue", "Avg Price"))
        fig.add_trace(go.Bar(y=rev["Coffee"], x=rev["Total Revenue"], orientation="h",
                             marker_color=PALETTE[2], name="Revenue"), 1, 1)
        fig.add_trace(go.Bar(y=rev["Coffee"], x=rev["Avg Price"], orientation="h",
                             marker_color=PALETTE[4], name="Avg Price"), 1, 2)
        fig.update_layout(template=PLOTLY_TEMPLATE, height=450, showlegend=False)
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    if col_tod and col_coffee:
        section("📅 Coffee Popularity by Time of Day")
        heat_data = df.groupby([col_tod, col_coffee]).size().reset_index(name="Orders")
        heat_pivot = heat_data.pivot(index=col_tod, columns=col_coffee, values="Orders").fillna(0)
        fig = px.imshow(heat_pivot, color_continuous_scale="Oranges",
                        template=PLOTLY_TEMPLATE, title="Orders Heatmap: Time of Day vs Coffee",
                        aspect="auto")
        st.plotly_chart(fig, use_container_width=True)


# ─── 4. Payment & Revenue ─────────────────────────────────────────────────────
elif page == "💳 Payment & Revenue":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>💳 Payment & Revenue</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    if col_pay:
        with c1:
            section("💳 Payment Method Distribution")
            pay_counts = df[col_pay].value_counts().reset_index()
            pay_counts.columns = ["Method", "Count"]
            fig = px.bar(pay_counts, x="Method", y="Count",
                         color="Count", color_continuous_scale="Oranges",
                         template=PLOTLY_TEMPLATE, title="Transactions by Payment Method")
            st.plotly_chart(fig, use_container_width=True)

    if col_money:
        with c2:
            section("💵 Transaction Amount Distribution")
            fig = px.histogram(df, x=col_money, nbins=40, marginal="box",
                               color_discrete_sequence=[PALETTE[3]],
                               template=PLOTLY_TEMPLATE,
                               title="Distribution of Transaction Amounts")
            st.plotly_chart(fig, use_container_width=True)

    if col_pay and col_money:
        section("💰 Revenue by Payment Method")
        rev_pay = df.groupby(col_pay)[col_money].agg(["sum","mean","count"]).reset_index()
        rev_pay.columns = ["Method", "Total Revenue", "Avg Value", "Transactions"]
        fig = px.bar(rev_pay, x="Method", y="Total Revenue",
                     color="Total Revenue", color_continuous_scale="Oranges",
                     text="Total Revenue", template=PLOTLY_TEMPLATE,
                     title="Total Revenue by Payment Method")
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    if col_money:
        section("📦 Transaction Amount Range Filter")
        min_v, max_v = float(df[col_money].min()), float(df[col_money].max())
        r = st.slider("Select Amount Range", min_v, max_v, (min_v, max_v))
        filt = df[(df[col_money] >= r[0]) & (df[col_money] <= r[1])]
        st.info(f"**{len(filt):,}** transactions in range **${r[0]:.2f} – ${r[1]:.2f}**")
        fig = px.histogram(filt, x=col_money, nbins=30,
                           color_discrete_sequence=[PALETTE[2]],
                           template=PLOTLY_TEMPLATE, title="Filtered Transaction Distribution")
        st.plotly_chart(fig, use_container_width=True)


# ─── 5. Calendar Trends ───────────────────────────────────────────────────────
elif page == "📅 Calendar Trends":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>📅 Calendar Trends</h1>", unsafe_allow_html=True)

    WEEKDAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    c1, c2 = st.columns(2)

    if col_wday:
        with c1:
            section("📆 Sales by Weekday")
            wday = df[col_wday].value_counts().reindex(
                [d for d in WEEKDAY_ORDER if d in df[col_wday].unique()]).reset_index()
            wday.columns = ["Day", "Orders"]
            fig = px.bar(wday, x="Day", y="Orders", color="Orders",
                         color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE,
                         title="Orders per Weekday")
            st.plotly_chart(fig, use_container_width=True)

    if col_month:
        with c2:
            section("📅 Sales by Month")
            mon = df[col_month].value_counts().reset_index()
            mon.columns = ["Month", "Orders"]
            fig = px.bar(mon, x="Month", y="Orders", color="Orders",
                         color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE,
                         title="Orders per Month")
            st.plotly_chart(fig, use_container_width=True)

    if col_wday and col_money:
        section("💰 Revenue by Weekday")
        rev_wday = df.groupby(col_wday)[col_money].sum().reindex(
            [d for d in WEEKDAY_ORDER if d in df[col_wday].unique()]).reset_index()
        rev_wday.columns = ["Day", "Revenue"]
        fig = px.line(rev_wday, x="Day", y="Revenue", markers=True,
                      color_discrete_sequence=[PALETTE[3]],
                      template=PLOTLY_TEMPLATE, title="Revenue Trend by Weekday")
        fig.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(fig, use_container_width=True)

    if col_wday and col_coffee:
        section("☕ Coffee Popularity by Weekday")
        heatmap = df.groupby([col_wday, col_coffee]).size().reset_index(name="Orders")
        pivot = heatmap.pivot(index=col_wday, columns=col_coffee, values="Orders").fillna(0)
        pivot = pivot.reindex([d for d in WEEKDAY_ORDER if d in pivot.index])
        fig = px.imshow(pivot, color_continuous_scale="Oranges", aspect="auto",
                        template=PLOTLY_TEMPLATE,
                        title="Coffee Orders Heatmap: Weekday × Coffee Type")
        st.plotly_chart(fig, use_container_width=True)


# ─── 6. Correlation ───────────────────────────────────────────────────────────
elif page == "🔗 Correlation":
    st.markdown("<h1 style='color:#FFD700; font-family:Playfair Display,serif;'>🔗 Correlation Analysis</h1>", unsafe_allow_html=True)

    num_df = df.select_dtypes(include=np.number)

    if num_df.shape[1] < 2:
        st.warning("Not enough numeric columns for correlation."); st.stop()

    section("🌡️ Correlation Heatmap")
    corr = num_df.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdYlGn",
                    template=PLOTLY_TEMPLATE, title="Correlation Matrix",
                    aspect="auto", zmin=-1, zmax=1)
    st.plotly_chart(fig, use_container_width=True)

    section("🔍 Scatter Explorer")
    num_cols = num_df.columns.tolist()
    if len(num_cols) >= 2:
        cc1, cc2, cc3 = st.columns(3)
        x_col = cc1.selectbox("X Axis",  num_cols, index=0)
        y_col = cc2.selectbox("Y Axis",  num_cols, index=min(1, len(num_cols)-1))
        c_col = cc3.selectbox("Color by (optional)", ["None"] + df.columns.tolist())

        scatter_kwargs = dict(x=x_col, y=y_col, template=PLOTLY_TEMPLATE,
                              title=f"{x_col} vs {y_col}", opacity=0.6,
                              color_discrete_sequence=[PALETTE[3]])
        if c_col != "None":
            scatter_kwargs["color"] = c_col
            scatter_kwargs.pop("color_discrete_sequence", None)

        fig = px.scatter(df, **scatter_kwargs, trendline="ols")
        st.plotly_chart(fig, use_container_width=True)

    section("📊 Numeric Distributions")
    selected_cols = st.multiselect("Select columns to visualize", num_cols, default=num_cols[:3])
    if selected_cols:
        fig = make_subplots(1, len(selected_cols),
                            subplot_titles=selected_cols)
        for i, col in enumerate(selected_cols, 1):
            fig.add_trace(go.Histogram(x=df[col], name=col,
                                       marker_color=PALETTE[i % len(PALETTE)],
                                       showlegend=False), 1, i)
        fig.update_layout(template=PLOTLY_TEMPLATE, height=350)
        st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8B4513; font-size:0.8rem;'>"
    "☕ Coffee Sales EDA Dashboard &nbsp;|&nbsp; Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True,
)
