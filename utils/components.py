import streamlit as st


def metric_card(title, value, icon, description=""):

    with st.container(border=True):

        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown(
                f"""
                <div style="
                    font-size:40px;
                    text-align:center;
                    padding-top:10px;
                ">
                {icon}
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"### {title}"
            )

            st.markdown(
                f"""
                <div style="
                    font-size:32px;
                    font-weight:700;
                ">
                {value}
                </div>
                """,
                unsafe_allow_html=True
            )

            if description:

                st.caption(
                    description
                )