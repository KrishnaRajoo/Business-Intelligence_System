import streamlit as st

from styles import apply_theme, app_footer
from database.database import create_tables
from utils.loader import show_startup_loader

from modules.about import about_page
from modules.inventory import inventory_page
from modules.sales import sales_page
from modules.dashboard import dashboard_page
from modules.reports import reports_page
from modules.analytics import analytics_page
from modules.insights import insights_page
from modules.growth import growth_page
from modules.product_intelligence import product_intelligence_page
from modules.inventory_intelligence import inventory_intelligence_page
from modules.recommendations import recommendations_page


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BizInsightPro",
    page_icon="🔷",
    layout="wide"
)


# =====================================================
# STARTUP LOADER
# =====================================================

show_startup_loader()


# =====================================================
# APPLY APPLICATION THEME
# =====================================================

apply_theme()

# =====================================================
# SIDEBAR BRANDING
# =====================================================

st.sidebar.markdown(
    """
    <h1 style="
        text-align:center;
        margin-bottom:4px;
    ">
        🔷 BizInsightPro
    </h1>

    <p style="
        text-align:center;
        color:#00aaff;
        font-size:13px;
        margin-top:0;
    ">
        Business Intelligence System
    </p>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.caption("NAVIGATION")

    menu = st.radio(
        "Pages",
        [
            "ℹ️ About",
            "📊 Dashboard",
            "📦 Inventory",
            "💰 Sales",
            "📈 Analytics",
            "💡 Insights",
            "📈 Growth",
            "🧠 Product Intelligence",
            "📦 Inventory Intelligence",
            "🎯 Recommendations",
            "📄 Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    # -------------------------------------------------
    # SYSTEM STATUS
    # -------------------------------------------------

    st.caption("SYSTEM")

    st.success(
        "● System Online"
    )

    st.caption(
        "BizInsightPro v1.0"
    )


# =====================================================
# PAGE ROUTING
# =====================================================
if menu == "ℹ️ About":
    about_page()

elif menu == "📊 Dashboard":

    dashboard_page()


elif menu == "📦 Inventory":

    inventory_page()


elif menu == "💰 Sales":

    sales_page()


elif menu == "📈 Analytics":

    analytics_page()


elif menu == "💡 Insights":

    insights_page()


elif menu == "📈 Growth":

    growth_page()


elif menu == "🧠 Product Intelligence":

    product_intelligence_page()


elif menu == "📦 Inventory Intelligence":

    inventory_intelligence_page()


elif menu == "🎯 Recommendations":

    recommendations_page()


elif menu == "📄 Reports":

    reports_page()


# =====================================================
# APPLICATION FOOTER
# =====================================================

app_footer()

