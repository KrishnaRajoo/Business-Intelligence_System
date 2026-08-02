import streamlit as st
import pandas as pd

from database.database import (
    get_inventory_data,
    add_inventory,
    update_inventory,
    delete_inventory,
    inventory_product_exists
)


def inventory_page():

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("📦 Inventory Management")

    st.caption(
        "Manage products, stock levels, pricing and suppliers."
    )

    st.divider()

    # =====================================================
    # FETCH INVENTORY
    # =====================================================

    df = get_inventory_data()

    # =====================================================
    # CLEAN DATA
    # =====================================================

    if not df.empty:

        df["quantity"] = pd.to_numeric(
            df["quantity"],
            errors="coerce"
        ).fillna(0)

        df["price"] = pd.to_numeric(
            df["price"],
            errors="coerce"
        ).fillna(0)

    # =====================================================
    # KPI SECTION
    # =====================================================

    st.subheader("📊 Inventory Overview")

    total_products = len(df)

    total_units = (
        int(df["quantity"].sum())
        if not df.empty
        else 0
    )

    inventory_value = (
        (df["quantity"] * df["price"]).sum()
        if not df.empty
        else 0
    )

    low_stock = (
        len(df[df["quantity"] <= 10])
        if not df.empty
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📦 Products",
        f"{total_products:,}"
    )

    col2.metric(
        "🔢 Units",
        f"{total_units:,}"
    )

    col3.metric(
        "💰 Inventory Value",
        f"${inventory_value:,.2f}"
    )

    col4.metric(
        "⚠️ Low Stock",
        f"{low_stock:,}"
    )

    st.divider()

    # =====================================================
    # ACTION
    # =====================================================

    option = st.selectbox(
        "Inventory Action",
        [
            "View Inventory",
            "Add Product",
            "Edit Product",
            "Delete Product"
        ]
    )

    st.divider()

    # =====================================================
    # ADD PRODUCT
    # =====================================================

    if option == "Add Product":

        st.subheader("➕ Add New Product")

        with st.form(
            "add_product_form",
            clear_on_submit=True
        ):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Product Name",
                    placeholder="e.g. Wireless Mouse"
                )

                category = st.text_input(
                    "Category",
                    placeholder="e.g. Electronics"
                )

                supplier = st.text_input(
                    "Supplier",
                    placeholder="e.g. ABC Suppliers"
                )

            with col2:

                quantity = st.number_input(
                    "Quantity",
                    min_value=0,
                    step=1
                )

                price = st.number_input(
                    "Price",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )

            submitted = st.form_submit_button(
                "➕ Add Product",
                width="stretch"
            )

            if submitted:

                # -----------------------------------------
                # VALIDATION
                # -----------------------------------------

                name = name.strip()
                category = category.strip()
                supplier = supplier.strip()

                if not name:

                    st.error(
                        "Please enter a product name."
                    )

                elif not category:

                    st.error(
                        "Please enter a category."
                    )

                elif quantity <= 0:

                    st.error(
                        "Quantity must be greater than 0."
                    )

                elif price < 0:

                    st.error(
                        "Price cannot be negative."
                    )

                else:

                    # -------------------------------------
                    # CHECK EXISTING PRODUCT
                    # -------------------------------------

                    existing = inventory_product_exists(
                        name
                    )

                    if existing:

                        st.warning(
                            f"'{name}' already exists "
                            "in inventory."
                        )

                        st.info(
                            "Use 'Edit Product' to update "
                            "its stock instead of creating "
                            "a duplicate."
                        )

                    else:

                        # ---------------------------------
                        # ADD TO MYSQL
                        # ---------------------------------

                        add_inventory(
                            product_name=name,
                            category=category,
                            quantity=quantity,
                            price=price,
                            supplier=supplier
                        )

                        st.success(
                            f"✅ {name} added successfully."
                        )

                        st.rerun()

    # =====================================================
    # VIEW INVENTORY
    # =====================================================

    elif option == "View Inventory":

        st.subheader("📋 Inventory Records")

        if df.empty:

            st.info(
                "No inventory available. "
                "Add your first product."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                search = st.text_input(
                    "🔍 Search Product",
                    placeholder="Search product name..."
                )

            with col2:

                categories = sorted(
                    df["category"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                category = st.selectbox(
                    "Filter Category",
                    ["All"] + categories
                )

            # ---------------------------------------------
            # FILTER
            # ---------------------------------------------

            filtered = df.copy()

            if search:

                filtered = filtered[
                    filtered["product_name"]
                    .astype(str)
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            if category != "All":

                filtered = filtered[
                    filtered["category"]
                    .astype(str)
                    == category
                ]

            # ---------------------------------------------
            # INVENTORY VALUE
            # ---------------------------------------------

            filtered = filtered.copy()

            filtered["Inventory Value"] = (
                filtered["quantity"]
                *
                filtered["price"]
            )

            # ---------------------------------------------
            # DISPLAY
            # ---------------------------------------------

            display_columns = [
                "id",
                "product_name",
                "category",
                "quantity",
                "price",
                "supplier",
                "Inventory Value"
            ]

            available_columns = [
                column
                for column in display_columns
                if column in filtered.columns
            ]

            display_df = filtered[
                available_columns
            ].copy()

            display_df = display_df.rename(
                columns={
                    "id": "ID",
                    "product_name": "Product",
                    "category": "Category",
                    "quantity": "Quantity",
                    "price": "Price",
                    "supplier": "Supplier"
                }
            )

            st.dataframe(
                display_df,
                width="stretch",
                hide_index=True
            )

            st.caption(
                f"Showing {len(filtered)} "
                f"of {len(df)} products."
            )

    # =====================================================
    # EDIT PRODUCT
    # =====================================================

    elif option == "Edit Product":

        st.subheader("✏️ Edit Product")

        if df.empty:

            st.info(
                "No products available to edit."
            )

        else:

            product_options = {
                f"{row['product_name']} "
                f"(ID: {row['id']})": row["id"]
                for _, row in df.iterrows()
            }

            selected_product = st.selectbox(
                "Select Product",
                list(product_options.keys())
            )

            product_id = product_options[
                selected_product
            ]

            product = df[
                df["id"] == product_id
            ].iloc[0]

            st.info(
                f"Editing: {product['product_name']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                quantity = st.number_input(
                    "Update Quantity",
                    min_value=0,
                    value=int(product["quantity"]),
                    step=1
                )

            with col2:

                price = st.number_input(
                    "Update Price",
                    min_value=0.0,
                    value=float(product["price"]),
                    step=0.01,
                    format="%.2f"
                )

            if st.button(
                "💾 Update Product",
                width="stretch"
            ):

                if quantity < 0:

                    st.error(
                        "Quantity cannot be negative."
                    )

                elif price < 0:

                    st.error(
                        "Price cannot be negative."
                    )

                else:

                    # -------------------------------------
                    # UPDATE MYSQL
                    # -------------------------------------

                    update_inventory(
                        product_id=product_id,
                        quantity=quantity,
                        price=price
                    )

                    st.success(
                        f"✅ {product['product_name']} "
                        "updated successfully."
                    )

                    st.rerun()

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    elif option == "Delete Product":

        st.subheader("🗑️ Delete Product")

        if df.empty:

            st.info(
                "No products available to delete."
            )

        else:

            product_options = {
                f"{row['product_name']} "
                f"(ID: {row['id']})": row["id"]
                for _, row in df.iterrows()
            }

            selected_product = st.selectbox(
                "Select Product",
                list(product_options.keys())
            )

            product_id = product_options[
                selected_product
            ]

            product = df[
                df["id"] == product_id
            ].iloc[0]

            st.warning(
                f"You are about to delete "
                f"**{product['product_name']}**."
            )

            confirm = st.checkbox(
                "I understand that this product "
                "will be permanently deleted."
            )

            if st.button(
                "🗑️ Delete Product",
                width="stretch"
            ):

                if not confirm:

                    st.error(
                        "Please confirm deletion first."
                    )

                else:

                    # ---------------------------------
                    # DELETE FROM MYSQL
                    # ---------------------------------

                    delete_inventory(
                        product_id
                    )

                    st.success(
                        f"✅ {product['product_name']} "
                        "deleted successfully."
                    )

                    st.rerun()
