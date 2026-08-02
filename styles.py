import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL APPLICATION
        ===================================================== */

        .stApp {
            background-color: #070b12;
            color: #e6edf7;
        }

        .main {
            background-color: #070b12;
        }

        /* Main content width and spacing */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #05080d 0%,
                    #070d16 55%,
                    #05080d 100%
                );

            border-right: 1px solid #172a44;

        }


        /* Sidebar internal spacing */

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }


        /* Sidebar title */

        section[data-testid="stSidebar"] h1 {

            color: #ffffff !important;

            font-size: 25px !important;

            font-weight: 750 !important;

            letter-spacing: -0.5px;

        }


        /* Sidebar text */

        section[data-testid="stSidebar"] p {

            color: #718096;

        }


        /* =====================================================
           SIDEBAR NAVIGATION
        ===================================================== */

        section[data-testid="stSidebar"]
        div[role="radiogroup"] {

            gap: 7px;

        }


        /* Individual navigation container */

        section[data-testid="stSidebar"]
        div[role="radiogroup"] label {

            width: 100%;

            min-height: 46px;

            padding: 11px 13px;

            margin: 3px 0;

            border-radius: 10px;

            border: 1px solid transparent;

            background: transparent;

            transition:
                background 0.2s ease,
                border 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;

            cursor: pointer;

        }


        /* Navigation hover */

        section[data-testid="stSidebar"]
        div[role="radiogroup"] label:hover {

            background:
                linear-gradient(
                    135deg,
                    #0b1828,
                    #0a1420
                );

            border-color: #183653;

            transform: translateX(3px);

        }


        /* Navigation text */

        section[data-testid="stSidebar"]
        div[role="radiogroup"] label p {

            color: #9fb2c8 !important;

            font-size: 14px !important;

            font-weight: 600 !important;

            margin: 0 !important;

        }


        /* Active navigation item */

        section[data-testid="stSidebar"]
        div[role="radiogroup"]
        label:has(input:checked) {

            background:
                linear-gradient(
                    135deg,
                    #0d2948,
                    #0a1c31
                );

            border: 1px solid #087cff;

            box-shadow:
                0 5px 20px rgba(
                    0,
                    124,
                    255,
                    0.18
                );

        }


        /* Active navigation text */

        section[data-testid="stSidebar"]
        div[role="radiogroup"]
        label:has(input:checked) p {

            color: #ffffff !important;

            font-weight: 700 !important;

        }


        /* Hide radio circles */

        section[data-testid="stSidebar"]
        div[role="radiogroup"]
        label > div:first-child {

            display: none;

        }


        /* =====================================================
           SIDEBAR CAPTIONS
        ===================================================== */

        section[data-testid="stSidebar"]
        .stCaption {

            color: #52677f !important;

            font-size: 11px !important;

            font-weight: 700 !important;

            letter-spacing: 1.2px;

            text-transform: uppercase;

        }


        /* =====================================================
           SIDEBAR DIVIDERS
        ===================================================== */

        section[data-testid="stSidebar"] hr {

            border-color: #172a44 !important;

            margin-top: 14px;

            margin-bottom: 14px;

        }


        /* =====================================================
           PAGE HEADINGS
        ===================================================== */

        h1 {

            color: #ffffff !important;

            font-weight: 750 !important;

            letter-spacing: -0.7px;

        }


        h2 {

            color: #ffffff !important;

            font-weight: 700 !important;

        }


        h3 {

            color: #e6edf7 !important;

            font-weight: 650 !important;

        }


        /* =====================================================
           BODY TEXT
        ===================================================== */

        .stMarkdown p {

            color: #c3cfdd;

        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        div[data-testid="stMetric"] {

            background:
                linear-gradient(
                    145deg,
                    #0c1420,
                    #080d15
                );

            border: 1px solid #172a44;

            border-radius: 14px;

            padding: 18px;

            box-shadow:
                0 8px 25px rgba(
                    0,
                    0,
                    0,
                    0.25
                );

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;

        }


        div[data-testid="stMetric"]:hover {

            transform: translateY(-2px);

            border-color: #24527d;

        }


        div[data-testid="stMetricLabel"] {

            color: #7fbfff !important;

            font-weight: 600 !important;

        }


        div[data-testid="stMetricValue"] {

            color: #ffffff !important;

            font-weight: 750 !important;

        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {

            background:
                linear-gradient(
                    135deg,
                    #0066ff,
                    #008cff
                );

            color: #ffffff;

            border: none;

            border-radius: 9px;

            min-height: 40px;

            padding: 0.55rem 1.2rem;

            font-weight: 650;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                background 0.2s ease;

        }


        .stButton > button:hover {

            background:
                linear-gradient(
                    135deg,
                    #008cff,
                    #0066ff
                );

            color: #ffffff;

            box-shadow:
                0 0 18px rgba(
                    0,
                    140,
                    255,
                    0.35
                );

            transform: translateY(-1px);

        }


        /* =====================================================
           DOWNLOAD BUTTON
        ===================================================== */

        .stDownloadButton > button {

            background: #0d1624;

            color: #65b8ff;

            border: 1px solid #1d4f7a;

            border-radius: 9px;

            font-weight: 650;

        }


        .stDownloadButton > button:hover {

            background: #102237;

            color: #ffffff;

            border-color: #008cff;

        }


        /* =====================================================
           TEXT INPUTS
        ===================================================== */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {

            background-color: #0b111b !important;

            color: #ffffff !important;

            border: 1px solid #20344f !important;

            border-radius: 9px !important;

        }


        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {

            border-color: #087cff !important;

            box-shadow:
                0 0 0 1px #087cff !important;

        }


        /* =====================================================
           SELECT BOX
        ===================================================== */

        .stSelectbox div[data-baseweb="select"] {

            background-color: #0b111b;

            border-radius: 9px;

        }


        .stSelectbox div[data-baseweb="select"] > div {

            border-color: #20344f;

        }


        /* =====================================================
           DATAFRAME
        ===================================================== */

        div[data-testid="stDataFrame"] {

            border: 1px solid #172a44;

            border-radius: 12px;

            overflow: hidden;

        }


        /* =====================================================
           CONTAINERS
        ===================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {

            border-color: #172a44 !important;

            border-radius: 14px;

            background-color: #080e17;

        }


        /* =====================================================
           EXPANDERS
        ===================================================== */

        div[data-testid="stExpander"] {

            background-color: #0b111b;

            border: 1px solid #172a44;

            border-radius: 12px;

        }


        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {

            border-radius: 10px;

        }


        /* =====================================================
           PROGRESS BAR
        ===================================================== */

        div[data-testid="stProgressBar"] > div > div {

            background:
                linear-gradient(
                    90deg,
                    #0066ff,
                    #00aaff
                );

        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {

            border-color: #172a44 !important;

        }


        /* =====================================================
           RADIO BUTTONS OUTSIDE SIDEBAR
        ===================================================== */

        div[role="radiogroup"] label {

            border-radius: 8px;

        }


        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {

            width: 7px;

            height: 7px;

        }


        ::-webkit-scrollbar-track {

            background: #070b12;

        }


        ::-webkit-scrollbar-thumb {

            background: #20344f;

            border-radius: 10px;

        }


        ::-webkit-scrollbar-thumb:hover {

            background: #087cff;

        }


        /* =====================================================
           FOOTER
        ===================================================== */

        .biz-footer {

            text-align: center;

            margin-top: 50px;

            padding: 20px 0;

            color: #64748b;

            font-size: 13px;

            border-top: 1px solid #16263d;

        }


        .biz-footer span {

            color: #168cff;

            font-weight: 650;

        }


        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 768px) {

            h1 {

                font-size: 28px !important;

            }

            h2 {

                font-size: 23px !important;

            }

            h3 {

                font-size: 19px !important;

            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

def app_footer():

    st.markdown(
        """
        <div class="biz-footer">
            Built by <span>Krishna Rajoo</span>
            · Business Intelligence & Data Management
        </div>
        """,
        unsafe_allow_html=True
    )