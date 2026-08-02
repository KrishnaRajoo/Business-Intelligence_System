import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from database.database import (
    get_inventory_data,
    get_sales_data
)


def recommendations_page():

    st.header("🎯 Business Recommendations")

    inventory = get_inventory_data()
    sales = get_sales_data()

    # ==========================================
    # VALIDATE DATA
    # ==========================================

    if inventory.empty and sales.empty:

        st.info(
            "📊 Add inventory and sales records to generate "
            "business recommendations."
        )

        return

    # ==========================================
    # DATA CLEANING
    # ==========================================

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

    # ==========================================
    # BASIC METRICS
    # ==========================================

    total_revenue = (
        sales["total_amount"].sum()
        if not sales.empty
        else 0
    )

    total_units_sold = (
        sales["quantity"].sum()
        if not sales.empty
        else 0
    )

    total_transactions = (
        len(sales)
        if not sales.empty
        else 0
    )

    total_inventory_units = (
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

    # ==========================================
    # INVENTORY RISK
    # ==========================================

    critical_stock = pd.DataFrame()
    low_stock = pd.DataFrame()

    if not inventory.empty:

        critical_stock = inventory[
            inventory["quantity"] <= 5
        ]

        low_stock = inventory[
            (inventory["quantity"] > 5)
            &
            (inventory["quantity"] <= 10)
        ]

    # ==========================================
    # PRODUCT PERFORMANCE
    # ==========================================

    product_sales = pd.DataFrame()

    if not sales.empty:

        product_sales = (
            sales
            .groupby("product_name")
            .agg(
                Units_Sold=("quantity", "sum"),
                Revenue=("total_amount", "sum")
            )
            .reset_index()
        )

    # ==========================================
    # BUSINESS HEALTH SCORE
    # ==========================================

    score = 100

    positive_signals = []
    negative_signals = []

    # ------------------------------------------
    # INVENTORY CONDITIONS
    # ------------------------------------------

    if not inventory.empty:

        if len(critical_stock) > 0:

            penalty = min(
                25,
                len(critical_stock) * 5
            )

            score -= penalty

            negative_signals.append(
                f"{len(critical_stock)} critical "
                "stock item(s)"
            )

        elif len(low_stock) > 0:

            penalty = min(
                10,
                len(low_stock) * 2
            )

            score -= penalty

            negative_signals.append(
                f"{len(low_stock)} low-stock item(s)"
            )

        else:

            positive_signals.append(
                "Inventory levels are healthy"
            )

    # ------------------------------------------
    # SALES CONDITIONS
    # ------------------------------------------

    if total_transactions > 0:

        positive_signals.append(
            "Sales activity is being recorded"
        )

    else:

        score -= 20

        negative_signals.append(
            "No sales transactions recorded"
        )

    # ------------------------------------------
    # PRODUCT DIVERSIFICATION
    # ------------------------------------------

    if not product_sales.empty:

        total_product_revenue = (
            product_sales["Revenue"].sum()
        )

        if total_product_revenue > 0:

            top_product = (
                product_sales
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            top_share = (
                top_product["Revenue"]
                /
                total_product_revenue
                *
                100
            )

            if top_share >= 70:

                score -= 15

                negative_signals.append(
                    f"{top_product['product_name']} "
                    "generates most of the revenue"
                )

            elif top_share >= 50:

                score -= 7

                negative_signals.append(
                    "Revenue is somewhat concentrated "
                    "in one product"
                )

            else:

                positive_signals.append(
                    "Revenue is reasonably diversified"
                )

    # Keep score within range
    score = max(
        0,
        min(
            100,
            score
        )
    )

    # ==========================================
    # HEALTH STATUS
    # ==========================================

    if score >= 85:

        health_status = "Excellent"
        health_message = (
            "Business indicators are currently strong."
        )

    elif score >= 70:

        health_status = "Healthy"
        health_message = (
            "Business performance looks generally healthy "
            "with a few areas requiring attention."
        )

    elif score >= 50:

        health_status = "Needs Attention"
        health_message = (
            "Several business indicators require attention."
        )

    else:

        health_status = "At Risk"
        health_message = (
            "Multiple important business indicators "
            "require immediate attention."
        )

    # ==========================================
    # HEALTH SCORE DISPLAY
    # ==========================================

    st.subheader("❤️ Business Health Score")

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        st.metric(
            "Health Score",
            f"{score}/100"
        )

        st.metric(
            "Status",
            health_status
        )

    with col2:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={
                    "text": "Business Health"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "threshold": {
                        "line": {
                            "width": 4
                        },
                        "value": 70
                    }
                }
            )
        )

        fig.update_layout(
            height=280
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.info(
        f"📌 {health_message}"
    )

    st.divider()

    # ==========================================
    # KEY BUSINESS METRICS
    # ==========================================

    st.subheader("📊 Business Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "📦 Units Sold",
        f"{int(total_units_sold):,}"
    )

    col3.metric(
        "🧾 Transactions",
        f"{total_transactions:,}"
    )

    col4.metric(
        "📦 Inventory Value",
        f"${inventory_value:,.2f}"
    )

    st.divider()

    # ==========================================
    # PRIORITY ACTIONS
    # ==========================================

    st.subheader("🚨 Priority Actions")

    actions = []

    # Critical inventory
    if not critical_stock.empty:

        for _, row in critical_stock.iterrows():

            actions.append(
                (
                    "🔴 HIGH",
                    f"Restock {row['product_name']}",
                    f"Only {int(row['quantity'])} "
                    "unit(s) currently available."
                )
            )

    # Low inventory
    if not low_stock.empty:

        for _, row in low_stock.iterrows():

            actions.append(
                (
                    "🟡 MEDIUM",
                    f"Review stock for {row['product_name']}",
                    f"Current stock: "
                    f"{int(row['quantity'])} units."
                )
            )

    # Revenue concentration
    if not product_sales.empty:

        total_product_revenue = (
            product_sales["Revenue"].sum()
        )

        if total_product_revenue > 0:

            top_product = (
                product_sales
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            share = (
                top_product["Revenue"]
                /
                total_product_revenue
                *
                100
            )

            if share >= 50:

                actions.append(
                    (
                        "🟡 MEDIUM",
                        "Diversify product revenue",
                        f"{top_product['product_name']} "
                        f"accounts for {share:.1f}% "
                        "of recorded revenue."
                    )
                )

    # No sales
    if total_transactions == 0:

        actions.append(
            (
                "🔴 HIGH",
                "Record sales activity",
                "No sales transactions are currently "
                "available for analysis."
            )
        )

    if not actions:

        st.success(
            "🟢 No critical actions detected. "
            "The business currently looks stable."
        )

    else:

        for priority, title, description in actions:

            with st.container(border=True):

                st.write(
                    f"**{priority} — {title}**"
                )

                st.caption(
                    description
                )

    st.divider()

    # ==========================================
    # POSITIVE SIGNALS
    # ==========================================

    st.subheader("🟢 Positive Signals")

    if positive_signals:

        for signal in positive_signals:

            st.success(
                signal
            )

    else:

        st.info(
            "No strong positive signals identified yet."
        )

    # ==========================================
    # NEGATIVE SIGNALS
    # ==========================================

    st.subheader("⚠️ Areas to Monitor")

    if negative_signals:

        for signal in negative_signals:

            st.warning(
                signal
            )

    else:

        st.success(
            "No major warning signals detected."
        )

    st.divider()

    # ==========================================
    # MANAGEMENT SUMMARY
    # ==========================================

    st.subheader("🧠 Management Summary")

    if score >= 85:

        summary = (
            "The business is currently showing strong overall "
            "indicators. Continue monitoring inventory and "
            "sales performance while maintaining the products "
            "that are driving revenue."
        )

    elif score >= 70:

        summary = (
            "Overall business performance is healthy, but "
            "there are some areas that should be monitored. "
            "Pay particular attention to inventory levels "
            "and revenue concentration."
        )

    elif score >= 50:

        summary = (
            "Business performance requires attention. "
            "Inventory risks or sales concentration may "
            "affect future performance. Review the priority "
            "actions above before making new purchasing decisions."
        )

    else:

        summary = (
            "The current business indicators suggest elevated "
            "risk. Immediate attention should be given to "
            "inventory availability, sales activity, and "
            "product performance."
        )

    st.write(
        summary
    )