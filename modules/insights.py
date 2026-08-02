import streamlit as st
import pandas as pd

from database.database import create_connection


def insights_page():

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("💡 Smart Business Insights")

    st.caption(
        "Automatically identify sales opportunities, inventory "
        "risks and important business trends."
    )

    st.divider()

    # =====================================================
    # DATABASE
    # =====================================================

    conn = create_connection()

    try:

        # =================================================
        # LOAD DATA
        # =================================================

        sales = pd.read_sql(
            "SELECT * FROM sales",
            conn
        )

        inventory = pd.read_sql(
            "SELECT * FROM inventory",
            conn
        )

        # =================================================
        # EMPTY DATA
        # =================================================

        if sales.empty:

            st.info(
                "💡 Smart insights will appear after you "
                "record some sales transactions."
            )

            if not inventory.empty:

                st.subheader(
                    "📦 Current Inventory Status"
                )

                inventory["quantity"] = pd.to_numeric(
                    inventory["quantity"],
                    errors="coerce"
                ).fillna(0)

                total_products = len(inventory)

                total_units = int(
                    inventory["quantity"].sum()
                )

                low_stock = len(
                    inventory[
                        inventory["quantity"] <= 10
                    ]
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Products",
                    total_products
                )

                col2.metric(
                    "Units in Stock",
                    total_units
                )

                col3.metric(
                    "Low Stock Items",
                    low_stock
                )

            return

        # =================================================
        # CLEAN DATA
        # =================================================

        sales["quantity"] = pd.to_numeric(
            sales["quantity"],
            errors="coerce"
        ).fillna(0)

        sales["total_amount"] = pd.to_numeric(
            sales["total_amount"],
            errors="coerce"
        ).fillna(0)

        if not inventory.empty:

            inventory["quantity"] = pd.to_numeric(
                inventory["quantity"],
                errors="coerce"
            ).fillna(0)

            inventory["price"] = pd.to_numeric(
                inventory["price"],
                errors="coerce"
            ).fillna(0)

        # =================================================
        # BASIC METRICS
        # =================================================

        total_revenue = sales[
            "total_amount"
        ].sum()

        total_units = sales[
            "quantity"
        ].sum()

        transactions = len(sales)

        average_transaction = (
            total_revenue / transactions
            if transactions > 0
            else 0
        )

        # =================================================
        # EXECUTIVE SUMMARY
        # =================================================

        st.subheader(
            "📊 Executive Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Revenue",
            f"${total_revenue:,.2f}"
        )

        col2.metric(
            "📦 Units Sold",
            f"{int(total_units):,}"
        )

        col3.metric(
            "🧾 Transactions",
            f"{transactions:,}"
        )

        col4.metric(
            "💵 Avg. Transaction",
            f"${average_transaction:,.2f}"
        )

        st.divider()

        # =================================================
        # PRODUCT ANALYSIS
        # =================================================

        if "product_name" in sales.columns:

            product_summary = (
                sales
                .groupby("product_name")
                .agg(
                    Revenue=(
                        "total_amount",
                        "sum"
                    ),
                    Units=(
                        "quantity",
                        "sum"
                    ),
                    Transactions=(
                        "product_name",
                        "count"
                    )
                )
                .reset_index()
            )

            # ---------------------------------------------
            # BEST REVENUE PRODUCT
            # ---------------------------------------------

            best_revenue = (
                product_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            # ---------------------------------------------
            # BEST SELLING PRODUCT
            # ---------------------------------------------

            best_seller = (
                product_summary
                .sort_values(
                    "Units",
                    ascending=False
                )
                .iloc[0]
            )

            st.subheader(
                "🏆 Sales Highlights"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.success(
                    f"🏆 **Top Revenue Product**\n\n"
                    f"**{best_revenue['product_name']}**\n\n"
                    f"Generated "
                    f"**${best_revenue['Revenue']:,.2f}** "
                    f"in revenue."
                )

            with col2:

                st.success(
                    f"🔥 **Best-Selling Product**\n\n"
                    f"**{best_seller['product_name']}**\n\n"
                    f"Sold "
                    f"**{int(best_seller['Units'])} units**."
                )

        # =================================================
        # INVENTORY INSIGHTS
        # =================================================

        if not inventory.empty:

            st.divider()

            st.subheader(
                "📦 Inventory Intelligence"
            )

            # ---------------------------------------------
            # LOW STOCK
            # ---------------------------------------------

            low_stock = inventory[
                inventory["quantity"] <= 10
            ].copy()

            # ---------------------------------------------
            # OUT OF STOCK
            # ---------------------------------------------

            out_of_stock = inventory[
                inventory["quantity"] <= 0
            ].copy()

            # ---------------------------------------------
            # HEALTHY STOCK
            # ---------------------------------------------

            healthy_stock = inventory[
                inventory["quantity"] > 10
            ].copy()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🔴 Out of Stock",
                len(out_of_stock)
            )

            col2.metric(
                "🟠 Low Stock",
                len(low_stock)
            )

            col3.metric(
                "🟢 Healthy Stock",
                len(healthy_stock)
            )

            # ---------------------------------------------
            # OUT OF STOCK ALERT
            # ---------------------------------------------

            if not out_of_stock.empty:

                st.error(
                    f"🚨 **{len(out_of_stock)} product(s) "
                    "are completely out of stock.**"
                )

                st.dataframe(
                    out_of_stock[
                        [
                            "product_name",
                            "category",
                            "quantity"
                        ]
                    ],
                    width="stretch",
                    hide_index=True
                )

            # ---------------------------------------------
            # LOW STOCK ALERT
            # ---------------------------------------------

            if not low_stock.empty:

                st.warning(
                    f"⚠️ **{len(low_stock)} product(s) "
                    "need attention because their stock "
                    "is at or below 10 units.**"
                )

                st.dataframe(
                    low_stock[
                        [
                            "product_name",
                            "category",
                            "quantity"
                        ]
                    ],
                    width="stretch",
                    hide_index=True
                )

            if (
                low_stock.empty
                and out_of_stock.empty
            ):

                st.success(
                    "🟢 Inventory levels are currently "
                    "healthy."
                )

        # =================================================
        # SALES + INVENTORY COMBINATION
        # =================================================

        if (
            not inventory.empty
            and "product_name" in sales.columns
            and "product_name" in inventory.columns
        ):

            st.divider()

            st.subheader(
                "🔥 Demand & Restocking Recommendations"
            )

            demand = (
                sales
                .groupby("product_name")[
                    "quantity"
                ]
                .sum()
                .reset_index()
            )

            demand = demand.rename(
                columns={
                    "quantity":
                    "units_sold"
                }
            )

            stock_analysis = inventory[
                [
                    "product_name",
                    "quantity"
                ]
            ].copy()

            stock_analysis = stock_analysis.rename(
                columns={
                    "quantity":
                    "current_stock"
                }
            )

            analysis = demand.merge(
                stock_analysis,
                on="product_name",
                how="left"
            )

            analysis["current_stock"] = (
                analysis["current_stock"]
                .fillna(0)
            )

            # ---------------------------------------------
            # HIGH DEMAND + LOW STOCK
            # ---------------------------------------------

            high_demand = analysis[
                analysis["units_sold"]
                >= analysis["units_sold"].median()
            ]

            urgent_restock = high_demand[
                high_demand["current_stock"] <= 10
            ]

            if not urgent_restock.empty:

                st.error(
                    "🚨 **Priority Restocking Required**"
                )

                for _, row in urgent_restock.iterrows():

                    st.write(
                        f"🔴 **{row['product_name']}** — "
                        f"{int(row['units_sold'])} units sold, "
                        f"only {int(row['current_stock'])} "
                        f"currently in stock."
                    )

                    st.caption(
                        "Recommendation: Consider restocking "
                        "this product soon."
                    )

            else:

                st.success(
                    "🟢 No high-demand products are currently "
                    "at critical stock levels."
                )

            # ---------------------------------------------
            # HIGH STOCK + LOW SALES
            # ---------------------------------------------

            low_demand = analysis[
                analysis["units_sold"]
                < analysis["units_sold"].median()
            ]

            excess_stock = low_demand[
                low_demand["current_stock"] > 20
            ]

            if not excess_stock.empty:

                st.warning(
                    "📦 **Products with High Stock "
                    "and Relatively Low Sales**"
                )

                for _, row in excess_stock.iterrows():

                    st.write(
                        f"🟡 **{row['product_name']}** — "
                        f"{int(row['current_stock'])} units "
                        f"in stock, "
                        f"{int(row['units_sold'])} units sold."
                    )

                    st.caption(
                        "Recommendation: Monitor demand "
                        "before purchasing additional stock."
                    )

        # =================================================
        # PERFORMANCE BY PRODUCT
        # =================================================

        if "product_name" in sales.columns:

            st.divider()

            st.subheader(
                "📋 Product Performance Summary"
            )

            summary = (
                sales
                .groupby("product_name")
                .agg(
                    Revenue=(
                        "total_amount",
                        "sum"
                    ),
                    Units_Sold=(
                        "quantity",
                        "sum"
                    ),
                    Transactions=(
                        "product_name",
                        "count"
                    )
                )
                .reset_index()
            )

            summary["Average Sale"] = (
                summary["Revenue"]
                / summary["Transactions"]
            )

            summary = summary.sort_values(
                "Revenue",
                ascending=False
            )

            display = summary.copy()

            display["Revenue"] = (
                display["Revenue"]
                .map(
                    lambda x:
                    f"${x:,.2f}"
                )
            )

            display["Average Sale"] = (
                display["Average Sale"]
                .map(
                    lambda x:
                    f"${x:,.2f}"
                )
            )

            display = display.rename(
                columns={
                    "product_name":
                    "Product",
                    "Units_Sold":
                    "Units Sold"
                }
            )

            st.dataframe(
                display,
                width="stretch",
                hide_index=True
            )

        # =================================================
        # FINAL RECOMMENDATIONS
        # =================================================

        st.divider()

        st.subheader(
            "💡 Business Recommendations"
        )

        recommendations = []

        # ---------------------------------------------
        # REVENUE RECOMMENDATION
        # ---------------------------------------------

        if total_revenue > 0:

            recommendations.append(
                f"💰 Your recorded sales have generated "
                f"**${total_revenue:,.2f}** in revenue "
                f"across **{transactions} transactions**."
            )

        # ---------------------------------------------
        # PRODUCT RECOMMENDATION
        # ---------------------------------------------

        if "product_name" in sales.columns:

            recommendations.append(
                f"🏆 **{best_revenue['product_name']}** "
                f"is currently your strongest product "
                f"by revenue."
            )

            if (
                best_seller["product_name"]
                != best_revenue["product_name"]
            ):

                recommendations.append(
                    f"📦 **{best_seller['product_name']}** "
                    f"is your volume leader, even though "
                    f"it is not your highest-revenue product."
                )

        # ---------------------------------------------
        # INVENTORY RECOMMENDATION
        # ---------------------------------------------

        if not inventory.empty:

            if not low_stock.empty:

                recommendations.append(
                    f"⚠️ Review the **{len(low_stock)} "
                    "low-stock product(s)** and prioritize "
                    "replenishment based on sales demand."
                )

            else:

                recommendations.append(
                    "🟢 Current inventory levels do not "
                    "show an immediate low-stock warning."
                )

        # ---------------------------------------------
        # DISPLAY
        # ---------------------------------------------

        for recommendation in recommendations:

            st.info(
                recommendation
            )

    finally:

        conn.close()