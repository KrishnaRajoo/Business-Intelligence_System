import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import (
    get_inventory_data,
    get_sales_data
)


def inventory_intelligence_page():

    st.header("📦 Inventory Intelligence")

    inventory = get_inventory_data()
    sales = get_sales_data()

    # ==========================================
    # VALIDATE DATA
    # ==========================================

    if inventory.empty:

        st.info(
            "📦 Add inventory records to generate inventory intelligence."
        )

        return

    # ==========================================
    # DATA CLEANING
    # ==========================================

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

        if "date" in sales.columns:

            sales["date"] = pd.to_datetime(
                sales["date"],
                errors="coerce"
            )

    # ==========================================
    # INVENTORY VALUE
    # ==========================================

    inventory["Inventory_Value"] = (
        inventory["quantity"]
        *
        inventory["price"]
    )

    # ==========================================
    # SALES VELOCITY
    # ==========================================

    if not sales.empty:

        if "date" in sales.columns:

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

        sales_velocity = (
            sales
            .groupby("product_name")
            .agg(
                Units_Sold=("quantity", "sum"),
                Revenue=("total_amount", "sum")
            )
            .reset_index()
        )

        sales_velocity["Daily_Velocity"] = (
            sales_velocity["Units_Sold"]
            /
            days_active
        )

    else:

        sales_velocity = pd.DataFrame(
            columns=[
                "product_name",
                "Units_Sold",
                "Revenue",
                "Daily_Velocity"
            ]
        )

    # ==========================================
    # MERGE INVENTORY + SALES
    # ==========================================

    inventory_analysis = inventory.merge(
        sales_velocity,
        on="product_name",
        how="left"
    )

    inventory_analysis[
        [
            "Units_Sold",
            "Revenue",
            "Daily_Velocity"
        ]
    ] = inventory_analysis[
        [
            "Units_Sold",
            "Revenue",
            "Daily_Velocity"
        ]
    ].fillna(0)

    # ==========================================
    # STOCK COVERAGE
    # ==========================================

    inventory_analysis["Stock_Coverage_Days"] = (
        inventory_analysis["quantity"]
        /
        inventory_analysis["Daily_Velocity"].replace(
            0,
            float("nan")
        )
    )

    # Products with no sales
    inventory_analysis["Stock_Coverage_Days"] = (
        inventory_analysis[
            "Stock_Coverage_Days"
        ].fillna(999)
    )

    # ==========================================
    # INVENTORY STATUS
    # ==========================================

    def determine_status(row):

        stock = row["quantity"]
        velocity = row["Daily_Velocity"]
        coverage = row["Stock_Coverage_Days"]

        # Critical stock
        if stock <= 5:

            if velocity > 0:

                return "🔴 Critical / High Risk"

            return "🔴 Critical Stock"

        # High demand but low coverage
        if velocity > 0 and coverage <= 7:

            return "🚨 Reorder Soon"

        # Low stock
        if stock <= 10:

            return "🟡 Low Stock"

        # Overstock
        if (
            stock > 30
            and velocity <= 0.1
        ):

            return "🔵 Overstocked"

        # Slow moving
        if (
            stock > 10
            and velocity > 0
            and velocity < 0.2
        ):

            return "🐌 Slow Moving"

        return "🟢 Healthy"

    inventory_analysis["Status"] = (
        inventory_analysis.apply(
            determine_status,
            axis=1
        )
    )

    # ==========================================
    # KPI SECTION
    # ==========================================

    st.subheader("📊 Inventory Overview")

    total_products = len(
        inventory_analysis
    )

    total_units = inventory_analysis[
        "quantity"
    ].sum()

    total_value = inventory_analysis[
        "Inventory_Value"
    ].sum()

    reorder_products = inventory_analysis[
        inventory_analysis["Status"].isin(
            [
                "🔴 Critical / High Risk",
                "🔴 Critical Stock",
                "🚨 Reorder Soon"
            ]
        )
    ]

    overstock_products = inventory_analysis[
        inventory_analysis["Status"]
        == "🔵 Overstocked"
    ]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Products",
        total_products
    )

    col2.metric(
        "Units in Stock",
        f"{int(total_units):,}"
    )

    col3.metric(
        "Inventory Value",
        f"${total_value:,.2f}"
    )

    col4.metric(
        "🚨 Reorder Required",
        len(reorder_products)
    )

    st.divider()

    # ==========================================
    # STOCK RISK
    # ==========================================

    st.subheader("🚨 Stock Risk Analysis")

    if not reorder_products.empty:

        st.error(
            f"{len(reorder_products)} product(s) "
            "require inventory attention."
        )

        risk_columns = [
            "product_name",
            "quantity",
            "Units_Sold",
            "Daily_Velocity",
            "Stock_Coverage_Days",
            "Status"
        ]

        available_columns = [
            column
            for column in risk_columns
            if column in reorder_products.columns
        ]

        st.dataframe(
            reorder_products[
                available_columns
            ].rename(
                columns={
                    "product_name": "Product",
                    "quantity": "Current Stock",
                    "Units_Sold": "Units Sold",
                    "Daily_Velocity": "Units / Day",
                    "Stock_Coverage_Days": "Coverage (Days)",
                    "Status": "Status"
                }
            ).round(2),
            width="stretch",
            hide_index=True
        )

    else:

        st.success(
            "🟢 No immediate stockout risks detected."
        )

    st.divider()

    # ==========================================
    # STOCK COVERAGE CHART
    # ==========================================

    st.subheader("📅 Estimated Stock Coverage")

    coverage_data = inventory_analysis[
        inventory_analysis["Daily_Velocity"] > 0
    ].copy()

    if not coverage_data.empty:

        coverage_data = coverage_data.sort_values(
            "Stock_Coverage_Days"
        )

        fig = px.bar(
            coverage_data,
            x="product_name",
            y="Stock_Coverage_Days",
            title="Estimated Days of Inventory Remaining"
        )

        fig.update_layout(
            xaxis_title="Product",
            yaxis_title="Days of Stock"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:

        st.info(
            "More sales history is required to calculate stock coverage."
        )

    st.divider()

    # ==========================================
    # INVENTORY VALUE
    # ==========================================

    st.subheader("💰 Inventory Value by Product")

    value_data = inventory_analysis.sort_values(
        "Inventory_Value",
        ascending=False
    )

    fig = px.bar(
        value_data.head(15),
        x="product_name",
        y="Inventory_Value",
        title="Top Inventory Value"
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Inventory Value"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # OVERSTOCK ANALYSIS
    # ==========================================

    st.subheader("🔵 Overstock Analysis")

    if not overstock_products.empty:

        st.warning(
            f"{len(overstock_products)} product(s) "
            "may have excess inventory."
        )

        columns = [
            "product_name",
            "quantity",
            "Inventory_Value",
            "Units_Sold",
            "Daily_Velocity",
            "Status"
        ]

        available_columns = [
            column
            for column in columns
            if column in overstock_products.columns
        ]

        st.dataframe(
            overstock_products[
                available_columns
            ].rename(
                columns={
                    "product_name": "Product",
                    "quantity": "Current Stock",
                    "Inventory_Value": "Inventory Value",
                    "Units_Sold": "Units Sold",
                    "Daily_Velocity": "Units / Day",
                    "Status": "Status"
                }
            ).round(2),
            width="stretch",
            hide_index=True
        )

    else:

        st.success(
            "🟢 No significant overstock detected."
        )

    st.divider()

    # ==========================================
    # INVENTORY STATUS TABLE
    # ==========================================

    st.subheader("📋 Complete Inventory Intelligence")

    display_columns = [
        "product_name",
        "quantity",
        "price",
        "Inventory_Value",
        "Units_Sold",
        "Daily_Velocity",
        "Stock_Coverage_Days",
        "Status"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in inventory_analysis.columns
    ]

    display_data = inventory_analysis[
        available_columns
    ].copy()

    display_data = display_data.rename(
        columns={
            "product_name": "Product",
            "quantity": "Current Stock",
            "price": "Unit Price",
            "Inventory_Value": "Inventory Value",
            "Units_Sold": "Units Sold",
            "Daily_Velocity": "Units / Day",
            "Stock_Coverage_Days": "Coverage (Days)",
            "Status": "Status"
        }
    )

    st.dataframe(
        display_data.round(2),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    st.subheader("💡 Inventory Recommendations")

    recommendations = []

    critical = inventory_analysis[
        inventory_analysis["Status"]
        .isin(
            [
                "🔴 Critical / High Risk",
                "🔴 Critical Stock"
            ]
        )
    ]

    reorder = inventory_analysis[
        inventory_analysis["Status"]
        == "🚨 Reorder Soon"
    ]

    slow = inventory_analysis[
        inventory_analysis["Status"]
        == "🐌 Slow Moving"
    ]

    if not critical.empty:

        recommendations.append(
            "🔴 Prioritize immediate restocking for "
            f"{len(critical)} critical product(s)."
        )

    if not reorder.empty:

        recommendations.append(
            "🚨 Review reorder quantities for "
            f"{len(reorder)} high-demand product(s)."
        )

    if not overstock_products.empty:

        recommendations.append(
            "🔵 Consider promotions, discounts, or "
            "reduced purchasing for overstocked products."
        )

    if not slow.empty:

        recommendations.append(
            "🐌 Review slow-moving products before "
            "placing additional purchase orders."
        )

    if not recommendations:

        recommendations.append(
            "🟢 Inventory levels currently appear healthy."
        )

    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )