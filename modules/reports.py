import streamlit as st
import pandas as pd
import io

from database.database import (
    get_inventory_data,
    get_sales_data
)


def reports_page():

    st.header("📄 Reports & Export Center")

    inventory = get_inventory_data()
    sales = get_sales_data()

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
    # REPORT TYPE
    # ==========================================

    st.subheader("📑 Select Report")

    report_type = st.selectbox(
        "Choose a report",
        [
            "Sales Report",
            "Inventory Report",
            "Product Performance Report",
            "Business Summary"
        ]
    )

    st.divider()

    # ==========================================
    # SALES REPORT
    # ==========================================

    if report_type == "Sales Report":

        st.subheader("💰 Sales Report")

        if sales.empty:

            st.info(
                "No sales records available."
            )

            return

        # Summary
        total_revenue = sales[
            "total_amount"
        ].sum()

        total_units = sales[
            "quantity"
        ].sum()

        transactions = len(sales)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Revenue",
            f"${total_revenue:,.2f}"
        )

        col2.metric(
            "Units Sold",
            int(total_units)
        )

        col3.metric(
            "Transactions",
            transactions
        )

        st.divider()

        st.dataframe(
            sales,
            width="stretch",
            hide_index=True
        )

        # CSV
        csv = sales.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Sales CSV",
            data=csv,
            file_name="sales_report.csv",
            mime="text/csv",
            width="stretch"
        )

    # ==========================================
    # INVENTORY REPORT
    # ==========================================

    elif report_type == "Inventory Report":

        st.subheader("📦 Inventory Report")

        if inventory.empty:

            st.info(
                "No inventory records available."
            )

            return

        inventory_report = inventory.copy()

        inventory_report[
            "Inventory Value"
        ] = (
            inventory_report["quantity"]
            *
            inventory_report["price"]
        )

        total_units = inventory_report[
            "quantity"
        ].sum()

        total_value = inventory_report[
            "Inventory Value"
        ].sum()

        low_stock = len(
            inventory_report[
                inventory_report["quantity"] <= 10
            ]
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Units in Stock",
            int(total_units)
        )

        col2.metric(
            "Inventory Value",
            f"${total_value:,.2f}"
        )

        col3.metric(
            "Low Stock Items",
            low_stock
        )

        st.divider()

        st.dataframe(
            inventory_report,
            width="stretch",
            hide_index=True
        )

        csv = inventory_report.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Inventory CSV",
            data=csv,
            file_name="inventory_report.csv",
            mime="text/csv",
            width="stretch"
        )

    # ==========================================
    # PRODUCT PERFORMANCE
    # ==========================================

    elif report_type == "Product Performance Report":

        st.subheader("🏆 Product Performance Report")

        if sales.empty:

            st.info(
                "Record sales to generate product performance."
            )

            return

        performance = (
            sales
            .groupby("product_name")
            .agg(
                Units_Sold=("quantity", "sum"),
                Revenue=("total_amount", "sum"),
                Transactions=("product_name", "count")
            )
            .reset_index()
        )

        performance = performance.sort_values(
            "Revenue",
            ascending=False
        )

        performance["Revenue Contribution %"] = (
            performance["Revenue"]
            /
            performance["Revenue"].sum()
            *
            100
        )

        col1, col2, col3 = st.columns(3)

        top_revenue = performance.iloc[0]

        top_units = performance.sort_values(
            "Units_Sold",
            ascending=False
        ).iloc[0]

        col1.metric(
            "Top Revenue Product",
            top_revenue["product_name"]
        )

        col2.metric(
            "Best-Selling Product",
            top_units["product_name"]
        )

        col3.metric(
            "Products Analyzed",
            len(performance)
        )

        st.divider()

        st.dataframe(
            performance.round(2),
            width="stretch",
            hide_index=True
        )

        csv = performance.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Product Report",
            data=csv,
            file_name="product_performance.csv",
            mime="text/csv",
            width="stretch"
        )

    # ==========================================
    # BUSINESS SUMMARY
    # ==========================================

    elif report_type == "Business Summary":

        st.subheader("🧠 Business Summary")

        total_revenue = (
            sales["total_amount"].sum()
            if not sales.empty
            else 0
        )

        total_units = (
            sales["quantity"].sum()
            if not sales.empty
            else 0
        )

        transactions = (
            len(sales)
            if not sales.empty
            else 0
        )

        inventory_units = (
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

        low_stock = (
            len(
                inventory[
                    inventory["quantity"] <= 10
                ]
            )
            if not inventory.empty
            else 0
        )

        # ------------------------------------------
        # SUMMARY TABLE
        # ------------------------------------------

        summary = pd.DataFrame(
            {
                "Metric": [
                    "Total Revenue",
                    "Units Sold",
                    "Transactions",
                    "Inventory Units",
                    "Inventory Value",
                    "Low Stock Products"
                ],
                "Value": [
                    f"${total_revenue:,.2f}",
                    f"{int(total_units):,}",
                    f"{transactions:,}",
                    f"{int(inventory_units):,}",
                    f"${inventory_value:,.2f}",
                    f"{low_stock:,}"
                ]
            }
        )

        st.dataframe(
            summary,
            width="stretch",
            hide_index=True
        )

        st.divider()

        # ------------------------------------------
        # MANAGEMENT SUMMARY
        # ------------------------------------------

        st.subheader("📋 Management Summary")

        summary_text = f"""
BizInsightPro Business Summary

Total Revenue: ${total_revenue:,.2f}

Units Sold: {int(total_units):,}

Total Transactions: {transactions:,}

Inventory Units: {int(inventory_units):,}

Inventory Value: ${inventory_value:,.2f}

Low Stock Products: {low_stock}

This report provides a consolidated overview of
recorded sales and inventory performance.
"""

        st.text_area(
            "Report Summary",
            summary_text,
            height=250
        )

        # ------------------------------------------
        # DOWNLOAD SUMMARY
        # ------------------------------------------

        st.download_button(
            "📥 Download Business Summary",
            data=summary_text,
            file_name="business_summary.txt",
            mime="text/plain",
            width="stretch"
        )