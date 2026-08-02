import pymysql
import pandas as pd
import streamlit as st


# =====================================================
# DATABASE CONNECTION
# =====================================================

def create_connection():

    return pymysql.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        ssl={"ssl": True},
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False
    )


# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    try:

        # -------------------------------------------------
        # INVENTORY
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (

                id INT AUTO_INCREMENT PRIMARY KEY,

                product_name VARCHAR(255) NOT NULL,

                category VARCHAR(255),

                quantity INT DEFAULT 0,

                price DECIMAL(12,2) DEFAULT 0.00,

                supplier VARCHAR(255)

            )
            """
        )

        # -------------------------------------------------
        # SALES
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (

                id INT AUTO_INCREMENT PRIMARY KEY,

                customer VARCHAR(255),

                product_name VARCHAR(255),

                quantity INT DEFAULT 0,

                unit_price DECIMAL(12,2) DEFAULT 0.00,

                total_amount DECIMAL(12,2) DEFAULT 0.00,

                payment_status VARCHAR(100),

                date DATE

            )
            """
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


# =====================================================
# INVENTORY - GET
# =====================================================

def get_inventory_data():

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                product_name,
                category,
                quantity,
                price,
                supplier
            FROM inventory
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        columns = [
            "id",
            "product_name",
            "category",
            "quantity",
            "price",
            "supplier"
        ]

        return pd.DataFrame(rows, columns=columns)

    finally:

        cursor.close()
        conn.close()


# =====================================================
# INVENTORY - ADD
# =====================================================

def add_inventory(
    product_name,
    category,
    quantity,
    price,
    supplier
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO inventory
            (
                product_name,
                category,
                quantity,
                price,
                supplier
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                product_name,
                category,
                quantity,
                price,
                supplier
            )
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# =====================================================
# INVENTORY - UPDATE
# =====================================================

def update_inventory(
    product_id,
    quantity,
    price
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE inventory

            SET
                quantity = %s,
                price = %s

            WHERE id = %s
            """,
            (
                quantity,
                price,
                product_id
            )
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# =====================================================
# INVENTORY - DELETE
# =====================================================

def delete_inventory(product_id):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM inventory
            WHERE id = %s
            """,
            (product_id,)
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# =====================================================
# INVENTORY - CHECK PRODUCT
# =====================================================

def inventory_product_exists(product_name):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT id
            FROM inventory
            WHERE product_name = %s
            LIMIT 1
            """,
            (product_name,)
        )

        return cursor.fetchone() is not None

    finally:

        cursor.close()
        conn.close()


# =====================================================
# SALES - GET
# =====================================================

def get_sales_data():

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                customer,
                product_name,
                quantity,
                unit_price,
                total_amount,
                payment_status,
                date
            FROM sales
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        columns = [
            "id",
            "customer",
            "product_name",
            "quantity",
            "unit_price",
            "total_amount",
            "payment_status",
            "date"
        ]

        return pd.DataFrame(rows, columns=columns)

    finally:

        cursor.close()
        conn.close()


# =====================================================
# SALES - ADD
# =====================================================

def add_sale(
    customer,
    product_name,
    quantity,
    unit_price,
    total_amount,
    payment_status,
    date
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

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
                quantity,
                unit_price,
                total_amount,
                payment_status,
                date
            )
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# =====================================================
# SALES - UPDATE
# =====================================================

def update_sale(
    sale_id,
    quantity,
    unit_price,
    total_amount,
    payment_status
):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE sales

            SET
                quantity = %s,
                unit_price = %s,
                total_amount = %s,
                payment_status = %s

            WHERE id = %s
            """,
            (
                quantity,
                unit_price,
                total_amount,
                payment_status,
                sale_id
            )
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# =====================================================
# SALES - DELETE
# =====================================================

def delete_sale(sale_id):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM sales
            WHERE id = %s
            """,
            (sale_id,)
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()
