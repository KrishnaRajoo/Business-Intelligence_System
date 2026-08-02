import streamlit as st
import time


def show_startup_loader(
    duration=2.5
):
    """
    Shows the BizInsightPro startup loader only once
    per Streamlit browser session.
    """

    # Already shown in this session
    if st.session_state.get("startup_loader_shown", False):
        return

    # Mark it immediately so navigation/reruns
    # don't trigger the loader again
    st.session_state["startup_loader_shown"] = True

    loader = st.empty()

    with loader.container():

        # ---------------------------------------------
        # SPACE
        # ---------------------------------------------

        for _ in range(5):
            st.write("")

        # ---------------------------------------------
        # BRAND
        # ---------------------------------------------

        st.markdown(
            "# 🔷",
            text_alignment="center"
        )

        st.markdown(
            "# BizInsightPro",
            text_alignment="center"
        )

        st.markdown(
            "### Business Intelligence System",
            text_alignment="center"
        )

        st.caption(
            "Preparing your business intelligence dashboard...",
            text_alignment="center"
        )

        st.write("")

        # ---------------------------------------------
        # PROGRESS
        # ---------------------------------------------

        progress = st.progress(
            0,
            text="Starting BizInsightPro..."
        )

        percentage = st.empty()

        status = st.empty()

        # ---------------------------------------------
        # STARTUP STEPS
        # ---------------------------------------------

        steps = [
            (15, "🔌 Connecting to business database..."),
            (35, "📦 Loading inventory records..."),
            (55, "💰 Loading sales transactions..."),
            (75, "📈 Preparing analytics..."),
            (90, "💡 Preparing business insights..."),
            (100, "🚀 BizInsightPro is ready!")
        ]

        delay = duration / len(steps)

        for value, message in steps:

            progress.progress(
                value,
                text=message
            )

            percentage.markdown(
                f"### {value}%",
                text_alignment="center"
            )

            status.caption(
                message,
                text_alignment="center"
            )

            time.sleep(delay)

        st.success(
            "✓ Dashboard ready"
        )

        time.sleep(0.3)

    loader.empty()