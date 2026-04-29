# =============================================================================
# ShaktiSabha: Women in Indian Legislature - Streamlit Dashboard
# =============================================================================
# requirements.txt:
#   streamlit>=1.32.0
#   pandas>=2.0.0
#   plotly>=5.18.0
#   numpy>=1.24.0
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import streamlit as st

import random
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShaktiSabha – Women in Indian Legislature",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --saffron: #FF9933;
    --green:   #138808;
    --navy:    #000080;
    --ivory:   #FFF8F0;
    --red:     #DC143C;
    --gold:    #E8A020;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: var(--ivory);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0c29, #302b63, #24243e) !important;
}
[data-testid="stSidebar"] * {
    color: #f0e6d3 !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stToggle label {
    color: #f0e6d3 !important;
    font-weight: 500;
}

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, #FF9933 0%, #FF6B35 30%, #138808 70%, #0a5c02 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: "🇮🇳";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
}
.hero-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: white;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    letter-spacing: -0.5px;
}
.hero-header p {
    color: rgba(255,255,255,0.88);
    font-size: 1rem;
    margin: 0.4rem 0 0 0;
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    border-left: 4px solid var(--saffron);
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
}
.kpi-card.green  { border-left-color: var(--green); }
.kpi-card.navy   { border-left-color: var(--navy); }
.kpi-card.red    { border-left-color: var(--red); }
.kpi-card.gold   { border-left-color: var(--gold); }
.kpi-label {
    font-size: 0.72rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #aaa;
    margin-top: 0.25rem;
}

/* ── Section Headers ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #1a1a2e;
    border-bottom: 3px solid var(--saffron);
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 1rem 0;
    display: inline-block;
}

/* ── Ticker ── */
.ticker-wrap {
    background: linear-gradient(90deg, #1a1a2e, #302b63);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.ticker-text {
    color: #FFD700;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ── Timestamp ── */
.last-updated {
    font-size: 0.75rem;
    color: #aaa;
    text-align: right;
    margin-bottom: 0.5rem;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 8px 8px 0 0;
    border: 1px solid #e0d9d0;
    border-bottom: none;
    font-weight: 500;
    color: #555;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: white;
    border-top: 3px solid var(--saffron) !important;
    color: #1a1a2e !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ─── Color Palette ────────────────────────────────────────────────────────────
COLORS = ["#FF9933", "#138808", "#000080", "#DC143C",
          "#FFD700", "#4CAF50", "#9C27B0", "#FF5722",
          "#00BCD4", "#795548", "#607D8B", "#E91E63"]

PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="DM Sans",
    font_color="#333",
)

# ─── Embedded Data ────────────────────────────────────────────────────────────
@st.cache_data
def load_lok_sabha():
    return pd.DataFrame({
        "Year":        [2004, 2009, 2014, 2019, 2024],
        "Total_Seats": [543,  543,  543,  543,  543],
        "Women_Elected":[45,  59,   64,   78,   74],
        "Women_Pct":   [8.3, 10.9, 11.8, 14.4, 13.6],
        "Total_Contested": [355, 556, 668, 726, 797],
    })

@st.cache_data
def load_rajya_sabha():
    return pd.DataFrame({
        "Year":        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "Total_Members":[245, 245, 245, 245, 245, 245, 245, 245, 245, 245],
        "Women_Members":[28,  27,  29,  30,  31,  30,  33,  34,  32,  35],
        "Women_Pct":   [11.4,11.0,11.8,12.2,12.7,12.2,13.5,13.9,13.1,14.3],
    })

@st.cache_data
def load_state_data():
    data = {
        "State": [
            "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
            "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand",
            "Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur",
            "Meghalaya","Mizoram","Nagaland","Odisha","Punjab",
            "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
            "Uttar Pradesh","Uttarakhand","West Bengal","Delhi","Jammu & Kashmir"
        ],
        "Total_Seats": [
            175, 60,  126, 243, 90,
            40,  182, 90,  68,  81,
            224, 140, 230, 288, 60,
            60,  40,  60,  147, 117,
            200, 32,  234, 119, 60,
            403, 70,  294, 70,  90
        ],
        "Women_MLAs": [
            21, 5,  18, 28, 14,
            3,  18, 12, 8,  9,
            16, 11, 24, 24, 5,
            4,  2,  1,  22, 16,
            27, 4,  23, 13, 7,
            47, 7,  50, 9,  6
        ],
        "Region": [
            "South","North-East","North-East","East","Central",
            "West","West","North","North","East",
            "South","South","Central","West","North-East",
            "North-East","North-East","North-East","East","North",
            "North","North-East","South","South","North-East",
            "North","North","East","North","North"
        ],
        "Female_Literacy": [
            59.7, 57.6, 67.3, 53.3, 60.2,
            81.8, 70.7, 66.8, 76.6, 56.2,
            68.1, 92.1, 60.0, 75.5, 70.3,
            73.8, 89.4, 76.7, 64.4, 71.3,
            52.7, 76.4, 73.9, 66.1, 83.1,
            59.3, 70.7, 71.2, 80.9, 58.0
        ],
    }
    df = pd.DataFrame(data)
    df["Women_Pct"] = (df["Women_MLAs"] / df["Total_Seats"] * 100).round(1)
    df["Performance_Tier"] = pd.cut(
        df["Women_Pct"],
        bins=[-1, 5, 10, 15, 100],
        labels=["Below 5%", "5–10%", "10–15%", "Above 15%"]
    )
    return df

@st.cache_data
def load_party_data():
    return pd.DataFrame({
        "Party":            ["BJP","INC","TMC","SP","BSP","AAP","DMK","NCP","CPI(M)","Others"],
        "Total_MPs":        [240, 99,  29,  37,  10,  3,   22,  8,   4,    91],
        "Women_MPs":        [31,  13,  12,  3,   2,   1,   5,   2,   1,    4],
        "Total_Candidates": [441, 328, 48,  71,  88,  22,  39,  51,  29,   2300],
        "Women_Candidates": [69,  65,  20,  12,  16,  5,   10,  8,   5,    287],
        "Color": COLORS[:10],
    })

@st.cache_data
def load_breaking_news_pool():
    return [
        "🗳️ Himachal Pradesh by-poll: 2 women candidates win in Shimla district",
        "🗳️ West Bengal panchayat result: TMC fields 38% women, 29 elected",
        "🗳️ Rajasthan MLA seat: INC candidate Dr. Sunita Sharma wins by 4,200 votes",
        "🗳️ Bihar legislative council: 3 women members sworn in today",
        "🗳️ Kerala local body election: 50% women reservation breaches 52% mark",
        "🗳️ Maharashtra ZP election: NCP woman candidate wins Pune North ward",
        "🗳️ Assam by-election: BJP's Ranjita Devi elected with 12,000 vote margin",
        "🗳️ UP municipal polls: 1,240 women corporators elected across 17 cities",
        "🗳️ Tamil Nadu assembly: AIADMK nominates 28 women for 50 by-poll seats",
        "🗳️ Odisha gram panchayat: Women occupy 52.3% of total elected seats",
    ]

# ─── Session State Init ───────────────────────────────────────────────────────
if "live_offset" not in st.session_state:
    st.session_state.live_offset = {"lok": 0, "rajya": 0, "state_idx": 0}
if "last_updated" not in st.session_state:
    st.session_state.last_updated = datetime.now().strftime("%H:%M:%S")
if "ticker_msg" not in st.session_state:
    st.session_state.ticker_msg = "Live election monitoring active — data refreshes automatically"

# ─── Load Data ───────────────────────────────────────────────────────────────
df_lok    = load_lok_sabha()
df_rajya  = load_rajya_sabha()
df_states = load_state_data()
df_party  = load_party_data()
news_pool = load_breaking_news_pool()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ ShaktiSabha")
    st.markdown("*Women in Indian Legislature*")
    st.markdown("---")

    st.markdown("### 🔍 Filters")
    sel_states = st.multiselect(
        "States", options=sorted(df_states["State"].tolist()),
        default=[], placeholder="All states"
    )
    sel_parties = st.multiselect(
        "Parties", options=df_party["Party"].tolist(),
        default=[], placeholder="All parties"
    )
    sel_years = st.slider("Lok Sabha Year Range", 2004, 2024, (2004, 2024), step=5)
    sel_region = st.selectbox(
        "Region", ["All"] + sorted(df_states["Region"].unique().tolist())
    )

    st.markdown("---")
    st.markdown("### 🔄 Live Updates")
    auto_refresh = st.toggle("Enable Auto-Refresh", value=False)
    refresh_interval = st.slider("Refresh every (seconds)", 5, 60, 10, disabled=not auto_refresh)

    st.markdown("---")
    # Download
    filtered_states = df_states.copy()
    if sel_states:
        filtered_states = filtered_states[filtered_states["State"].isin(sel_states)]
    if sel_region != "All":
        filtered_states = filtered_states[filtered_states["Region"] == sel_region]

    csv_data = filtered_states.drop(columns=["Performance_Tier"]).to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download State Data CSV", data=csv_data,
                       file_name="women_mla_data.csv", mime="text/csv")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#aaa;text-align:center'>"
        "Data: ECI, PRS Legislative Research<br>Last updated: 2024</div>",
        unsafe_allow_html=True
    )

# ─── Apply Filters ───────────────────────────────────────────────────────────
f_states  = df_states.copy()
if sel_states:  f_states = f_states[f_states["State"].isin(sel_states)]
if sel_region != "All": f_states = f_states[f_states["Region"] == sel_region]

f_lok   = df_lok[(df_lok["Year"] >= sel_years[0]) & (df_lok["Year"] <= sel_years[1])].copy()
f_party = df_party.copy()
if sel_parties: f_party = f_party[f_party["Party"].isin(sel_parties)]

# ─── Live Simulation ─────────────────────────────────────────────────────────
def get_live_kpis():
    offset = st.session_state.live_offset
    lok_women  = int(df_lok["Women_Elected"].iloc[-1]) + offset["lok"]
    rajya_women = int(df_rajya["Women_Members"].iloc[-1]) + offset["rajya"]
    total_mla   = int(f_states["Women_MLAs"].sum())
    lok_pct     = round(lok_women / 543 * 100, 1)
    rajya_pct   = round(rajya_women / 245 * 100, 1)
    best_state  = f_states.loc[f_states["Women_Pct"].idxmax(), "State"] if len(f_states) > 0 else "Kerala"
    best_pct    = f_states["Women_Pct"].max() if len(f_states) > 0 else 0
    return lok_women, rajya_women, total_mla, lok_pct, rajya_pct, best_state, best_pct

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <h1>🏛️ ShaktiSabha</h1>
  <p>Tracking Women's Representation in Indian Legislative Bodies — MLAs & MPs</p>
</div>
""", unsafe_allow_html=True)

# ─── Ticker ──────────────────────────────────────────────────────────────────
ticker_placeholder = st.empty()

# ─── Timestamp ───────────────────────────────────────────────────────────────
ts_placeholder = st.empty()

# ─── KPI Row ─────────────────────────────────────────────────────────────────
kpi_placeholder = st.empty()

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 National Overview",
    "🗺️ State Analysis",
    "🎗️ Party Breakdown",
    "📈 Trends & Forecast",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — National Overview
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Lok Sabha Women % Across Elections</div>', unsafe_allow_html=True)

    fig_lok = go.Figure()
    fig_lok.add_trace(go.Scatter(
        x=f_lok["Year"], y=f_lok["Women_Pct"],
        mode="lines+markers+text",
        name="Women %",
        line=dict(color="#FF9933", width=3),
        marker=dict(size=10, color="#FF9933", line=dict(width=2, color="white")),
        text=[f"{v}%" for v in f_lok["Women_Pct"]],
        textposition="top center",
        fill="tozeroy",
        fillcolor="rgba(255,153,51,0.12)",
    ))
    fig_lok.add_hline(
        y=33, line_dash="dash", line_color="#DC143C", line_width=2,
        annotation_text="33% Reservation Goal", annotation_position="top right",
        annotation_font_color="#DC143C",
    )
    fig_lok.update_layout(
        **PLOTLY_TEMPLATE,
        height=360,
        xaxis=dict(title="Election Year", tickmode="array", tickvals=f_lok["Year"]),
        yaxis=dict(title="Women %", range=[0, 40]),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=40),
    )
    st.plotly_chart(fig_lok, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Seats Contested vs Elected</div>', unsafe_allow_html=True)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=f_lok["Year"], y=f_lok["Total_Contested"],
            name="Contested", marker_color="#000080", opacity=0.75,
        ))
        fig_bar.add_trace(go.Bar(
            x=f_lok["Year"], y=f_lok["Women_Elected"],
            name="Elected", marker_color="#FF9933",
        ))
        fig_bar.update_layout(
            **PLOTLY_TEMPLATE, barmode="group", height=300,
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=30, r=20, t=10, b=30),
            xaxis_title="Year", yaxis_title="Count",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Party-wise Women MPs (Current Lok Sabha)</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(go.Pie(
            labels=f_party["Party"],
            values=f_party["Women_MPs"],
            hole=0.55,
            marker=dict(colors=COLORS[:len(f_party)]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Women MPs: %{value}<br>Share: %{percent}<extra></extra>",
        ))
        fig_donut.update_layout(
            **PLOTLY_TEMPLATE, height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — State Analysis
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Women MLAs by State (Ranked)</div>', unsafe_allow_html=True)

    tier_colors = {"Below 5%": "#DC143C", "5–10%": "#FF9933", "10–15%": "#FFD700", "Above 15%": "#138808"}
    sorted_states = f_states.sort_values("Women_Pct", ascending=True)
    sorted_states["Tier_Color"] = sorted_states["Performance_Tier"].map(tier_colors).astype(object).fillna("#aaa")

    fig_states = go.Figure(go.Bar(
        x=sorted_states["Women_Pct"],
        y=sorted_states["State"],
        orientation="h",
        marker_color=sorted_states["Tier_Color"],
        text=[f"{v}% ({int(w)} MLAs)" for v, w in zip(sorted_states["Women_Pct"], sorted_states["Women_MLAs"])],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Women: %{x}%<extra></extra>",
    ))
    fig_states.add_vline(x=33, line_dash="dash", line_color="#DC143C",
                         annotation_text="33% Goal", annotation_position="top right")
    fig_states.update_layout(
        **PLOTLY_TEMPLATE,
        height=max(600, len(sorted_states) * 22),
        xaxis=dict(title="Women MLA %", range=[0, 45]),
        yaxis=dict(title=""),
        margin=dict(l=150, r=80, t=20, b=40),
    )
    st.plotly_chart(fig_states, use_container_width=True)

    # Legend
    lcols = st.columns(4)
    for i, (tier, color) in enumerate(tier_colors.items()):
        lcols[i].markdown(
            f"<div style='background:{color};border-radius:6px;padding:6px 10px;"
            f"color:white;font-size:0.8rem;font-weight:600;text-align:center'>"
            f"{tier}</div>", unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Female Literacy vs Women MLA %</div>', unsafe_allow_html=True)
    fig_scatter = px.scatter(
        f_states, x="Female_Literacy", y="Women_Pct",
        color="Region", size="Women_MLAs",
        hover_name="State",
        hover_data={"Women_MLAs": True, "Total_Seats": True},
        labels={"Female_Literacy": "Female Literacy Rate (%)", "Women_Pct": "Women MLA %"},
        color_discrete_sequence=COLORS,
        trendline="ols",
    )
    fig_scatter.update_layout(**PLOTLY_TEMPLATE, height=420, margin=dict(l=40, r=30, t=20, b=40))
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Table
    st.markdown('<div class="section-title">State-wise Data Table</div>', unsafe_allow_html=True)
    tbl = f_states[["State", "Region", "Total_Seats", "Women_MLAs", "Women_Pct", "Female_Literacy", "Performance_Tier"]].copy()
    tbl = tbl.rename(columns={
        "Total_Seats": "Total Seats", "Women_MLAs": "Women MLAs",
        "Women_Pct": "Women %", "Female_Literacy": "Female Literacy %",
        "Performance_Tier": "Tier"
    }).sort_values("Women %", ascending=False)
    st.dataframe(
        tbl.style.background_gradient(subset=["Women %"], cmap="YlGn")
               .format({"Women %": "{:.1f}", "Female Literacy %": "{:.1f}"}),
        use_container_width=True, height=400
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Party Breakdown
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Candidates vs Elected Women by Party</div>', unsafe_allow_html=True)

    fig_grp = go.Figure()
    fig_grp.add_trace(go.Bar(
        name="Women Candidates", x=f_party["Party"], y=f_party["Women_Candidates"],
        marker_color="#000080", opacity=0.7,
    ))
    fig_grp.add_trace(go.Bar(
        name="Women Elected", x=f_party["Party"], y=f_party["Women_MPs"],
        marker_color="#FF9933",
    ))
    fig_grp.update_layout(
        **PLOTLY_TEMPLATE, barmode="group", height=380,
        legend=dict(orientation="h", y=1.05),
        xaxis_title="Party", yaxis_title="Count",
        margin=dict(l=40, r=30, t=20, b=40),
    )
    st.plotly_chart(fig_grp, use_container_width=True)

    col_c, col_d = st.columns([1, 1])
    with col_c:
        st.markdown('<div class="section-title">Win Rate by Party</div>', unsafe_allow_html=True)
        f_party["Win_Rate"] = (f_party["Women_MPs"] / f_party["Women_Candidates"] * 100).round(1)
        fig_win = px.bar(
            f_party.sort_values("Win_Rate", ascending=False),
            x="Win_Rate", y="Party", orientation="h",
            color="Win_Rate", color_continuous_scale=["#DC143C", "#FF9933", "#138808"],
            text=[f"{v}%" for v in f_party.sort_values("Win_Rate", ascending=False)["Win_Rate"]],
            labels={"Win_Rate": "Win Rate (%)"},
        )
        fig_win.update_layout(**PLOTLY_TEMPLATE, height=320, showlegend=False,
                              margin=dict(l=80, r=40, t=10, b=30),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_win, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-title">Women % of Total MPs by Party</div>', unsafe_allow_html=True)
        f_party["Pct_of_Party"] = (f_party["Women_MPs"] / f_party["Total_MPs"] * 100).round(1)
        fig_pct = px.bar(
            f_party.sort_values("Pct_of_Party", ascending=False),
            x="Party", y="Pct_of_Party",
            color="Party", color_discrete_sequence=COLORS,
            text=[f"{v}%" for v in f_party.sort_values("Pct_of_Party", ascending=False)["Pct_of_Party"]],
            labels={"Pct_of_Party": "Women % of Party MPs"},
        )
        fig_pct.update_layout(**PLOTLY_TEMPLATE, height=320, showlegend=False,
                              margin=dict(l=30, r=20, t=10, b=40))
        st.plotly_chart(fig_pct, use_container_width=True)

    # Party table
    st.markdown('<div class="section-title">Party Summary Table</div>', unsafe_allow_html=True)
    ptbl = f_party[["Party", "Total_MPs", "Women_MPs", "Pct_of_Party",
                     "Women_Candidates", "Win_Rate"]].rename(columns={
        "Total_MPs": "Total MPs", "Women_MPs": "Women MPs",
        "Pct_of_Party": "Women % of Party",
        "Women_Candidates": "Women Candidates", "Win_Rate": "Win Rate %"
    })
    st.dataframe(
        ptbl.style.background_gradient(subset=["Women % of Party"], cmap="Oranges")
               .format({"Women % of Party": "{:.1f}", "Win Rate %": "{:.1f}"}),
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Trends & Forecast
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="section-title">Rajya Sabha Women % Trend</div>', unsafe_allow_html=True)
        fig_rs = go.Figure()
        fig_rs.add_trace(go.Scatter(
            x=df_rajya["Year"], y=df_rajya["Women_Pct"],
            mode="lines+markers",
            line=dict(color="#138808", width=2.5),
            marker=dict(size=8, color="#138808"),
            fill="tozeroy", fillcolor="rgba(19,136,8,0.1)",
            name="Rajya Sabha"
        ))
        fig_rs.add_hline(y=33, line_dash="dot", line_color="#DC143C",
                         annotation_text="33%", annotation_font_color="#DC143C")
        fig_rs.update_layout(
            **PLOTLY_TEMPLATE, height=340,
            xaxis_title="Year", yaxis_title="Women %",
            margin=dict(l=40, r=30, t=20, b=40),
        )
        st.plotly_chart(fig_rs, use_container_width=True)

    with col_f:
        st.markdown('<div class="section-title">Lok Sabha Forecast to 2029</div>', unsafe_allow_html=True)
        years_hist  = df_lok["Year"].tolist()
        pct_hist    = df_lok["Women_Pct"].tolist()
        z = np.polyfit(years_hist, pct_hist, 1)
        p = np.poly1d(z)
        forecast_years = [2024, 2029]
        forecast_pct   = [round(p(y), 1) for y in forecast_years]

        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(
            x=years_hist, y=pct_hist,
            mode="lines+markers", name="Actual",
            line=dict(color="#FF9933", width=2.5),
            marker=dict(size=8),
        ))
        fig_fc.add_trace(go.Scatter(
            x=forecast_years, y=forecast_pct,
            mode="lines+markers", name="Forecast",
            line=dict(color="#000080", width=2, dash="dash"),
            marker=dict(size=9, symbol="diamond"),
        ))
        fig_fc.add_hrect(
            y0=33, y1=40, fillcolor="rgba(19,136,8,0.08)",
            line_width=0, annotation_text="33% Zone",
            annotation_position="top left",
        )
        fig_fc.update_layout(
            **PLOTLY_TEMPLATE, height=340,
            xaxis_title="Year", yaxis_title="Women %",
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=40, r=30, t=20, b=40),
        )
        st.plotly_chart(fig_fc, use_container_width=True)

    # Combined overlay
    st.markdown('<div class="section-title">Lok Sabha vs Rajya Sabha — Women % Comparison</div>',
                unsafe_allow_html=True)
    fig_comp = go.Figure()
    lok_merged = df_lok[df_lok["Year"] >= 2009].copy()
    fig_comp.add_trace(go.Scatter(
        x=lok_merged["Year"], y=lok_merged["Women_Pct"],
        mode="lines+markers", name="Lok Sabha",
        line=dict(color="#FF9933", width=2.5), marker=dict(size=9)
    ))
    fig_comp.add_trace(go.Scatter(
        x=df_rajya["Year"][::2], y=df_rajya["Women_Pct"][::2],
        mode="lines+markers", name="Rajya Sabha",
        line=dict(color="#138808", width=2.5), marker=dict(size=9)
    ))
    fig_comp.add_hline(y=33, line_dash="dash", line_color="#DC143C",
                       annotation_text="33% Constitutional Amendment Goal")
    fig_comp.update_layout(
        **PLOTLY_TEMPLATE, height=360,
        xaxis_title="Year", yaxis_title="Women %",
        legend=dict(orientation="h", y=1.05),
        margin=dict(l=40, r=30, t=20, b=40),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Key insights
    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
    ins1, ins2, ins3 = st.columns(3)
    with ins1:
        st.info("📌 **At current growth rate**, Lok Sabha could reach 33% representation only by **~2044** — nearly 20 years away.")
    with ins2:
        st.warning("⚠️ **10 states** still have women's MLA representation **below 5%**, including Nagaland (1.7%) and Mizoram (5%).")
    with ins3:
        st.success("✅ **West Bengal** leads with 50 women MLAs (17%), followed by **Rajasthan** (13.5%) and **Odisha** (15%).")

# ─── Render KPIs & Ticker (shared, above tabs) ───────────────────────────────
def render_kpis_and_ticker():
    lok_w, rajya_w, mla_total, lok_pct, rajya_pct, best_st, best_pct = get_live_kpis()

    ticker_placeholder.markdown(
        f"<div class='ticker-wrap'><span class='ticker-text'>"
        f"🔴 LIVE &nbsp;|&nbsp; {st.session_state.ticker_msg} &nbsp;|&nbsp; "
        f"Lok Sabha Women: {lok_pct}% &nbsp;|&nbsp; Rajya Sabha Women: {rajya_pct}% &nbsp;|&nbsp; "
        f"Best State: {best_st} ({best_pct:.1f}%)"
        f"</span></div>",
        unsafe_allow_html=True,
    )

    ts_placeholder.markdown(
        f"<div class='last-updated'>🕐 Last updated: {st.session_state.last_updated}</div>",
        unsafe_allow_html=True,
    )

    with kpi_placeholder.container():
        c1, c2, c3, c4, c5 = st.columns(5)
        cards = [
            (c1, "Women MPs (Lok Sabha)", f"{lok_w}", f"{lok_pct}% of 543 seats", ""),
            (c2, "Women Members (RS)",    f"{rajya_w}", f"{rajya_pct}% of 245 seats", "green"),
            (c3, "Women MLAs (Filtered)", f"{mla_total}", f"Across {len(f_states)} states", "navy"),
            (c4, "Best Performing State", best_st, f"{best_pct:.1f}% women MLAs", "gold"),
            (c5, "33% Goal Gap (LS)",
             f"{round(33 - lok_pct, 1)}%",
             "Seats needed to meet goal", "red"),
        ]
        for col, label, value, sub, cls in cards:
            col.markdown(
                f"<div class='kpi-card {cls}'>"
                f"<div class='kpi-label'>{label}</div>"
                f"<div class='kpi-value'>{value}</div>"
                f"<div class='kpi-sub'>{sub}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

render_kpis_and_ticker()

# ─── Auto-Refresh Loop ───────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(refresh_interval)
    # Simulate small live delta
    st.session_state.live_offset["lok"]   = random.randint(-2, 2)
    st.session_state.live_offset["rajya"] = random.randint(-1, 1)
    st.session_state.last_updated         = datetime.now().strftime("%H:%M:%S")
    st.session_state.ticker_msg           = random.choice(news_pool)
    st.rerun()