import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import (
    get_inventory_data,
    get_sales_data
)


def product_intelligence_page():

    st.header("🧠 Product Intelligence")

    inventory = get_inventory_data()
    sales = get_sales_data()

    # ==========================================
    # DATA VALIDATION
    # ==========================================

    if sales.empty:

        st.info(
            "📊 Record sales first to generate product intelligence."
        )

        return

    # ==========================================
    # DATA CLEANING
    # ==========================================

    sales["quantity"] = pd.to_numeric(
        sales["quantity"],
        errors="coerce"
    ).fillna(0)

    sales["total_amount"] = pd.to_numeric(
        sales["total_amount"],
        errors="coerce"
    ).fillna(0)

    inventory["quantity"] = pd.to_numeric(
        inventory["quantity"],
        errors="coerce"
    ).fillna(0)

    inventory["price"] = pd.to_numeric(
        inventory["price"],
        errors="coerce"
    ).fillna(0)

    # ==========================================
    # PRODUCT SALES SUMMARY
    # ==========================================

    product_sales = (
        sales
        .groupby("product_name")
        .agg(
            Units_Sold=("quantity", "sum"),
            Revenue=("total_amount", "sum"),
            Transactions=("product_name", "count")
        )
        .reset_index()
    )

    # ==========================================
    # INVENTORY SUMMARY
    # ==========================================

    inventory_summary = (
        inventory
        .groupby("product_name")
        .agg(
            Current_Stock=("quantity", "sum"),
            Unit_Price=("price", "mean")
        )
        .reset_index()
    )

    # ==========================================
    # MERGE SALES + INVENTORY
    # ==========================================

    product_data = product_sales.merge(
        inventory_summary,
        on="product_name",
        how="outer"
    )

    product_data = product_data.fillna(0)

    # ==========================================
    # REVENUE CONTRIBUTION
    # ==========================================

    total_revenue = product_data["Revenue"].sum()

    if total_revenue > 0:

        product_data["Revenue_Contribution"] = (
            product_data["Revenue"]
            /
            total_revenue
            *
            100
        )

    else:

        product_data["Revenue_Contribution"] = 0

    # ==========================================
    # SALES VELOCITY
    # ==========================================

    if "date" in sales.columns:

        sales["date"] = pd.to_datetime(
            sales["date"],
            errors="coerce"
        )

        valid_dates = sales["date"].dropna()

        if not valid_dates.empty:

            days_active = max(
                1,
                (
                    valid_dates.max()
                    -
                    valid_dates.min()
                ).days + 1
            )

        else:

            days_active = 1

    else:

        days_active = 1

    product_data["Daily_Velocity"] = (
        product_data["Units_Sold"]
        /
        days_active
    )

    # ==========================================
    # STOCK COVERAGE
    # ==========================================

    product_data["Stock_Coverage_Days"] = 0.0

    for index, row in product_data.iterrows():

        velocity = row["Daily_Velocity"]

        if velocity > 0:

            product_data.loc[
                index,
                "Stock_Coverage_Days"
            ] = (
                row["Current_Stock"]
                /
                velocity
            )

        else:

            product_data.loc[
                index,
                "Stock_Coverage_Days"
            ] = 999

    # ==========================================
    # PRODUCT RANKINGS
    # ==========================================

    best_revenue = product_data.sort_values(
        "Revenue",
        ascending=False
    )

    best_units = product_data.sort_values(
        "Units_Sold",
        ascending=False
    )

    # ==========================================
    # KPI SECTION
    # ==========================================

    st.subheader("📊 Product Overview")

    top_product = best_revenue.iloc[0]

    fastest_product = best_units.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏆 Top Revenue Product",
        top_product["product_name"]
    )

    col2.metric(
        "🚀 Most Units Sold",
        fastest_product["product_name"]
    )

    col3.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col4.metric(
        "📦 Products",
        len(product_data)
    )

    st.divider()

    # ==========================================
    # TOP PRODUCTS
    # ==========================================

    st.subheader("🏆 Best-Selling Products")

    top_products = best_revenue.head(10)

    fig = px.bar(
        top_products,
        x="Revenue",
        y="product_name",
        orientation="h",
        title="Top Products by Revenue"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # REVENUE CONTRIBUTION
    # ==========================================

    st.subheader("💰 Revenue Contribution")

    contribution = product_data.sort_values(
        "Revenue_Contribution",
        ascending=False
    ).head(10)

    fig = px.pie(
        contribution,
        names="product_name",
        values="Revenue_Contribution",
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # SALES VELOCITY
    # ==========================================

    st.subheader("🚀 Sales Velocity")

    velocity_data = product_data.sort_values(
        "Daily_Velocity",
        ascending=False
    )

    fig = px.bar(
        velocity_data.head(10),
        x="Daily_Velocity",
        y="product_name",
        orientation="h",
        title="Fastest Moving Products"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # STOCK COVERAGE
    # ==========================================

    st.subheader("📦 Stock Coverage")

    coverage = product_data[
        product_data["Daily_Velocity"] > 0
    ].copy()

    if not coverage.empty:

        coverage = coverage.sort_values(
            "Stock_Coverage_Days"
        )

        st.dataframe(
            coverage[
                [
                    "product_name",
                    "Current_Stock",
                    "Units_Sold",
                    "Daily_Velocity",
                    "Stock_Coverage_Days"
                ]
            ].rename(
                columns={
                    "product_name": "Product",
                    "Current_Stock": "Current Stock",
                    "Units_Sold": "Units Sold",
                    "Daily_Velocity": "Units / Day",
                    "Stock_Coverage_Days": "Stock Coverage (Days)"
                }
            ).round(2),
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "Not enough sales history to calculate stock coverage."
        )

    st.divider()

    # ==========================================
    # PRODUCT STATUS
    # ==========================================

    st.subheader("🚦 Product Status")

    def determine_status(row):

        if row["Current_Stock"] <= 5:

            return "🔴 Critical Stock"

        if row["Current_Stock"] <= 10:

            return "🟡 Low Stock"

        if (
            row["Units_Sold"] <= 2
            and row["Current_Stock"] > 10
        ):

            return "🐌 Slow Moving"

        if row["Daily_Velocity"] > 1:

            return "🚀 Fast Moving"

        return "🟢 Stable"

    product_data["Status"] = product_data.apply(
        determine_status,
        axis=1
    )

    status_table = product_data[
        [
            "product_name",
            "Units_Sold",
            "Revenue",
            "Current_Stock",
            "Revenue_Contribution",
            "Status"
        ]
    ].sort_values(
        "Revenue",
        ascending=False
    )

    st.dataframe(
        status_table.rename(
            columns={
                "product_name": "Product",
                "Units_Sold": "Units Sold",
                "Revenue": "Revenue",
                "Current_Stock": "Current Stock",
                "Revenue_Contribution": "Revenue %",
                "Status": "Status"
            }
        ).round(2),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # ==========================================
    # AUTOMATED PRODUCT RECOMMENDATIONS
    # ==========================================

    st.subheader("💡 Product Recommendations")

    critical_products = product_data[
        product_data["Current_Stock"] <= 5
    ]

    fast_products = product_data[
        product_data["Daily_Velocity"] > 1
    ]

    slow_products = product_data[
        (product_data["Units_Sold"] <= 2)
        &
        (product_data["Current_Stock"] > 10)
    ]

    if not critical_products.empty:

        st.error(
            f"🔴 {len(critical_products)} product(s) "
            "need immediate restocking."
        )

    if not fast_products.empty:

        st.info(
            f"🚀 {len(fast_products)} product(s) "
            "are selling rapidly. Monitor their stock closely."
        )

    if not slow_products.empty:

        st.warning(
            f"🐌 {len(slow_products)} product(s) "
            "have high stock but low sales activity. "
            "Consider promotions or reviewing pricing."
        )

    if (
        critical_products.empty
        and fast_products.empty
        and slow_products.empty
    ):

        st.success(
            "🟢 Product portfolio currently looks stable."
        )