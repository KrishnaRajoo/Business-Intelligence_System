import streamlit as st


# =========================================================
# BIZINSIGHTPRO COMPONENTS
# Native Streamlit components only
# No HTML / CSS
# =========================================================


def page_header(
    title,
    subtitle=None,
    icon="📊"
):
    """
    Reusable page header.
    """

    st.title(
        f"{icon} {title}"
    )

    if subtitle:

        st.caption(
            subtitle
        )

    st.divider()


def section_header(
    title,
    subtitle=None
):
    """
    Reusable section heading.
    """

    st.subheader(
        title
    )

    if subtitle:

        st.caption(
            subtitle
        )


def metric_cards(
    products,
    transactions,
    revenue,
    low_stock
):
    """
    Display four business KPI cards.
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Products",
            f"{products:,}"
        )

    with col2:

        st.metric(
            "💰 Transactions",
            f"{transactions:,}"
        )

    with col3:

        st.metric(
            "💵 Revenue",
            f"${revenue:,.2f}"
        )

    with col4:

        st.metric(
            "⚠️ Low Stock",
            f"{low_stock:,}"
        )


def success_message(
    message
):
    """
    Standard success message.
    """

    st.success(
        message
    )


def warning_message(
    message
):
    """
    Standard warning message.
    """

    st.warning(
        message
    )


def error_message(
    message
):
    """
    Standard error message.
    """

    st.error(
        message
    )


def info_message(
    message
):
    """
    Standard information message.
    """

    st.info(
        message
    )


def empty_state(
    message,
    icon="📭"
):
    """
    Display an empty-state message.
    """

    st.info(
        f"{icon} {message}"
    )


def show_loader(
    message="Loading BizInsightPro..."
):
    """
    Native Streamlit loader.

    Use this with:
        with show_loader():
            ...
    """

    return st.spinner(
        message
    )