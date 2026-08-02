import streamlit as st
import pandas as pd
from datetime import date

from database.database import create_connection


def sales_page():

    st.header("💰 Sales Management")

    conn = create_connection()

    try:

        # ==========================================
        # LOAD DATA
        # ==========================================

        inventory = pd.read_sql(
            "SELECT * FROM inventory",
            conn
        )

        sales = pd.read_sql(
            "SELECT * FROM sales ORDER BY id DESC",
            conn
        )

        # ==========================================
        # CLEAN INVENTORY DATA
        # ==========================================

        if not inventory.empty:

            inventory["quantity"] = pd.to_numeric(
                inventory["quantity"],
                errors="coerce"
            ).fillna(0).astype(int)

            inventory["price"] = pd.to_numeric(
                inventory["price"],
                errors="coerce"
            ).fillna(0.0)

        # ==========================================
        # MENU
        # ==========================================

        menu = st.selectbox(
            "Select Action",
            [
                "Record Sale",
                "Sales History"
            ]
        )

        # ==========================================
        # RECORD SALE
        # ==========================================

        if menu == "Record Sale":

            st.subheader("Create New Transaction")

            if inventory.empty:

                st.warning(
                    "Add inventory before making sales."
                )

                return

            # --------------------------------------
            # PRODUCT SELECTION
            # --------------------------------------

            product_options = inventory.apply(
                lambda row:
                f"{row['product_name']} | "
                f"Stock: {row['quantity']} | "
                f"ID: {row['id']}",
                axis=1
            ).tolist()

            selected_product = st.selectbox(
                "Select Product",
                product_options
            )

            # Extract inventory ID
            selected_id = int(
                selected_product.split("ID: ")[1]
            )

            # Get exact inventory record
            product_data = inventory[
                inventory["id"] == selected_id
            ].iloc[0]

            product_name = str(
                product_data["product_name"]
            )

            available_stock = int(
                product_data["quantity"]
            )

            unit_price = float(
                product_data["price"]
            )

            # --------------------------------------
            # PRODUCT INFORMATION
            # --------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"📦 Available Stock: "
                    f"{available_stock} units"
                )

            with col2:

                st.info(
                    f"💵 Unit Price: "
                    f"${unit_price:,.2f}"
                )

            # --------------------------------------
            # CUSTOMER
            # --------------------------------------

            customer = st.text_input(
                "Customer Name",
                placeholder="Enter customer name"
            )

            # --------------------------------------
            # QUANTITY
            # --------------------------------------

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=max(1, available_stock),
                value=1,
                step=1
            )

            # --------------------------------------
            # TOTAL
            # --------------------------------------

            total = float(quantity) * unit_price

            st.success(
                f"💰 Total Amount: "
                f"${total:,.2f}"
            )

            # --------------------------------------
            # PAYMENT STATUS
            # --------------------------------------

            payment = st.selectbox(
                "Payment Status",
                [
                    "Paid",
                    "Pending",
                    "Cancelled"
                ]
            )

            # ======================================
            # RECORD SALE
            # ======================================

            if st.button(
                "Record Sale",
                type="primary",
                width="stretch"
            ):

                # ----------------------------------
                # VALIDATION
                # ----------------------------------

                customer = customer.strip()

                if not customer:

                    st.error(
                        "Please enter the customer name."
                    )

                    return

                if quantity <= 0:

                    st.error(
                        "Quantity must be greater than 0."
                    )

                    return

                if quantity > available_stock:

                    st.error(
                        f"❌ Insufficient stock. "
                        f"Only {available_stock} "
                        f"units available."
                    )

                    return

                # ----------------------------------
                # CANCELLED SALE
                # ----------------------------------

                if payment == "Cancelled":

                    st.warning(
                        "Cancelled transactions do not "
                        "reduce inventory."
                    )

                    return

                # ----------------------------------
                # CALCULATE NEW STOCK
                # ----------------------------------

                new_stock = (
                    available_stock - int(quantity)
                )

                cursor = conn.cursor()

                try:

                    # ==============================
                    # INSERT SALE
                    # ==============================

                    cursor.execute(
                        """
                        INSERT INTO sales
                        (
                            customer,
                            product_name,
                            quantity,
                            unit_price,
                            total_amount,
                            payment_status,
                            date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            customer,
                            product_name,
                            int(quantity),
                            unit_price,
                            total,
                            payment,
                            date.today()
                        )
                    )

                    # ==============================
                    # UPDATE INVENTORY
                    # ==============================

                    cursor.execute(
                        """
                        UPDATE inventory
                        SET quantity = %s
                        WHERE id = %s
                        """,
                        (
                            int(new_stock),
                            selected_id
                        )
                    )

                    # ==============================
                    # COMMIT BOTH OPERATIONS
                    # ==============================

                    conn.commit()

                    st.success(
                        f"✅ Sale recorded successfully. "
                        f"{product_name} stock is now "
                        f"{new_stock} units."
                    )

                    st.rerun()

                except Exception as e:

                    # --------------------------------
                    # ROLLBACK IF ANYTHING FAILS
                    # --------------------------------

                    conn.rollback()

                    st.error(
                        f"❌ Failed to record sale: {e}"
                    )

                finally:

                    cursor.close()

        # ==========================================
        # SALES HISTORY
        # ==========================================

        else:

            st.subheader("🧾 Transaction History")

            if not sales.empty:

                # ----------------------------------
                # CLEAN DATE
                # ----------------------------------

                if "date" in sales.columns:

                    sales["date"] = pd.to_datetime(
                        sales["date"],
                        errors="coerce"
                    ).dt.strftime("%Y-%m-%d")

                # ----------------------------------
                # SEARCH
                # ----------------------------------

                search = st.text_input(
                    "🔍 Search Customer / Product",
                    placeholder="Search customer or product..."
                )

                filtered = sales.copy()

                if search:

                    search = search.strip()

                    filtered = filtered[
                        filtered.astype(str)
                        .apply(
                            lambda row:
                            row.str.contains(
                                search,
                                case=False,
                                na=False
                            ).any(),
                            axis=1
                        )
                    ]

                # ----------------------------------
                # SALES SUMMARY
                # ----------------------------------

                total_transactions = len(filtered)

                total_units_sold = (
                    pd.to_numeric(
                        filtered["quantity"],
                        errors="coerce"
                    ).fillna(0).sum()
                    if not filtered.empty
                    else 0
                )

                total_revenue = (
                    pd.to_numeric(
                        filtered["total_amount"],
                        errors="coerce"
                    ).fillna(0).sum()
                    if not filtered.empty
                    else 0
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "🧾 Transactions",
                    f"{total_transactions:,}"
                )

                col2.metric(
                    "📦 Units Sold",
                    f"{int(total_units_sold):,}"
                )

                col3.metric(
                    "💰 Revenue",
                    f"${total_revenue:,.2f}"
                )

                st.divider()

                # ----------------------------------
                # DISPLAY HISTORY
                # ----------------------------------

                st.dataframe(
                    filtered,
                    width="stretch",
                    hide_index=True
                )

                st.caption(
                    f"Showing {len(filtered)} "
                    f"of {len(sales)} transactions."
                )

            else:

                st.info(
                    "No sales recorded yet."
                )

    finally:

        # ==========================================
        # CLOSE DATABASE CONNECTION
        # ==========================================

        conn.close()
