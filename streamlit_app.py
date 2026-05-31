"""
Future Lens: AI Transition Simulator

Explore how work, learning, creativity, sports, investing, and life evolved
from 1980 to today — and how AI may reshape them through 2050.

Run: streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from content import (
    CAREER_EVOLUTION,
    DOMAIN_CATEGORIES,
    DOMAINS,
    IMPACT_PROFILES,
    TIMELINE,
    TIMELINE_YEARS,
    DomainInfo,
    get_future_workflow,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Future Lens · AI Transition Simulator",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #0f0a1e 0%, #1a1033 35%, #0c1929 100%);
    }
    .block-container { padding-top: 1.2rem; max-width: 1180px; }
    .fl-hero {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 50%, #f59e0b 100%);
        border-radius: 24px;
        padding: 2rem 2.2rem;
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: 0 20px 50px rgba(124, 58, 237, 0.35);
    }
    .fl-hero h1 { margin: 0 0 0.35rem; font-size: 2.3rem; font-weight: 800; }
    .fl-hero p { margin: 0; opacity: 0.95; font-size: 1.05rem; line-height: 1.55; max-width: 780px; }
    .fl-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.65rem;
        color: #e2e8f0;
    }
    .fl-card h3 { color: #f8fafc; margin: 0 0 0.35rem; font-size: 1rem; }
    .fl-card p { margin: 0; color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; }
    .fl-section {
        color: #f1f5f9;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 1.5rem 0 0.75rem;
    }
    .fl-sub { color: #94a3b8; font-size: 0.92rem; margin-bottom: 1rem; }
    .fl-domain-chip {
        display: inline-block;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 0.55rem 0.85rem;
        margin: 0.25rem;
        color: #e2e8f0;
        font-size: 0.88rem;
        font-weight: 600;
    }
    .fl-timeline-year {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .fl-impact-pill {
        display: inline-block;
        border-radius: 999px;
        padding: 0.35rem 0.85rem;
        font-size: 0.82rem;
        font-weight: 700;
        margin-right: 0.35rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 0.65rem;
    }
    div[data-testid="stMetric"] label { color: #94a3b8 !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f8fafc !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session state defaults ────────────────────────────────────────────────────

if "impact" not in st.session_state:
    st.session_state.impact = "Balanced"
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "teaching"
if "timeline_year" not in st.session_state:
    st.session_state.timeline_year = 2025
if "run_sim" not in st.session_state:
    st.session_state.run_sim = False


def _domain_by_key(key: str) -> DomainInfo | None:
    for d in DOMAINS:
        if d.key == key:
            return d
    return None


def _render_hero() -> None:
    st.markdown(
        """
        <div class="fl-hero">
            <h1>🔮 Future Lens: AI Transition Simulator</h1>
            <p>See how work, learning, creativity, sports, investing, and everyday life evolved
            from 1980 to today — and explore playful, thoughtful scenarios for 2030–2050.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_home() -> None:
    st.markdown('<div class="fl-section">🏠 What is Future Lens?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="fl-card">
                <h3>🌌 A time-travel lens on AI</h3>
                <p>Future Lens is an interactive simulator — not a prediction engine.
                It helps you explore how tools, skills, and daily workflows changed decade by decade,
                and how AI might reshape them next.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="fl-card">
                <h3>🎯 Built for curiosity</h3>
                <p>Teachers, investors, musicians, athletes, students, and creators can all
                explore their domain, compare eras, and imagine future workflows —
                with Conservative, Balanced, or Aggressive AI futures.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fl-section">⚡ Why AI is changing work</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="fl-sub">AI compresses the cost of drafting, analyzing, and coordinating —
        which shifts human value toward judgment, relationships, creativity, and ethics.</div>
        """,
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("1980 → 2025", "Tool explosion", "PC → Cloud → Copilots")
    with m2:
        st.metric("Skills shift", "Less routine", "More judgment")
    with m3:
        st.metric("Domains", str(len(DOMAINS)), "6 categories")
    with m4:
        st.metric("Future horizon", "2050", "3 AI scenarios")

    st.markdown('<div class="fl-section">🎛️ Interactive domain selector</div>', unsafe_allow_html=True)
    st.markdown('<div class="fl-sub">Pick a domain to explore across the timeline and future simulator.</div>', unsafe_allow_html=True)

    for category in DOMAIN_CATEGORIES:
        st.markdown(f"**{category}**")
        chips = [d for d in DOMAINS if d.category == category]
        cols = st.columns(min(len(chips), 4))
        for col, domain in zip(cols, chips):
            with col:
                if st.button(
                    f"{domain.icon} {domain.name}",
                    key=f"pick_{domain.key}",
                    use_container_width=True,
                ):
                    st.session_state.selected_domain = domain.key
                    st.rerun()

    selected = _domain_by_key(st.session_state.selected_domain)
    if selected:
        st.success(f"Selected: {selected.icon} **{selected.name}** — {selected.tagline}")


def _render_timeline() -> None:
    st.markdown('<div class="fl-section">🕰️ Timeline Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Slide through decades — see how people worked, what tools existed, and what changed.</div>',
        unsafe_allow_html=True,
    )

    year = st.select_slider(
        "Choose a year",
        options=list(TIMELINE_YEARS),
        value=st.session_state.timeline_year,
        key="timeline_slider",
    )
    st.session_state.timeline_year = year
    era = TIMELINE[year]

    st.markdown(f'<div class="fl-timeline-year">{year}</div>', unsafe_allow_html=True)
    st.markdown(f"### {era.headline}")

    t1, t2 = st.columns(2, gap="medium")
    cards = [
        ("👷 How people worked", era.how_people_worked),
        ("🛠️ Tools that existed", era.tools),
        ("🧠 Skills that mattered", era.skills),
        ("🤖 What AI changed", era.ai_changed),
    ]
    for col, (title, body) in zip([t1, t2, t1, t2], cards):
        with col:
            st.markdown(
                f'<div class="fl-card"><h3>{title}</h3><p>{body}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        f'<div class="fl-card"><h3>🔭 What may happen next</h3><p>{era.whats_next}</p></div>',
        unsafe_allow_html=True,
    )

    if year >= 2025:
        st.info("💡 Tip: Jump to **Future Simulation** to see a detailed workflow for your selected domain.")


def _render_domains() -> None:
    st.markdown('<div class="fl-section">🗂️ Explore Domains</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">22 domains across work, education, investing, sports, music, and media.</div>',
        unsafe_allow_html=True,
    )

    domain_key = st.selectbox(
        "Choose a domain",
        options=[d.key for d in DOMAINS],
        format_func=lambda k: f"{_domain_by_key(k).icon} {_domain_by_key(k).name} — {_domain_by_key(k).category}",
        index=[d.key for d in DOMAINS].index(st.session_state.selected_domain),
    )
    st.session_state.selected_domain = domain_key
    domain = _domain_by_key(domain_key)
    if not domain:
        return

    st.markdown(
        f"""
        <div class="fl-card" style="border-left: 4px solid {domain.color};">
            <h3>{domain.icon} {domain.name}</h3>
            <p><strong>{domain.category}</strong> · {domain.tagline}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Quick era comparison**")
    c1, c2, c3 = st.columns(3)
    for col, yr in zip([c1, c2, c3], (2000, 2025, 2040)):
        with col:
            era = TIMELINE[yr]
            st.markdown(f"**{yr}**")
            st.caption(era.how_people_worked[:120] + "…")


def _render_impact_meter() -> str:
    st.markdown('<div class="fl-section">📊 AI Impact Meter</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Choose how fast and how deeply AI reshapes the future in this simulator.</div>',
        unsafe_allow_html=True,
    )

    impact = st.radio(
        "Future intensity",
        options=list(IMPACT_PROFILES.keys()),
        horizontal=True,
        format_func=lambda k: f"{IMPACT_PROFILES[k]['emoji']} {k}",
        index=list(IMPACT_PROFILES.keys()).index(st.session_state.impact),
    )
    st.session_state.impact = impact
    profile = IMPACT_PROFILES[impact]

    st.markdown(
        f"""
        <div class="fl-card">
            <h3>{profile['emoji']} {profile['label']} AI future</h3>
            <p>{profile['description']}</p>
            <p><em>{profile['tone']}</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return impact


def _render_future_simulation(impact: str) -> None:
    st.markdown('<div class="fl-section">🚀 Future Simulation</div>', unsafe_allow_html=True)

    domain = _domain_by_key(st.session_state.selected_domain)
    sim_year = st.select_slider(
        "Simulate year",
        options=[2030, 2040, 2050],
        value=st.session_state.sim_year,
    )
    st.session_state.sim_year = sim_year

    if st.button("✨ Simulate My Future Workflow", type="primary", use_container_width=True):
        st.session_state.run_sim = True

    if st.session_state.run_sim:
        dname = domain.name if domain else "Your domain"
        st.markdown(f"### {dname} · {sim_year} · {impact} scenario")

        steps = get_future_workflow(st.session_state.selected_domain, sim_year, impact)
        for i, step in enumerate(steps, start=1):
            st.markdown(
                f'<div class="fl-card"><h3>Step {i}</h3><p>{step}</p></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("Press **Simulate My Future Workflow** to generate your scenario.")


def _render_career_evolution(impact: str) -> None:
    st.markdown('<div class="fl-section">🧬 Career Evolution</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="fl-sub">How roles may shift under a <strong>{impact}</strong> AI future.</div>',
        unsafe_allow_html=True,
    )

    evo = CAREER_EVOLUTION[impact]
    c1, c2, c3 = st.columns(3, gap="medium")
    sections = [
        ("📉 Skills that decline", evo["decline"], "#f87171"),
        ("💎 Skills that remain valuable", evo["remain"], "#34d399"),
        ("🌱 New skills emerging", evo["emerge"], "#60a5fa"),
    ]
    for col, (title, items, color) in zip([c1, c2, c3], sections):
        with col:
            st.markdown(f"**{title}**")
            for item in items:
                st.markdown(
                    f'<div class="fl-card" style="border-left: 3px solid {color};"><p>{item}</p></div>',
                    unsafe_allow_html=True,
                )


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🔮 Future Lens")
    st.caption("AI Transition Simulator · Phase 1")
    page = st.radio(
        "Navigate",
        ["Home", "Timeline Explorer", "Domains", "Future Simulation", "Career Evolution"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Quick settings**")
    st.session_state.impact = st.selectbox(
        "AI Impact",
        list(IMPACT_PROFILES.keys()),
        index=list(IMPACT_PROFILES.keys()).index(st.session_state.impact),
    )
    st.session_state.selected_domain = st.selectbox(
        "Domain",
        [d.key for d in DOMAINS],
        format_func=lambda k: f"{_domain_by_key(k).icon} {_domain_by_key(k).name}",
        index=[d.key for d in DOMAINS].index(st.session_state.selected_domain),
    )

# ── Main pages ────────────────────────────────────────────────────────────────

_render_hero()

if page == "Home":
    _render_home()
elif page == "Timeline Explorer":
    _render_timeline()
elif page == "Domains":
    _render_domains()
elif page == "Future Simulation":
    impact = _render_impact_meter()
    _render_future_simulation(impact)
elif page == "Career Evolution":
    _render_career_evolution(st.session_state.impact)

st.caption("Future Lens · Phase 1 prototype · demo data · part of the Daniel AI Suite ecosystem")
