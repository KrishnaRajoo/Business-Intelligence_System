import streamlit as st


def about_page():

    # =====================================================
    # CENTERED PAGE TITLE
    # =====================================================

    st.title("🔷BizInsightPro")

    st.caption(
        "Business Intelligence • Data Management • Analytics • Intelligence"
    )

    st.divider()


    # =====================================================
    # INTRODUCTION
    # =====================================================

    st.header("What is BizInsightPro?")

    st.write(
        """
        BizInsightPro is a business intelligence and data management
        platform designed to help businesses manage their daily
        operations, understand their performance and make
        data-driven decisions.
        """
    )

    st.write(
        """
        The platform combines inventory management, sales management,
        analytics, business insights, growth analysis and intelligent
        recommendations into one application.
        """
    )


    # =====================================================
    # CORE CAPABILITIES
    # =====================================================

    st.header("🚀 Core Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):
            st.subheader("📊 Business Dashboard")
            st.write(
                "Monitor important KPIs including products, transactions, "
                "revenue and inventory health."
            )

        with st.container(border=True):
            st.subheader("📦 Inventory Management")
            st.write(
                "Add, update, search and manage products, quantities, "
                "categories, prices and suppliers."
            )

        with st.container(border=True):
            st.subheader("💰 Sales Management")
            st.write(
                "Record sales transactions and keep sales activity "
                "connected with inventory."
            )

        with st.container(border=True):
            st.subheader("📈 Analytics")
            st.write(
                "Understand business performance through charts, "
                "trends and easy-to-understand visualizations."
            )

        with st.container(border=True):
            st.subheader("💡 Business Insights")
            st.write(
                "Analyze business records and identify useful "
                "patterns and observations."
            )


    with col2:

        with st.container(border=True):
            st.subheader("🚀 Growth Analysis")
            st.write(
                "Evaluate business performance and identify "
                "potential growth opportunities."
            )

        with st.container(border=True):
            st.subheader("🧠 Product Intelligence")
            st.write(
                "Analyze product-level performance and identify "
                "products that require attention."
            )

        with st.container(border=True):
            st.subheader("📦 Inventory Intelligence")
            st.write(
                "Monitor stock conditions and identify products "
                "that may require inventory action."
            )

        with st.container(border=True):
            st.subheader("🎯 Recommendations")
            st.write(
                "Generate data-driven recommendations based on "
                "available business information."
            )

        with st.container(border=True):
            st.subheader("📄 Reports")
            st.write(
                "Generate structured reports for reviewing "
                "business performance and records."
            )


    # =====================================================
    # TECHNOLOGY STACK
    # =====================================================

    st.header("⚙️ Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:

        with st.container(border=True):
            st.subheader("🐍 Python")
            st.write(
                "Core programming language used for application "
                "logic and data processing."
            )

        with st.container(border=True):
            st.subheader("⚡ Streamlit")
            st.write(
                "Framework used to build the interactive web application."
            )

    with tech2:

        with st.container(border=True):
            st.subheader("🗄️ SQLite")
            st.write(
                "Database used to store inventory and sales records."
            )

        with st.container(border=True):
            st.subheader("🐼 Pandas")
            st.write(
                "Used for data manipulation, processing and analysis."
            )

    with tech3:

        with st.container(border=True):
            st.subheader("📊 Plotly")
            st.write(
                "Used to create interactive business charts and analytics."
            )

        with st.container(border=True):
            st.subheader("🤖 Scikit-learn")
            st.write(
                "Used for machine learning and intelligent analysis."
            )


    # =====================================================
    # HOW IT WORKS
    # =====================================================

    st.header("🔄 How BizInsightPro Works")

    steps = [
        (
            "01",
            "Data Management",
            "Products, inventory and sales transactions are "
            "recorded in the application."
        ),
        (
            "02",
            "Data Storage",
            "Business records are stored in the application's "
            "database for future access."
        ),
        (
            "03",
            "Analytics",
            "Historical records are processed to calculate "
            "important business metrics and identify trends."
        ),
        (
            "04",
            "Business Intelligence",
            "The intelligence modules analyze available "
            "business information."
        ),
        (
            "05",
            "Decision Making",
            "Dashboards, charts, insights and recommendations "
            "help users make better business decisions."
        ),
    ]

    for number, title, description in steps:

        with st.container(border=True):

            st.subheader(f"{number} — {title}")

            st.write(description)


    # =====================================================
    # DATA MANAGEMENT
    # =====================================================

    st.header("🗄️ Data Management")

    st.write(
        """
        BizInsightPro stores business records so that information
        remains available when the application is accessed again.
        """
    )

    st.info(
        "Inventory and sales records are stored in the application's "
        "SQLite database."
    )


    # =====================================================
    # PURPOSE
    # =====================================================

    st.header("🎯 Purpose of BizInsightPro")

    with st.container(border=True):

        st.subheader("Built for Better Business Decisions")

        st.write(
            """
            BizInsightPro is built around a simple idea:

            Business data should not simply be stored —
            it should be understood.

            The platform combines data management, analytics and
            intelligence to transform everyday business records
            into useful information.
            """
        )


    # =====================================================
    # APPLICATION MODULES
    # =====================================================

    st.header("🧩 Application Modules")

    modules = [
        "Dashboard",
        "Inventory",
        "Sales",
        "Analytics",
        "Insights",
        "Growth",
        "Product Intelligence",
        "Inventory Intelligence",
        "Recommendations",
        "Reports",
        "About",
    ]

    st.write(" • ".join(modules))


    # =====================================================
    # VERSION
    # =====================================================

    st.divider()

    st.caption(
        "🔷 BizInsightPro | Business Intelligence Platform | Version 1.0"
    )
