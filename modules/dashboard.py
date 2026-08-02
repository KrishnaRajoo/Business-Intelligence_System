import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import (
    get_inventory_data,
    get_sales_data
)


def dashboard_page():

    st.title("📊 Business Intelligence Dashboard")

    st.caption(
        "Manage products, stock levels, pricing and suppliers."
    )

    # =====================================================
    # LOAD DATA
    # =====================================================

    inventory = get_inventory_data()
    sales = get_sales_data()

    # =====================================================
    # CLEAN DATA
    # =====================================================

    if not inventory.empty:

        inventory["quantity"] = pd.to_numeric(
            inventory["quantity"],
            errors="coerce"
        ).fillna(0)

        inventory["price"] = pd.to_numeric(
            inventory["price"],
            errors="coerce"
        ).fillna(0)

    if not sales.empty:

        sales["quantity"] = pd.to_numeric(
            sales["quantity"],
            errors="coerce"
        ).fillna(0)

        sales["total_amount"] = pd.to_numeric(
            sales["total_amount"],
            errors="coerce"
        ).fillna(0)

    # =====================================================
    # DASHBOARD HEADER
    # =====================================================

    st.caption(
        "Monitor your business performance, sales activity "
        "and inventory health from one place."
    )

    st.divider()

    # =====================================================
    # EMPTY STATE
    # =====================================================

    if inventory.empty and sales.empty:

        st.info(
            "📊 Your dashboard is waiting for business data. "
            "Add inventory or sales records to start seeing insights."
        )

        return

    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_products = (
        len(inventory)
        if not inventory.empty
        else 0
    )

    total_units = (
        inventory["quantity"].sum()
        if not inventory.empty
        else 0
    )

    inventory_value = (
        (
            inventory["quantity"]
            *
            inventory["price"]
        ).sum()
        if not inventory.empty
        else 0
    )

    total_revenue = (
        sales["total_amount"].sum()
        if not sales.empty
        else 0
    )

    total_transactions = (
        len(sales)
        if not sales.empty
        else 0
    )

    low_stock = (
        len(
            inventory[
                inventory["quantity"] <= 10
            ]
        )
        if not inventory.empty
        else 0
    )

    units_sold = (
        sales["quantity"].sum()
        if not sales.empty
        else 0
    )

    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("📊 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Products",
        f"{total_products:,}"
    )

    col2.metric(
        "💰 Revenue",
        f"${total_revenue:,.2f}"
    )

    col3.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )

    col4.metric(
        "⚠️ Low Stock",
        f"{low_stock:,}"
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📦 Units in Stock",
        f"{int(total_units):,}"
    )

    col2.metric(
        "🛒 Units Sold",
        f"{int(units_sold):,}"
    )

    col3.metric(
        "💵 Inventory Value",
        f"${inventory_value:,.2f}"
    )

    st.divider()

    # =====================================================
    # SALES + INVENTORY CHARTS
    # =====================================================

    left, right = st.columns(2)

    # -----------------------------------------------------
    # SALES CHART
    # -----------------------------------------------------

    with left:

        st.subheader("💰 Sales Performance")

        if not sales.empty:

            if "date" in sales.columns:

                sales["date"] = pd.to_datetime(
                    sales["date"],
                    errors="coerce"
                )

                sales_chart = (
                    sales
                    .dropna(subset=["date"])
                    .groupby("date")["total_amount"]
                    .sum()
                    .reset_index()
                )

                if not sales_chart.empty:

                    fig = px.line(
                        sales_chart,
                        x="date",
                        y="total_amount",
                        markers=True
                    )

                    fig.update_layout(
                        height=350,
                        margin=dict(
                            l=10,
                            r=10,
                            t=20,
                            b=10
                        ),
                        xaxis_title="Date",
                        yaxis_title="Revenue"
                    )

                    st.plotly_chart(
                        fig,
                        width="stretch"
                    )

                else:

                    st.info(
                        "Not enough dated sales records "
                        "to display the trend."
                    )

            else:

                st.info(
                    "Sales date information is not available."
                )

        else:

            st.info(
                "No sales data available yet."
            )

    # -----------------------------------------------------
    # INVENTORY CHART
    # -----------------------------------------------------

    with right:

        st.subheader("📦 Inventory Distribution")

        if not inventory.empty:

            inventory_chart = (
                inventory
                .sort_values(
                    "quantity",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                inventory_chart,
                x="product_name",
                y="quantity"
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),
                xaxis_title="Product",
                yaxis_title="Units"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info(
                "No inventory data available yet."
            )

    st.divider()

    # =====================================================
    # TOP PRODUCTS
    # =====================================================

    st.subheader("🏆 Top Performing Products")

    if not sales.empty:

        product_performance = (
            sales
            .groupby("product_name")
            .agg(
                Units_Sold=("quantity", "sum"),
                Revenue=("total_amount", "sum")
            )
            .reset_index()
        )

        product_performance = (
            product_performance
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(5)
        )

        cols = st.columns(
            len(product_performance)
        )

        for col, (_, row) in zip(
            cols,
            product_performance.iterrows()
        ):

            with col:

                st.metric(
                    row["product_name"],
                    f"${row['Revenue']:,.2f}"
                )

                st.caption(
                    f"{int(row['Units_Sold'])} units sold"
                )

    else:

        st.info(
            "Sales data is required to identify "
            "top-performing products."
        )

    st.divider()

    # =====================================================
    # INVENTORY ALERTS
    # =====================================================

    st.subheader("🚨 Inventory Alerts")

    if not inventory.empty:

        low_stock_products = inventory[
            inventory["quantity"] <= 10
        ].copy()

        if not low_stock_products.empty:

            for _, row in (
                low_stock_products
                .sort_values("quantity")
                .head(5)
                .iterrows()
            ):

                if row["quantity"] <= 5:

                    st.error(
                        f"🔴 **{row['product_name']}** — "
                        f"Only {int(row['quantity'])} "
                        "units remaining."
                    )

                else:

                    st.warning(
                        f"🟡 **{row['product_name']}** — "
                        f"{int(row['quantity'])} "
                        "units remaining."
                    )

        else:

            st.success(
                "🟢 Inventory levels are currently healthy."
            )

    else:

        st.info(
            "No inventory records available."
        )

    st.divider()

    # =====================================================
    # RECENT SALES
    # =====================================================

    st.subheader("🧾 Recent Transactions")

    if not sales.empty:

        recent_sales = sales.tail(8).copy()

        st.dataframe(
            recent_sales,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No transactions recorded yet."
        )

    st.divider()

    # =====================================================
    # QUICK BUSINESS SUMMARY
    # =====================================================

    st.subheader("🧠 Business Snapshot")

    if total_revenue > 0:

        average_transaction = (
            total_revenue
            /
            total_transactions
        )

    else:

        average_transaction = 0

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.write(
            f"""
            **Revenue:** ${total_revenue:,.2f}

            **Average Transaction:** ${average_transaction:,.2f}

            **Units Sold:** {int(units_sold):,}
            """
        )

    with summary_col2:

        st.write(
            f"""
            **Products:** {total_products:,}

            **Units in Stock:** {int(total_units):,}

            **Low Stock Products:** {low_stock:,}
            """
        )