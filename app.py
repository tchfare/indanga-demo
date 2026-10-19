"""INDANGA: early warning for every child.
Streamlit demo for the UNICEF Rwanda @40 Pan-African Student Competition pitch.
All data is simulated. Run:  streamlit run app.py
"""
import base64
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="INDANGA | Early warning for every child", page_icon="🌍", layout="wide")
HERE = Path(__file__).parent

# ------------------------------------------------------------------ palette (UNICEF brand colours)
CYAN, DARKBLUE, INK, GREY = "#1CABE2", "#374EA2", "#1F2937", "#5B6472"
YELLOW, ORANGE, GREEN, RED, PURPLE = "#FFC20E", "#F26A21", "#00833D", "#E2231A", "#6A1E74"
NEED = {"Learning": CYAN, "Nutrition": YELLOW, "Health": RED, "Protection": PURPLE}
LVL = {"High": RED, "Medium": ORANGE, "Low": GREEN}


def b64(path):
    return base64.b64encode((HERE / path).read_bytes()).decode()


PHOTO = b64("assets/unicef_photo.jpg")
PHOTO_DUO = b64("assets/unicef_photo_duotone.jpg")
KIDS = b64("assets/kids_strip.svg")
LOGO = "".join(f'<span style="color:{c}">{ch}</span>' for ch, c in
               zip("INDANGA", [CYAN, YELLOW, GREEN, ORANGE, DARKBLUE, RED, CYAN]))

# ------------------------------------------------------------------ page style
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&family=Noto+Sans:wght@400;500;600;700;800&display=swap');
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"], .stDeployButton {{display:none !important;}}
.stApp {{background:#FFFFFF;}}
html, body, .stApp, .stMarkdown, p, li, label, input, textarea, button {{font-family:'Noto Sans', system-ui, sans-serif; color:{INK};}}
.block-container {{padding-top:0 !important; padding-bottom:0 !important; max-width:1320px;}}
h1, h2, h3 {{font-family:'Noto Sans', sans-serif !important; color:{INK} !important; font-weight:800 !important; letter-spacing:-.3px;}}
p, li {{font-size:17px; line-height:1.55;}}

/* navbar */
.nav {{display:flex; align-items:center; justify-content:space-between; padding:18px 4px 16px; border-bottom:1px solid #E5E7EB;}}
.brand {{display:flex; align-items:center; gap:14px;}}
.brand .logo {{font-family:'Fredoka', sans-serif; font-weight:700; font-size:34px; letter-spacing:2px; line-height:1;}}
.brand .tag {{font-size:14px; color:{GREY}; font-weight:600; border-left:2px solid #E5E7EB; padding-left:14px; line-height:1.3;}}
.navlinks {{display:flex; gap:26px; font-weight:700; font-size:15px; color:{GREY};}}
.pill {{background:#FFF7DB; color:#7A5A00; border:1px solid {YELLOW}; font-weight:800; font-size:13px; border-radius:999px; padding:7px 14px; white-space:nowrap;}}

/* hero */
.hero {{display:grid; grid-template-columns:1.05fr .95fr; gap:44px; align-items:center; padding:40px 4px 34px;}}
.eyebrow {{color:{CYAN}; font-weight:800; font-size:14px; letter-spacing:2px; text-transform:uppercase;}}
.hero h1 {{font-size:50px !important; line-height:1.08 !important; margin:10px 0 16px !important;}}
.hero h1 em {{font-style:normal; color:{CYAN};}}
.hero p.lead {{font-size:19px; color:#374151; margin:0 0 22px;}}
.steps {{display:flex; gap:10px; flex-wrap:wrap;}}
.step {{display:flex; align-items:center; gap:8px; background:#F3FAFE; border:1px solid #CDEBF8; border-radius:999px; padding:8px 14px; font-weight:700; font-size:15px;}}
.step b {{display:inline-flex; width:24px; height:24px; border-radius:50%; background:{CYAN}; color:#fff; align-items:center; justify-content:center; font-size:13px;}}
.photo {{position:relative;}}
.photo img {{width:100%; height:390px; object-fit:cover; object-position:50% 38%; border-radius:24px; display:block;}}
.photo .credit {{position:absolute; right:12px; top:12px; background:rgba(0,0,0,.55); color:#fff; font-size:12px; padding:3px 9px; border-radius:6px;}}
.photo .float {{position:absolute; left:16px; bottom:16px; background:#fff; border-radius:16px; padding:12px 16px; box-shadow:0 10px 30px rgba(31,41,55,.16); font-weight:700; font-size:15px; display:flex; gap:10px; align-items:center;}}
.photo .float .dot {{width:12px; height:12px; border-radius:50%; background:{GREEN};}}

/* duotone banner hero */
.banner {{position:relative; margin:22px 0 30px; height:540px; border-radius:30px; overflow:hidden; background:#0A3E5F;}}
.banner .bg {{position:absolute; right:0; top:0; width:68%; height:100%; object-fit:cover; object-position:58% 32%;}}
.banner .fade {{position:absolute; inset:0; background:linear-gradient(90deg,#0A3E5F 0%,#0A3E5F 34%,rgba(10,62,95,.78) 48%,rgba(10,62,95,.10) 70%,rgba(10,62,95,0) 100%);}}
.banner svg.d {{position:absolute; pointer-events:none; z-index:1;}}
.banner .tl {{left:-30px; top:-30px; width:130px; height:130px;}}
.banner .tr {{right:-8px; top:-8px; width:170px; height:170px;}}
.banner .br {{right:0; bottom:0; width:280px; height:180px;}}
.banner .x {{left:57%; bottom:22px; width:110px; height:76px;}}
.banner .txt {{position:absolute; left:56px; top:70px; width:min(560px, 52%); color:#fff; z-index:2;}}
.banner .eb {{color:{YELLOW}; font-weight:800; font-size:14px; letter-spacing:2.4px; text-transform:uppercase;}}
.banner h1 {{font-family:'Fredoka', sans-serif !important; font-weight:700 !important; font-size:64px !important; line-height:.98 !important; color:#fff !important; margin:12px 0 14px !important; letter-spacing:.5px;}}
.banner h1 .ol {{color:transparent; -webkit-text-stroke:2.5px #fff;}}
.banner .sub {{font-weight:800; font-size:21px; letter-spacing:1.2px; margin-bottom:10px; color:#fff;}}
.banner p {{color:#D8EEF8 !important; font-size:16.5px; line-height:1.5; margin:0 0 18px;}}
.banner .chips {{display:flex; flex-wrap:wrap; gap:8px;}}
.banner .chips span {{display:inline-flex; align-items:center; gap:8px; color:#fff; font-weight:700; font-size:14.5px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.35); border-radius:999px; padding:7px 13px;}}
.banner .chips b {{display:inline-flex; width:22px; height:22px; border-radius:50%; background:{YELLOW}; color:#0A3E5F; align-items:center; justify-content:center; font-size:12.5px;}}
.banner .credit {{position:absolute; right:16px; top:14px; z-index:2; background:rgba(0,0,0,.45); color:#fff; font-size:11.5px; padding:3px 9px; border-radius:6px;}}
.banner .float {{position:absolute; right:28px; bottom:26px; z-index:2; background:#fff; color:{INK}; border-radius:14px; padding:11px 15px; box-shadow:0 10px 26px rgba(0,0,0,.25); font-weight:700; font-size:14.5px; display:flex; gap:9px; align-items:center;}}
.banner .float .dot {{width:11px; height:11px; border-radius:50%; background:{GREEN};}}

/* small laptops and tablets */
@media (min-width: 761px) and (max-width: 1180px) {{
  .banner {{height:auto; min-height:540px;}}
  .banner .txt {{position:relative; left:0; top:0; width:min(540px, 60%); padding:64px 0 96px 44px;}}
  .banner h1 {{font-size:50px !important;}}
  .banner .x {{display:none;}}
}}

/* phones and small screens */
@media (max-width: 760px) {{
  .nav {{padding:12px 2px;}}
  .brand .logo {{font-size:28px;}}
  .brand .tag {{display:none;}}
  .pill {{font-size:11px; padding:5px 10px;}}
  .banner {{height:auto; min-height:560px; border-radius:22px; margin:14px 0 22px;}}
  .banner .bg {{width:100%; height:300px; object-position:55% 30%;}}
  .banner .fade {{background:linear-gradient(180deg, rgba(10,62,95,0) 0px, rgba(10,62,95,0) 180px, #0A3E5F 300px, #0A3E5F 100%);}}
  .banner .txt {{position:relative; left:0; top:0; width:100%; padding:268px 20px 76px;}}
  .banner h1 {{font-size:40px !important;}}
  .banner .sub {{font-size:18px;}}
  .banner p {{font-size:15px;}}
  .banner .x, .banner .br {{display:none;}}
  .banner .float {{left:20px; right:auto; bottom:18px; font-size:13px;}}
  .hero h1, .section-title {{font-size:22px;}}
  .kpi .n {{font-size:32px;}}
  .phone {{width:280px;}}
}}

/* section + cards */
.section-title {{font-size:26px; font-weight:800; margin:6px 0 4px;}}
.section-sub {{color:{GREY}; font-size:16px; margin-bottom:14px;}}
.kpi {{background:#fff; border:1px solid #E5E7EB; border-radius:18px; padding:18px 20px; height:100%;}}
.kpi .n {{font-size:40px; font-weight:800; line-height:1.05;}}
.kpi .l {{color:{GREY}; font-weight:600; font-size:15px; margin-top:4px;}}
.kpi .bar {{height:5px; border-radius:4px; margin-bottom:12px; width:44px;}}
[data-testid="stVerticalBlockBorderWrapper"] {{border-radius:18px !important; border-color:#E5E7EB !important;}}
.note {{color:{GREY}; font-size:14px;}}
.chip {{display:inline-block; border-radius:999px; padding:3px 11px; font-size:13px; font-weight:800; color:#fff; margin:0 6px 0 0;}}
.reason {{display:flex; align-items:center; gap:8px; padding:7px 0; border-bottom:1px solid #F1F2F4; font-size:16px;}}

/* tabs */
.stTabs [data-baseweb="tab-list"] {{gap:6px; border-bottom:1px solid #E5E7EB;}}
.stTabs [data-baseweb="tab"] {{padding:12px 20px;}}
.stTabs [data-baseweb="tab"] p {{font-size:18px !important; font-weight:700 !important; color:{GREY};}}
.stTabs [aria-selected="true"] p {{color:{CYAN} !important;}}
.stTabs [aria-selected="true"] {{color:{CYAN} !important;}}
.stTabs [data-baseweb="tab-highlight"] {{background:{CYAN} !important; height:3px;}}

/* buttons */
[data-testid="stColumn"]:last-child .stButton {{max-width:300px; margin:0 auto;}}
.stButton > button {{border-radius:12px; font-weight:700; font-size:15px; padding:10px 14px; border:1px solid #D1D5DB;}}
.stButton > button:hover {{border-color:{CYAN}; color:{CYAN};}}

/* realistic smartphone */
.phone {{width:300px; margin:0 auto; background:#0B0F14; border-radius:48px; padding:11px; box-shadow:0 24px 50px rgba(15,23,42,.28), inset 0 0 0 2px #2B313A;}}
.screen {{position:relative; background:#fff; border-radius:38px; overflow:hidden; height:590px; display:flex; flex-direction:column;}}
.island {{position:absolute; top:10px; left:50%; transform:translateX(-50%); width:96px; height:28px; background:#0B0F14; border-radius:20px; z-index:3;}}
.status {{display:flex; justify-content:space-between; align-items:center; padding:14px 26px 6px; font-size:14px; font-weight:700; color:#111;}}
.status .icons {{display:flex; gap:6px; align-items:center;}}
.apphead {{display:flex; flex-direction:column; align-items:center; padding:8px 0 10px; border-bottom:1px solid #ECECEF; background:#F9F9FB;}}
.avatar {{width:46px; height:46px; border-radius:50%; background:{CYAN}; color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; font-size:16px;}}
.apphead .who {{font-size:13px; font-weight:700; margin-top:4px; color:#111;}}
.apphead .sub {{font-size:11px; color:#8E8E93;}}
.thread {{flex:1; padding:12px 12px; background:#fff; overflow:hidden;}}
.daystamp {{text-align:center; font-size:11px; color:#8E8E93; margin:2px 0 10px; font-weight:600;}}
.bin {{background:#E9E9EB; color:#111; border-radius:18px 18px 18px 6px; padding:9px 12px; font-size:13.5px; line-height:1.42; max-width:88%; margin-bottom:8px;}}
.bout {{background:#0A84FF; color:#fff; border-radius:18px 18px 6px 18px; padding:8px 13px; font-size:13.5px; margin:0 0 3px auto; width:fit-content; max-width:80%;}}
.delivered {{text-align:right; font-size:10.5px; color:#8E8E93; margin-bottom:8px;}}
.inputbar {{display:flex; align-items:center; gap:8px; padding:8px 12px 18px; border-top:1px solid #ECECEF;}}
.inputbar .field {{flex:1; border:1px solid #D1D1D6; border-radius:18px; padding:6px 12px; font-size:13px; color:#B0B0B5;}}
.inputbar .send {{width:28px; height:28px; border-radius:50%; background:#0A84FF; display:flex; align-items:center; justify-content:center;}}
.homebar {{width:110px; height:4px; background:#111; border-radius:4px; margin:0 auto 8px;}}

/* footer */
.footer {{margin-top:40px; border-top:1px solid #E5E7EB;}}
.footer img {{width:100%; display:block;}}
.footer .txt {{background:#E8F6FC; text-align:center; color:#334155; font-size:13.5px; padding:6px 10px 18px;}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------ transparent risk model
W = dict(intercept=-2.4, day=0.15, rep=0.8, growth=[0.0, 0.8, 1.6], dose=0.8, poor=0.7, dis=0.6)
FLAG = 0.9
ACTION = {"Learning": ("Teacher", "remedial class and home contact"),
          "Nutrition": ("Community health worker", "nutrition check and referral"),
          "Health": ("Community health worker", "catch up vaccination"),
          "Protection": ("Social worker", "household support visit")}


def contributions(days, rep, growth, doses, poor, dis):
    return {"Learning": W["day"] * days + (W["rep"] if rep else 0),
            "Nutrition": W["growth"][growth],
            "Health": W["dose"] * doses,
            "Protection": (W["poor"] if poor else 0) + (W["dis"] if dis else 0)}


def risk(k):
    return 1 / (1 + np.exp(-(W["intercept"] + sum(k.values()))))


def level(p):
    return "High" if p >= 0.6 else "Medium" if p >= 0.3 else "Low"


def reasons(c):
    r = []
    if c["days"] >= 6: r.append(("Learning", f"missed {c['days']} school days this month"))
    if c["rep"]: r.append(("Learning", "repeated a grade"))
    if c["growth"] == 2: r.append(("Nutrition", "growth faltering (low weight for age)"))
    elif c["growth"] == 1: r.append(("Nutrition", "growth slowing, at risk"))
    if c["doses"]: r.append(("Health", f"{c['doses']} vaccine dose{'s' if c['doses'] > 1 else ''} missed"))
    if c["poor"]: r.append(("Protection", "household in Ubudehe category D or E (most vulnerable)"))
    if c["dis"]: r.append(("Protection", "child with a disability"))
    return r


@st.cache_data
def simulate(n=1240, seed=20261030):
    rng = np.random.default_rng(seed)
    sectors = [f"Sector {i}" for i in range(1, 7)]
    s_risk = np.array([0.0, 0.35, 0.15, 0.55, 0.05, 0.25])
    s = rng.integers(0, 6, n)
    age = rng.integers(0, 14, n)                      # 0 to 13 years
    u5 = age < 5
    poor = rng.random(n) < 0.18 + s_risk[s] * 0.45
    base = poor.astype(float) + s_risk[s]
    girl = rng.random(n) < 0.5
    dis = rng.random(n) < np.where(poor, 0.08, 0.04)
    spike = rng.random(n) < 0.13
    # learning signals only for school age (5+); growth and vaccination signals only for under fives
    days = np.clip(np.round(rng.random(n) * 4 + base * rng.random(n) * 6 + spike * (6 + rng.random(n) * 8)), 0, 20).astype(int) * ~u5
    rep = (rng.random(n) < 0.14 + base * 0.12) & ~u5 & (age >= 7)
    g = rng.random(n)
    growth = np.where(g < 0.12 + base * 0.12, 2, np.where(g < 0.30 + base * 0.14, 1, 0)) * u5
    doses = np.where(rng.random(n) < 0.16 + base * 0.12, np.where(rng.random(n) < 0.35, 2, 1), 0) * u5
    df = pd.DataFrame(dict(id=[f"RW-{4000 + (i * 7) % 5000:04d}{chr(65 + i % 26)}" for i in range(n)],
                           age=age, sector=[sectors[i] for i in s], girl=girl, dis=dis,
                           poor=poor, days=days, rep=rep, growth=growth, doses=doses))
    k = df.apply(lambda r: contributions(r.days, r.rep, r.growth, r.doses, r.poor, r.dis), axis=1)
    df["p"] = [risk(x) for x in k]
    df["level"] = df.p.map(level)
    df["main"] = [max(x, key=x.get) for x in k]
    df["n_needs"] = [sum(v >= FLAG for v in x.values()) for x in k]
    df["age_group"] = np.where(df.age < 5, "Under 5", "5 to 13")
    return df


@st.cache_data
def under5_trend(share_now, n_u5, seed=7):
    """Simulated monthly monitoring of the share of under fives flagged (illustration only)."""
    rng = np.random.default_rng(seed)
    months = pd.date_range("2025-11-01", "2026-10-01", freq="MS")
    season = 0.025 * np.sin((np.asarray(months.month) - 3) / 12 * 2 * np.pi)      # lean season bump
    share = np.clip(share_now + season - season[-1] + rng.normal(0, 0.008, len(months)), 0, 1).astype(float)
    share[-1] = share_now
    return pd.DataFrame({"month": months, "share": share, "n": n_u5})


AGE_OPTS = ["All children (0 to 13)", "Under 5", "5 to 13"]


def by_age(d, choice):
    return d if choice == AGE_OPTS[0] else d[d.age_group == choice]


def style(chart, h):
    return (chart.properties(height=h)
            .configure_view(strokeWidth=0)
            .configure_axis(labelFontSize=14, titleFontSize=13, labelColor=INK, titleColor=GREY, gridColor="#EEF0F3", domain=False, labelFont="Noto Sans", titleFont="Noto Sans")
            .configure_legend(labelFontSize=14, labelFont="Noto Sans", orient="bottom", title=None))


df = simulate()
st.session_state.setdefault("status", {})

# ------------------------------------------------------------------ navbar + hero
st.markdown(f"""
<div class="nav">
  <div class="brand"><div class="logo">{LOGO}</div><div class="tag">Early warning<br>for every child</div></div>
  <div class="pill">Student prototype &middot; simulated data</div>
</div>
<div class="banner">
  <img class="bg" src="data:image/jpeg;base64,{PHOTO_DUO}" alt="Two smiling children in a Rwandan classroom">
  <div class="fade"></div>
  <svg class="d tl" viewBox="0 0 130 130"><circle cx="38" cy="38" r="30" fill="{ORANGE}"/><circle cx="38" cy="38" r="52" fill="none" stroke="{ORANGE}" stroke-width="11" stroke-dasharray="190 400" transform="rotate(10 38 38)"/></svg>
  <svg class="d tr" viewBox="0 0 170 170"><path d="M40,0 C50,40 100,30 96,70 C92,110 150,100 160,140" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round"/><path d="M66,0 C76,34 122,26 120,62" fill="none" stroke="{YELLOW}" stroke-width="5" stroke-linecap="round"/></svg>
  <svg class="d br" viewBox="0 0 280 180"><g fill="none" stroke="{YELLOW}" stroke-width="18" stroke-linecap="round"><path d="M40,180 A160,160 0 0 1 280,30"/><path d="M100,180 A100,100 0 0 1 280,92"/></g></svg>
  <svg class="d x" viewBox="0 0 130 90"><g stroke="{ORANGE}" stroke-width="8" stroke-linecap="round"><path d="M10,10 l16,16 M26,10 l-16,16"/><path d="M58,30 l16,16 M74,30 l-16,16"/><path d="M14,58 l16,16 M30,58 l-16,16"/><path d="M98,56 l13,13 M111,56 l-13,13"/></g></svg>
  <div class="txt">
    <div class="eb">Kuri buri mwana &middot; for every child</div>
    <h1>Find every child<br>before risk<br>becomes <span class="ol">harm.</span></h1>
    <div class="sub">Early warning, together.</div>
    <p>INDANGA links the school, health, immunisation and social protection data Rwanda already collects, and tells frontline workers which child to visit, why, and which service to call.</p>
    <div class="chips"><span><b>1</b>Link</span><span><b>2</b>Score</span><span><b>3</b>Explain</span><span><b>4</b>Act with a human</span></div>
  </div>
  <span class="credit">&copy; UNICEF/UNI725007/Iyakaremye</span>
  <div class="float"><span class="dot"></span>Every alert is reviewed by a person</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["District overview", "Children to visit", "Child profile and what if"])

# ------------------------------------------------------------------ 1. overview
with tab1:
    st.markdown('<div class="section-title">Pilot district at a glance</div><div class="section-sub">One district, six sectors, updated every month from existing records.</div>', unsafe_allow_html=True)
    age_choice = st.radio("Age group", AGE_OPTS, horizontal=True, key="age_overview")
    d = by_age(df, age_choice)
    flagged = d[d.level != "Low"]
    cols = st.columns(4)
    for col, val, lab, colr in [(cols[0], f"{len(d):,}", "children monitored", CYAN),
                                (cols[1], (d.level == "High").sum(), "high risk: visit this week", RED),
                                (cols[2], (d.level == "Medium").sum(), "medium risk: follow up this month", ORANGE),
                                (cols[3], (flagged.n_needs >= 2).sum(), "at risk in two or more needs", PURPLE)]:
        col.markdown(f'<div class="kpi"><div class="bar" style="background:{colr}"></div><div class="n">{val}</div><div class="l">{lab}</div></div>', unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1, st.container(border=True):
        st.markdown("#### Where risk is building up, by sector")
        sec = d.groupby(["sector", "level"]).size().rename("n").reset_index()
        sec["share"] = sec.n / sec.groupby("sector").n.transform("sum")
        sec["o"] = sec.level.map({"High": 0, "Medium": 1, "Low": 2})
        ch = alt.Chart(sec).mark_bar(cornerRadius=3, height=22).encode(
            y=alt.Y("sector:N", title=None, sort=sorted(df.sector.unique())),
            x=alt.X("share:Q", stack="normalize", axis=alt.Axis(format="%", title=None)),
            color=alt.Color("level:N", scale=alt.Scale(domain=["High", "Medium", "Low"], range=[RED, ORANGE, "#E5E7EB"])),
            order="o:Q", tooltip=["sector", "level", alt.Tooltip("share:Q", format=".0%")])
        st.altair_chart(style(ch, 300), width="stretch")
        st.markdown('<div class="note">District teams can send support where harm is concentrating.</div>', unsafe_allow_html=True)
    with c2, st.container(border=True):
        st.markdown("#### What drives the alerts")
        need = flagged.main.value_counts(normalize=True).reindex(list(NEED)).fillna(0).rename("share").reset_index()
        need.columns = ["need", "share"]
        st.altair_chart(style(alt.Chart(need).mark_bar(cornerRadius=3, height=22).encode(
            y=alt.Y("need:N", title=None, sort=list(NEED)), x=alt.X("share:Q", axis=alt.Axis(format="%", title=None)),
            color=alt.Color("need:N", scale=alt.Scale(domain=list(NEED), range=list(NEED.values())), legend=None),
            tooltip=["need", alt.Tooltip("share:Q", format=".0%")]), 170), width="stretch")
        st.markdown("#### Fairness check")
        groups = {"Girls": d.girl, "Boys": ~d.girl, "Disability": d.dis, "Ubudehe D/E": d.poor, "Ubudehe A to C": ~d.poor}
        fair = pd.DataFrame({"group": list(groups), "rate": [(d[m].level == "High").mean() if m.any() else 0 for m in groups.values()]})
        st.altair_chart(style(alt.Chart(fair).mark_bar(cornerRadius=3, height=18, color=DARKBLUE).encode(
            y=alt.Y("group:N", title=None, sort=list(groups)), x=alt.X("rate:Q", axis=alt.Axis(format="%", title="share at high risk")),
            tooltip=["group", alt.Tooltip("rate:Q", format=".0%")]), 180), width="stretch")
        st.markdown('<div class="note">Higher rates in Ubudehe D and E reflect real need. With real data, the check compares how well at risk children are caught in each group, so that no group is missed or over flagged.</div>', unsafe_allow_html=True)

    # ---- under five focus
    u5 = df[df.age_group == "Under 5"]
    u5_share = (u5.level != "Low").mean()
    st.write("")
    with st.container(border=True):
        st.markdown("#### Under fives: nutrition and immunisation watch")
        a, b = st.columns([1, 2.2], gap="large")
        with a:
            for val, lab, colr in [(f"{len(u5):,}", "under fives monitored", CYAN),
                                   (f"{u5_share:.0%}", "flagged this month (high or medium)", ORANGE),
                                   (f"{(u5.growth == 2).mean():.0%}", "with growth faltering", YELLOW),
                                   (f"{(u5.doses > 0).mean():.0%}", "with a missed vaccine dose", RED)]:
                st.markdown(f'<div class="kpi" style="margin-bottom:10px"><div class="bar" style="background:{colr}"></div><div class="n" style="font-size:30px">{val}</div><div class="l">{lab}</div></div>', unsafe_allow_html=True)
        with b:
            tr = under5_trend(round(float(u5_share), 3), len(u5))
            line = alt.Chart(tr).mark_line(point=alt.OverlayMarkDef(size=70, filled=True, color=CYAN), color=CYAN, strokeWidth=3).encode(
                x=alt.X("month:T", title=None, axis=alt.Axis(format="%b %Y", labelAngle=0, tickCount=6)),
                y=alt.Y("share:Q", title="share of under fives flagged", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 0.5])),
                tooltip=[alt.Tooltip("month:T", format="%B %Y"), alt.Tooltip("share:Q", format=".1%")])
            st.altair_chart(style(line, 300), width="stretch")
            st.markdown('<div class="note">Simulated monthly monitoring, shown to illustrate the dashboard, not a result. With real data this line would track the under five indicators behind Rwanda\'s stunting target (27% in 2025, NISR RDHS).</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ 2. list
with tab2:
    st.markdown('<div class="section-title">Children to visit</div><div class="section-sub">Highest risk first. Each alert comes with its reasons and a suggested action.</div>', unsafe_allow_html=True)
    f0, f1, f2, f3, f4 = st.columns(5)
    age_l = f0.selectbox("Age group", AGE_OPTS, key="age_list")
    sector = f1.selectbox("Sector", ["All sectors"] + sorted(df.sector.unique()))
    need = f2.selectbox("Main need", ["All needs"] + list(NEED))
    lv = f3.selectbox("Risk level", ["High and medium", "High only", "Everyone"])
    q = f4.text_input("Search child ID", placeholder="e.g. RW-5015P").strip().upper()
    view = by_age(df, age_l).copy()
    if sector != "All sectors": view = view[view.sector == sector]
    if need != "All needs": view = view[view.main == need]
    view = view[view.level == "High"] if lv == "High only" else view[view.level != "Low"] if lv == "High and medium" else view
    if q: view = view[view.id.str.contains(q)]
    view = view.sort_values("p", ascending=False)
    show = view.head(40).copy()
    show["Main reasons"] = show.apply(lambda r: "; ".join(t for _, t in reasons(r)[:3]), axis=1)
    show["Suggested action"] = show.main.map(lambda m: f"{ACTION[m][0]}: {ACTION[m][1]}")
    show["Status"] = show.id.map(lambda i: st.session_state.status.get(i, "To visit"))
    show["Level"] = show.level.map({"High": "🔴 High", "Medium": "🟠 Medium", "Low": "🟢 Low"})
    st.dataframe(show[["id", "age", "sector", "Level", "p", "Main reasons", "Suggested action", "Status"]]
                 .rename(columns={"id": "Child ID", "age": "Age", "sector": "Sector", "p": "Risk"}),
                 hide_index=True, width="stretch", height=560, row_height=44,
                 column_config={"Risk": st.column_config.ProgressColumn("Risk", min_value=0, max_value=1, format="percent")})
    st.markdown(f'<div class="note">{len(view)} children match. Showing the {len(show)} with the highest risk. Open a child in the next tab to see why.</div>', unsafe_allow_html=True)
    export = view.assign(
        risk_percent=(view.p * 100).round(1),
        main_reasons=view.apply(lambda r: "; ".join(t for _, t in reasons(r)), axis=1),
        suggested_action=view.main.map(lambda m: f"{ACTION[m][0]}: {ACTION[m][1]}"),
        status=view.id.map(lambda i: st.session_state.status.get(i, "To visit")),
    )[["id", "age", "age_group", "sector", "level", "risk_percent", "main", "main_reasons", "suggested_action", "status"]] \
        .rename(columns={"id": "child_id", "level": "risk_level", "main": "main_need"})
    st.download_button(f"⬇️  Download this list as CSV ({len(export)} children)", export.to_csv(index=False).encode("utf-8"),
                       file_name="INDANGA_priority_list_simulated.csv", mime="text/csv")

# ------------------------------------------------------------------ 3. child profile
with tab3:
    order = df.sort_values("p", ascending=False).id.tolist()
    top = st.columns([1, 2])
    cid = top[0].selectbox("Choose a child (highest risk first)", order, index=0)
    c = df.set_index("id").loc[cid]
    if st.session_state.get("loaded") != cid:
        st.session_state.update(loaded=cid, days=int(c.days), growth=int(c.growth), doses=int(c.doses),
                                rep=bool(c.rep), poor=bool(c.poor), dis=bool(c.dis))

    left, mid, right = st.columns([1.15, 1, 0.95], gap="large")
    with mid, st.container(border=True):
        st.markdown("#### What if? Try it live")
        young = c.age < 5
        st.markdown(f'<div class="note" style="margin-bottom:6px">{"Under five: nutrition and immunisation signals apply." if young else "School age: learning signals apply."}</div>', unsafe_allow_html=True)
        st.slider("School days missed this month", 0, 20, key="days", disabled=young)
        st.select_slider("Growth (weight for age)", options=[0, 1, 2], format_func=lambda v: ["normal", "at risk", "faltering"][v], key="growth", disabled=not young)
        st.slider("Vaccine doses missed", 0, 2, key="doses", disabled=not young)
        st.checkbox("Repeated a grade", key="rep", disabled=young)
        st.checkbox("Household in Ubudehe category D or E", key="poor")
        st.checkbox("Child with a disability", key="dis")
        if st.button("Reset to recorded data", width="stretch"):
            st.session_state.loaded = None
            st.rerun()
        st.markdown('<div class="note">Move a slider to show how a nutrition visit or a return to school lowers the risk straight away.</div>', unsafe_allow_html=True)

    cur = dict(days=st.session_state.days, rep=st.session_state.rep, growth=st.session_state.growth,
               doses=st.session_state.doses, poor=st.session_state.poor, dis=st.session_state.dis)
    k = contributions(**cur)
    p, rs = risk(k), reasons(cur)
    lvl, main = level(p), max(k, key=k.get)

    with left, st.container(border=True):
        st.markdown(f"#### Child {cid}")
        st.markdown(f'<div class="note" style="margin:-6px 0 6px">{"Girl" if c.girl else "Boy"}, {c.age} years &middot; {c.sector}</div>', unsafe_allow_html=True)
        ring = pd.DataFrame({"part": ["risk", "rest"], "v": [p, 1 - p]})
        donut = alt.Chart(ring).mark_arc(innerRadius=62, outerRadius=84, cornerRadius=6).encode(
            theta="v:Q", color=alt.Color("part:N", scale=alt.Scale(domain=["risk", "rest"], range=[LVL[lvl], "#EEF0F3"]), legend=None))
        txt = alt.Chart(pd.DataFrame({"t": [f"{p:.0%}"]})).mark_text(fontSize=32, fontWeight=800, color=INK, font="Noto Sans").encode(text="t:N")
        st.altair_chart((donut + txt).properties(width=200, height=190).configure_view(strokeWidth=0), width="stretch")
        st.markdown(f'<div style="text-align:center;font-weight:800;color:{LVL[lvl]};font-size:18px;margin:-6px 0 8px">{lvl} risk</div>', unsafe_allow_html=True)
        dims = pd.DataFrame({"need": list(k), "points": list(k.values())})
        st.altair_chart(style(alt.Chart(dims).mark_bar(cornerRadius=3, height=18).encode(
            y=alt.Y("need:N", title=None, sort=list(NEED)), x=alt.X("points:Q", title="risk points", scale=alt.Scale(domain=[0, 3.5])),
            color=alt.Color("need:N", scale=alt.Scale(domain=list(NEED), range=list(NEED.values())), legend=None)), 190), width="stretch")
        st.markdown("**Why this child was flagged**")
        st.markdown("".join(f'<div class="reason"><span class="chip" style="background:{NEED[d]}">{d}</span>{t}</div>' for d, t in rs)
                    or '<div class="reason">No warning signs recorded.</div>', unsafe_allow_html=True)
        st.markdown('<div class="note" style="margin-top:10px">Transparent model: every point of risk comes from a reason a frontline worker can check.</div>', unsafe_allow_html=True)

    with right:
        who, what = ACTION[main]
        two = " and ".join(t for _, t in rs[:2])
        if lvl == "Low":
            alert = f"INDANGA: child {cid} ({c.sector}) is now low risk. No visit needed this week. Thank you!"
        else:
            alert = (f"INDANGA alert for the {who.lower()}, {c.sector}.<br><br>Please visit child <b>{cid}</b> this "
                     f"{'week' if lvl == 'High' else 'month'}.<br>Why: {two}.<br>Suggested: {what}.<br><br>Reply 1 when done.")
        status = st.session_state.status.get(cid)
        reply = {"Visited": ("1", "Thank you. Visit recorded for " + cid + "."),
                 "Referred": ("2", "Referral sent. The service will contact the family."),
                 "Reviewed, no action": ("3", "Noted. Your comment has been saved.")}.get(status)
        out = (f'<div class="bout">{reply[0]}</div><div class="delivered">Delivered</div><div class="bin">{reply[1]}</div>') if reply else ""
        st.markdown(f"""
<div class="phone"><div class="screen">
  <div class="island"></div>
  <div class="status"><span>8:30</span><span class="icons">
    <svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" fill="#111"/><rect x="5" y="5" width="3" height="7" rx="1" fill="#111"/><rect x="10" y="2.5" width="3" height="9.5" rx="1" fill="#111"/><rect x="15" y="0" width="3" height="12" rx="1" fill="#111"/></svg>
    <svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 11.5 L10.4 9 A3.4 3.4 0 0 0 5.6 9 Z M8 1 C11 1 13.6 2.2 15.5 4.1 L13.8 5.8 C12.3 4.3 10.3 3.4 8 3.4 S3.7 4.3 2.2 5.8 L0.5 4.1 C2.4 2.2 5 1 8 1 Z M8 5.3 C9.8 5.3 11.3 6 12.4 7.1 L10.8 8.7 C10.1 8 9.1 7.6 8 7.6 S5.9 8 5.2 8.7 L3.6 7.1 C4.7 6 6.2 5.3 8 5.3 Z" fill="#111"/></svg>
    <svg width="26" height="12" viewBox="0 0 26 12"><rect x="0.5" y="0.5" width="22" height="11" rx="3" fill="none" stroke="#111"/><rect x="2" y="2" width="16" height="8" rx="2" fill="#111"/><rect x="23.5" y="4" width="2" height="4" rx="1" fill="#111"/></svg>
  </span></div>
  <div class="apphead"><div class="avatar">IN</div><div class="who">INDANGA Alerts</div><div class="sub">Text Message &middot; SMS</div></div>
  <div class="thread"><div class="daystamp">Today 8:30</div><div class="bin">{alert}</div>{out}</div>
  <div class="inputbar"><div class="field">Text Message</div><div class="send"><svg width="14" height="14" viewBox="0 0 24 24"><path d="M12 4 L12 20 M5 11 L12 4 L19 11" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/></svg></div></div>
  <div class="homebar"></div>
</div></div>""", unsafe_allow_html=True)
        st.write("")
        for lab, stt in [("✅  Confirm visit done", "Visited"), ("📨  Refer to a service", "Referred"), ("📝  No action, add a note", "Reviewed, no action")]:
            if st.button(lab, width="stretch", key=f"b_{stt}"):
                st.session_state.status[cid] = stt
                st.toast(f"{cid}: {stt}")
                st.rerun()
        st.markdown(f'<div class="note" style="text-align:center">Status: <b>{status or "To visit"}</b> &middot; INDANGA suggests, the worker decides.</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ footer
st.markdown(f"""
<div class="footer"><img src="data:image/svg+xml;base64,{KIDS}" alt="Illustrated children">
<div class="txt">INDANGA prototype by <b>Tchandikou Ouadja Fare</b>, African Institute for Mathematical Sciences (AIMS) Rwanda &middot; UNICEF Rwanda @40 Pan-African Student Competition<br>
All data shown is simulated for demonstration. No real child is represented. Photo &copy; UNICEF/UNI725007/Iyakaremye.</div></div>
""", unsafe_allow_html=True)
