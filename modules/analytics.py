import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import create_connection


def analytics_page():

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("📈 Business Analytics")

    st.caption(
        "Understand sales performance, product demand and "
        "business trends through simple visual reports."
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
                "📊 Analytics will appear after you record "
                "your first sales transaction."
            )

            if not inventory.empty:

                st.subheader(
                    "📦 Current Inventory"
                )

                inventory["quantity"] = pd.to_numeric(
                    inventory["quantity"],
                    errors="coerce"
                ).fillna(0)

                inventory["price"] = pd.to_numeric(
                    inventory["price"],
                    errors="coerce"
                ).fillna(0)

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Products",
                    f"{len(inventory):,}"
                )

                col2.metric(
                    "Units in Stock",
                    f"{int(inventory['quantity'].sum()):,}"
                )

                col3.metric(
                    "Inventory Value",
                    f"${(inventory['quantity'] * inventory['price']).sum():,.2f}"
                )

            return

        # =================================================
        # CLEAN SALES DATA
        # =================================================

        if "quantity" in sales.columns:

            sales["quantity"] = pd.to_numeric(
                sales["quantity"],
                errors="coerce"
            ).fillna(0)

        if "total_amount" in sales.columns:

            sales["total_amount"] = pd.to_numeric(
                sales["total_amount"],
                errors="coerce"
            ).fillna(0)

        # =================================================
        # CLEAN INVENTORY
        # =================================================

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
        # FIND DATE COLUMN
        # =================================================

        date_column = None

        possible_dates = [
            "date",
            "sale_date",
            "created_at",
            "transaction_date",
            "timestamp"
        ]

        for column in possible_dates:

            if column in sales.columns:

                converted = pd.to_datetime(
                    sales[column],
                    errors="coerce"
                )

                if converted.notna().any():

                    sales[column] = converted

                    date_column = column

                    break

        # =================================================
        # FILTERS
        # =================================================

        st.subheader("🎛️ Report Filters")

        filtered_sales = sales.copy()

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # DATE FILTER
        # -------------------------------------------------

        with col1:

            if date_column:

                valid_dates = sales[
                    date_column
                ].dropna()

                if not valid_dates.empty:

                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()

                    date_range = st.date_input(
                        "📅 Select Date Range",
                        value=(
                            min_date,
                            max_date
                        )
                    )

                    if (
                        isinstance(date_range, tuple)
                        and len(date_range) == 2
                    ):

                        start_date, end_date = date_range

                        filtered_sales = filtered_sales[
                            (
                                filtered_sales[date_column].dt.date
                                >= start_date
                            )
                            &
                            (
                                filtered_sales[date_column].dt.date
                                <= end_date
                            )
                        ]

        # -------------------------------------------------
        # PRODUCT FILTER
        # -------------------------------------------------

        with col2:

            if "product_name" in sales.columns:

                products = sorted(
                    sales["product_name"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_products = st.multiselect(
                    "📦 Products",
                    products,
                    placeholder="All products"
                )

                if selected_products:

                    filtered_sales = filtered_sales[
                        filtered_sales["product_name"]
                        .isin(selected_products)
                    ]

        # =================================================
        # CHECK FILTER RESULT
        # =================================================

        if filtered_sales.empty:

            st.warning(
                "No sales records match the selected filters."
            )

            return

        # =================================================
        # KPI SECTION
        # =================================================

        st.divider()

        st.subheader("📊 Business Performance")

        revenue = filtered_sales[
            "total_amount"
        ].sum()

        units_sold = filtered_sales[
            "quantity"
        ].sum()

        transactions = len(
            filtered_sales
        )

        average_sale = (
            revenue / transactions
            if transactions > 0
            else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total Revenue",
            f"${revenue:,.2f}"
        )

        col2.metric(
            "📦 Units Sold",
            f"{int(units_sold):,}"
        )

        col3.metric(
            "🧾 Transactions",
            f"{transactions:,}"
        )

        col4.metric(
            "💵 Average Sale",
            f"${average_sale:,.2f}"
        )

        # =================================================
        # REVENUE TREND
        # =================================================

        if date_column:

            st.divider()

            st.subheader(
                "📈 Revenue Trend"
            )

            daily_revenue = (
                filtered_sales
                .dropna(subset=[date_column])
                .groupby(
                    filtered_sales[
                        date_column
                    ].dt.date
                )["total_amount"]
                .sum()
                .reset_index()
            )

            daily_revenue.columns = [
                "Date",
                "Revenue"
            ]

            if not daily_revenue.empty:

                fig = px.line(
                    daily_revenue,
                    x="Date",
                    y="Revenue",
                    markers=True,
                    title="Daily Revenue"
                )

                fig.update_layout(
                    template="plotly_dark",
                    xaxis_title="Date",
                    yaxis_title="Revenue",
                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )

        # =================================================
        # MONTHLY REVENUE
        # =================================================

        if date_column:

            st.subheader(
                "📊 Monthly Revenue"
            )

            monthly_data = (
                filtered_sales
                .dropna(subset=[date_column])
                .copy()
            )

            monthly_data["Month"] = (
                monthly_data[date_column]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_revenue = (
                monthly_data
                .groupby("Month")[
                    "total_amount"
                ]
                .sum()
                .reset_index()
            )

            if not monthly_revenue.empty:

                fig = px.bar(
                    monthly_revenue,
                    x="Month",
                    y="total_amount",
                    text_auto=".2s",
                    title="Revenue by Month"
                )

                fig.update_layout(
                    template="plotly_dark",
                    xaxis_title="Month",
                    yaxis_title="Revenue"
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )

        # =================================================
        # PRODUCT PERFORMANCE
        # =================================================

        if "product_name" in filtered_sales.columns:

            st.divider()

            st.subheader(
                "🏆 Product Performance"
            )

            product_data = (
                filtered_sales
                .groupby("product_name")
                .agg(
                    Revenue=(
                        "total_amount",
                        "sum"
                    ),
                    Units=(
                        "quantity",
                        "sum"
                    )
                )
                .reset_index()
            )

            # ---------------------------------------------
            # TOP PRODUCTS BY REVENUE
            # ---------------------------------------------

            top_revenue = (
                product_data
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                top_revenue,
                x="Revenue",
                y="product_name",
                orientation="h",
                text_auto=".2s",
                title="Top Products by Revenue"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Revenue",
                yaxis_title="Product"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

            # ---------------------------------------------
            # TOP PRODUCTS BY UNITS
            # ---------------------------------------------

            top_units = (
                product_data
                .sort_values(
                    "Units",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                top_units,
                x="Units",
                y="product_name",
                orientation="h",
                text_auto=True,
                title="Best-Selling Products by Quantity"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Units Sold",
                yaxis_title="Product"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # =================================================
        # REVENUE MIX
        # =================================================

        if "product_name" in filtered_sales.columns:

            st.divider()

            st.subheader(
                "🥧 Revenue Mix"
            )

            revenue_mix = (
                filtered_sales
                .groupby("product_name")[
                    "total_amount"
                ]
                .sum()
                .reset_index()
            )

            revenue_mix = (
                revenue_mix
                .sort_values(
                    "total_amount",
                    ascending=False
                )
            )

            # Keep pie chart readable
            if len(revenue_mix) > 6:

                top = revenue_mix.head(5)

                other_value = (
                    revenue_mix.iloc[5:]
                    ["total_amount"]
                    .sum()
                )

                other = pd.DataFrame({
                    "product_name": ["Other"],
                    "total_amount": [other_value]
                })

                revenue_mix = pd.concat(
                    [
                        top,
                        other
                    ],
                    ignore_index=True
                )

            fig = px.pie(
                revenue_mix,
                names="product_name",
                values="total_amount",
                hole=0.45,
                title="Where Your Revenue Comes From"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # =================================================
        # CATEGORY PERFORMANCE
        # =================================================

        if (
            "product_name" in filtered_sales.columns
            and not inventory.empty
            and "category" in inventory.columns
        ):

            st.divider()

            st.subheader(
                "📊 Category Performance"
            )

            product_category = inventory[
                [
                    "product_name",
                    "category"
                ]
            ].drop_duplicates(
                subset=["product_name"]
            )

            category_sales = filtered_sales.merge(
                product_category,
                on="product_name",
                how="left"
            )

            category_sales["category"] = (
                category_sales["category"]
                .fillna("Other")
            )

            category_data = (
                category_sales
                .groupby("category")
                .agg(
                    Revenue=(
                        "total_amount",
                        "sum"
                    ),
                    Units=(
                        "quantity",
                        "sum"
                    )
                )
                .reset_index()
            )

            # ---------------------------------------------
            # CATEGORY REVENUE
            # ---------------------------------------------

            fig = px.bar(
                category_data,
                x="category",
                y="Revenue",
                text_auto=".2s",
                title="Revenue by Category"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Category",
                yaxis_title="Revenue"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

            # ---------------------------------------------
            # CATEGORY UNITS
            # ---------------------------------------------

            fig = px.bar(
                category_data,
                x="category",
                y="Units",
                text_auto=True,
                title="Units Sold by Category"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Category",
                yaxis_title="Units Sold"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # =================================================
        # INVENTORY HEALTH
        # =================================================

        if not inventory.empty:

            st.divider()

            st.subheader(
                "📦 Inventory Health"
            )

            inventory_chart = inventory.copy()

            inventory_chart = (
                inventory_chart
                .sort_values(
                    "quantity",
                    ascending=True
                )
                .tail(15)
            )

            fig = px.bar(
                inventory_chart,
                x="quantity",
                y="product_name",
                orientation="h",
                text_auto=True,
                title="Current Stock by Product"
            )

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Units in Stock",
                yaxis_title="Product"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

            # ---------------------------------------------
            # STOCK ALERT
            # ---------------------------------------------

            low_stock = inventory[
                inventory["quantity"] <= 10
            ]

            if low_stock.empty:

                st.success(
                    "🟢 Inventory levels look healthy."
                )

            else:

                st.warning(
                    f"⚠️ {len(low_stock)} product(s) "
                    "are currently at low stock levels."
                )

                st.dataframe(
                    low_stock[
                        [
                            "product_name",
                            "category",
                            "quantity",
                            "price"
                        ]
                    ],
                    width="stretch",
                    hide_index=True
                )

        # =================================================
        # BUSINESS SUMMARY
        # =================================================

        st.divider()

        st.subheader(
            "💡 Business Summary"
        )

        if "product_name" in filtered_sales.columns:

            product_summary = (
                filtered_sales
                .groupby("product_name")
                .agg(
                    Revenue=(
                        "total_amount",
                        "sum"
                    ),
                    Units=(
                        "quantity",
                        "sum"
                    )
                )
                .reset_index()
            )

            best_revenue = (
                product_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            best_units = (
                product_summary
                .sort_values(
                    "Units",
                    ascending=False
                )
                .iloc[0]
            )

            col1, col2, col3 = st.columns(3)

            col1.info(
                f"🏆 **Highest Revenue Product**\n\n"
                f"{best_revenue['product_name']}\n\n"
                f"${best_revenue['Revenue']:,.2f}"
            )

            col2.info(
                f"📦 **Most Sold Product**\n\n"
                f"{best_units['product_name']}\n\n"
                f"{int(best_units['Units']):,} units"
            )

            col3.info(
                f"💵 **Average Transaction**\n\n"
                f"${average_sale:,.2f}"
            )

    finally:

        conn.close()