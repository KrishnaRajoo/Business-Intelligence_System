import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import get_sales_data


def growth_page():

    st.header("📈 Sales Growth Analysis")

    sales = get_sales_data()

    if sales.empty:
        st.info("📊 Record sales to generate growth analysis.")
        return

    # ==========================================
    # DATA CLEANING
    # ==========================================

    sales["date"] = pd.to_datetime(
        sales["date"],
        errors="coerce"
    )

    sales["quantity"] = pd.to_numeric(
        sales["quantity"],
        errors="coerce"
    ).fillna(0)

    sales["total_amount"] = pd.to_numeric(
        sales["total_amount"],
        errors="coerce"
    ).fillna(0)

    sales = sales.dropna(subset=["date"])

    if sales.empty:
        st.info("No valid sales dates available.")
        return

    # ==========================================
    # MONTHLY DATA
    # ==========================================

    monthly = (
        sales
        .assign(
            Month=sales["date"].dt.to_period("M").astype(str)
        )
        .groupby("Month")
        .agg(
            Revenue=("total_amount", "sum"),
            Units_Sold=("quantity", "sum"),
            Transactions=("product_name", "count")
        )
        .reset_index()
    )

    if monthly.empty:
        st.info("Not enough data for growth analysis.")
        return

    # ==========================================
    # CURRENT / PREVIOUS PERIOD
    # ==========================================

    current = monthly.iloc[-1]

    if len(monthly) >= 2:

        previous = monthly.iloc[-2]

        revenue_growth = (
            (
                current["Revenue"]
                -
                previous["Revenue"]
            )
            /
            previous["Revenue"]
            * 100
            if previous["Revenue"] != 0
            else 0
        )

        units_growth = (
            (
                current["Units_Sold"]
                -
                previous["Units_Sold"]
            )
            /
            previous["Units_Sold"]
            * 100
            if previous["Units_Sold"] != 0
            else 0
        )

        transaction_growth = (
            (
                current["Transactions"]
                -
                previous["Transactions"]
            )
            /
            previous["Transactions"]
            * 100
            if previous["Transactions"] != 0
            else 0
        )

    else:

        previous = None
        revenue_growth = 0
        units_growth = 0
        transaction_growth = 0

    # ==========================================
    # KPI CARDS
    # ==========================================

    st.subheader("📊 Period Comparison")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Revenue Growth",
        f"{revenue_growth:+.1f}%",
        delta=f"{revenue_growth:+.1f}%"
    )

    col2.metric(
        "📦 Unit Growth",
        f"{units_growth:+.1f}%",
        delta=f"{units_growth:+.1f}%"
    )

    col3.metric(
        "🧾 Transaction Growth",
        f"{transaction_growth:+.1f}%",
        delta=f"{transaction_growth:+.1f}%"
    )

    st.caption(
        f"Comparison: {current['Month']} "
        + (
            f"vs {previous['Month']}"
            if previous is not None
            else "(first recorded period)"
        )
    )

    st.divider()

    # ==========================================
    # REVENUE TREND
    # ==========================================

    st.subheader("💰 Monthly Revenue Trend")

    fig = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # UNITS TREND
    # ==========================================

    st.subheader("📦 Monthly Units Sold")

    fig = px.bar(
        monthly,
        x="Month",
        y="Units_Sold",
        title="Units Sold by Month"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Units Sold"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # TRANSACTION TREND
    # ==========================================

    st.subheader("🧾 Monthly Transactions")

    fig = px.bar(
        monthly,
        x="Month",
        y="Transactions",
        title="Transactions by Month"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Transactions"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # BEST SALES DAY
    # ==========================================

    daily = (
        sales
        .groupby(
            sales["date"].dt.date
        )
        .agg(
            Revenue=("total_amount", "sum"),
            Units_Sold=("quantity", "sum"),
            Transactions=("product_name", "count")
        )
        .reset_index()
    )

    if not daily.empty:

        best_day = daily.loc[
            daily["Revenue"].idxmax()
        ]

        st.subheader("🏆 Best Sales Day")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Date",
            str(best_day["date"])
        )

        col2.metric(
            "Revenue",
            f"${best_day['Revenue']:,.2f}"
        )

        col3.metric(
            "Transactions",
            int(best_day["Transactions"])
        )

    st.divider()

    # ==========================================
    # GROWTH INTERPRETATION
    # ==========================================

    st.subheader("💡 Growth Interpretation")

    if previous is None:

        st.info(
            "Record sales across at least two different "
            "months to generate meaningful growth comparisons."
        )

    elif revenue_growth > 10:

        st.success(
            f"🚀 Revenue is growing strongly. "
            f"The latest period increased by "
            f"{revenue_growth:.1f}%."
        )

    elif revenue_growth > 0:

        st.success(
            f"📈 Revenue is growing moderately by "
            f"{revenue_growth:.1f}% compared with the previous period."
        )

    elif revenue_growth == 0:

        st.info(
            "➡️ Revenue is unchanged compared with "
            "the previous period."
        )

    else:

        st.warning(
            f"📉 Revenue declined by "
            f"{abs(revenue_growth):.1f}% compared with "
            "the previous period."
        )

    # ==========================================
    # MONTHLY TABLE
    # ==========================================

    st.subheader("📋 Monthly Performance")

    st.dataframe(
        monthly,
        width="stretch",
        hide_index=True
    )