"""
Future Lens: AI Transition Simulator

Domain → Area → Skill → evolution timeline → drivers → future advice → simulation.

Run: streamlit run streamlit_app.py
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from taxonomy import (
    AREAS,
    BROAD_DOMAINS,
    DOMAIN_ICONS,
    build_skill_profile,
    get_skills_for_area,
)

st.set_page_config(
    page_title="Future Lens · AI Transition Simulator",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    from suite_deploy_probe import init_developer_mode_from_query

    init_developer_mode_from_query(st)
except Exception:
    pass

import future_lens_boot as _fl_boot

try:
    from future_lens_wizard import (
        ensure_wizard_session_keys,
        init_developer_mode_from_query,
        render_wizard_trace,
        select_domain,
        update_trace as _update_fl_trace,
    )

    init_developer_mode_from_query(st)
    ensure_wizard_session_keys(st)
    _update_fl_trace(
        st,
        persistence_ok=_fl_boot.PERSISTENCE_OK,
        boot_error=_fl_boot.BOOT_ERROR,
    )
except Exception as _wizard_import_exc:

    def ensure_wizard_session_keys(st_obj: Any) -> None:
        for key, default in (
            ("broad_domain", None),
            ("area", None),
            ("specific_skill", None),
            ("sim_year", 2030),
            ("timeline_year", None),
            ("wizard_complete", False),
        ):
            st_obj.session_state.setdefault(key, default)

    def _update_fl_trace(st_obj: Any, **fields: Any) -> None:
        pass

    def render_wizard_trace(st_obj: Any) -> None:
        pass

    def select_domain(st_obj: Any, domain: str) -> None:
        prev = st_obj.session_state.get("broad_domain")
        st_obj.session_state["broad_domain"] = domain
        if prev != domain:
            st_obj.session_state["area"] = None
            st_obj.session_state["specific_skill"] = None
            st_obj.session_state["timeline_year"] = None

    init_developer_mode_from_query = lambda _st: None  # type: ignore[assignment,misc]
    ensure_wizard_session_keys(st)

_fl_boot.bootstrap_persistence(st)
try:
    from suite_user_persistence import show_persistence_messages

    show_persistence_messages(st)
except Exception:
    pass
try:
    _update_fl_trace(st, restore_ran=bool(st.session_state.get("_suite_disk_state_restored::future_lens")))
except Exception:
    pass

if not _fl_boot.PERSISTENCE_OK:
    ensure_wizard_session_keys(st)  # type: ignore[misc]
    if _fl_boot.BOOT_ERROR and st.session_state.get("developer_mode"):
        st.sidebar.warning(f"Persistence unavailable: {_fl_boot.BOOT_ERROR}")

FL_ACTIVE_TAB_KEY = _fl_boot.FL_ACTIVE_TAB_KEY
FL_TAB_LABELS = _fl_boot.FL_TAB_LABELS

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(160deg, #0f0a1e 0%, #1a1033 35%, #0c1929 100%); }
    .block-container { padding-top: 1rem; max-width: 1200px; }
    .fl-hero {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 50%, #f59e0b 100%);
        border-radius: 20px; padding: 1.75rem 2rem; color: white; margin-bottom: 1.25rem;
    }
    .fl-hero h1 { margin: 0; font-size: 2rem; font-weight: 800; }
    .fl-hero p { margin: 0.5rem 0 0; opacity: 0.95; font-size: 1rem; line-height: 1.5; }
    .fl-goals {
        display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem;
    }
    .fl-goal-pill {
        background: rgba(255,255,255,0.18); border-radius: 999px;
        padding: 0.25rem 0.7rem; font-size: 0.78rem; font-weight: 600;
    }
    .fl-section { color: #f1f5f9; font-size: 1.25rem; font-weight: 800; margin: 1.5rem 0 0.4rem; }
    .fl-sub { color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.85rem; line-height: 1.45; }
    .fl-card {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 0.6rem; color: #e2e8f0;
        line-height: 1.5;
    }
    .fl-card-highlight {
        background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(219,39,119,0.15));
        border: 1px solid rgba(167,139,250,0.35);
    }
    .fl-year {
        font-size: 1.75rem; font-weight: 900;
        background: linear-gradient(90deg, #a78bfa, #f472b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .fl-year-forecast { opacity: 0.85; }
    .fl-step {
        display: inline-block; background: linear-gradient(90deg, #7c3aed, #db2777);
        border-radius: 999px; padding: 0.25rem 0.75rem; font-size: 0.72rem;
        font-weight: 800; color: white; margin-right: 0.4rem; letter-spacing: 0.03em;
    }
    .fl-step-done { background: rgba(34,197,94,0.35); color: #86efac; }
    .fl-breadcrumb {
        background: rgba(255,255,255,0.08); border-radius: 12px; padding: 0.75rem 1rem;
        color: #cbd5e1; font-size: 0.92rem; margin: 0.75rem 0 1rem;
    }
    .fl-breadcrumb strong { color: #f1f5f9; }
    .fl-driver {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px; padding: 1rem; height: 100%; color: #e2e8f0;
    }
    .fl-driver-icon { font-size: 1.6rem; margin-bottom: 0.3rem; }
    .fl-driver-name { font-weight: 800; color: #f1f5f9; font-size: 0.95rem; margin-bottom: 0.35rem; }
    .fl-driver-desc { font-size: 0.82rem; color: #94a3b8; line-height: 1.45; }
    .fl-advice-title { color: #c4b5fd; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.4rem; }
    .fl-advice-item {
        background: rgba(255,255,255,0.04); border-left: 3px solid #7c3aed;
        padding: 0.5rem 0.75rem; margin-bottom: 0.35rem; border-radius: 0 8px 8px 0;
        color: #e2e8f0; font-size: 0.88rem;
    }
    .fl-sim-scene {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px; padding: 1.1rem 1.2rem; margin-bottom: 0.65rem;
        color: #e2e8f0; min-height: 120px;
    }
    .fl-sim-label { color: #a78bfa; font-weight: 800; font-size: 0.85rem; margin-bottom: 0.4rem; }
    .fl-day-block {
        background: rgba(124,58,237,0.15); border: 1px solid rgba(167,139,250,0.3);
        border-radius: 10px; padding: 0.65rem 0.85rem; margin-bottom: 0.4rem;
        color: #e2e8f0; font-size: 0.85rem;
    }
    .fl-day-time { color: #c4b5fd; font-weight: 700; font-size: 0.78rem; }
    .fl-timeline-nav {
        display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 1rem;
    }
    .fl-timeline-era {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px; padding: 0.5rem 0.75rem; text-align: center;
        color: #94a3b8; font-size: 0.8rem; min-width: 70px;
    }
    .fl-timeline-era-active {
        background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(219,39,119,0.25));
        border-color: rgba(167,139,250,0.5); color: #f1f5f9; font-weight: 700;
    }
    .fl-forecast-badge {
        display: inline-block; background: rgba(245,158,11,0.25); color: #fbbf24;
        border-radius: 999px; padding: 0.15rem 0.55rem; font-size: 0.7rem;
        font-weight: 700; margin-left: 0.4rem; vertical-align: middle;
    }
    div[data-testid="stSidebar"] { background: rgba(15,10,30,0.95); }
    </style>
    """,
    unsafe_allow_html=True,
)


def _render_hero() -> None:
    st.markdown(
        """
        <div class="fl-hero">
            <h1>🔮 Future Lens: AI Transition Simulator</h1>
            <p>Start with a broad domain — not a random job. Drill down to one specific skill,
            then explore how it evolved, why it changed, and how to prepare for 2030–2050.</p>
            <div class="fl-goals">
                <span class="fl-goal-pill">1 · How it evolved</span>
                <span class="fl-goal-pill">2 · Why it changed</span>
                <span class="fl-goal-pill">3 · Where it's heading</span>
                <span class="fl-goal-pill">4 · Practical advice</span>
                <span class="fl-goal-pill">5 · Future simulation</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_progress() -> None:
    steps = [
        ("STEP 1", "Domain", st.session_state.broad_domain),
        ("STEP 2", "Area", st.session_state.area),
        ("STEP 3", "Skill", st.session_state.specific_skill),
    ]
    cols = st.columns(3)
    for col, (label, name, value) in zip(cols, steps):
        done = value is not None
        cls = "fl-step fl-step-done" if done else "fl-step"
        with col:
            st.markdown(
                f'<span class="{cls}">{label}</span> **{name}**'
                + (f"<br><small>{value}</small>" if value else ""),
                unsafe_allow_html=True,
            )


def _persist_wizard_state() -> None:
    try:
        if _fl_boot.PERSISTENCE_OK:
            _fl_boot.autosave_future_lens_state(st)
    except Exception:
        pass


def _render_selection_wizard() -> bool:
    st.markdown('<div class="fl-section">Choose your focus</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Follow the hierarchy: broad domain → specific area → one precise skill or activity.</div>',
        unsafe_allow_html=True,
    )
    _render_progress()

    # Step 1 — Domain (visual grid)
    st.markdown('<span class="fl-step">STEP 1</span> **Choose a broad domain**', unsafe_allow_html=True)
    domain_cols = st.columns(4)
    for i, domain in enumerate(BROAD_DOMAINS):
        with domain_cols[i % 4]:
            icon = DOMAIN_ICONS.get(domain, "🔮")
            st.button(
                f"{icon} {domain}",
                key=f"domain_{domain}",
                use_container_width=True,
                on_click=select_domain,
                args=(st, domain),
            )

    domain = st.session_state.get("broad_domain")
    if not domain:
        st.info("Select a domain above to continue.")
        try:
            _update_fl_trace(st, wizard_block_reason="Select a domain above to continue.")
        except Exception:
            pass
        return False

    # Step 2 — Area
    areas = AREAS.get(domain, ("General activity",))
    st.markdown('<span class="fl-step">STEP 2</span> **Choose a more specific area**', unsafe_allow_html=True)
    prev_area = st.session_state.area
    area = st.selectbox(
        "Area",
        areas,
        index=areas.index(st.session_state.area) if st.session_state.area in areas else 0,
        key="_area_select",
        label_visibility="collapsed",
    )
    if area != prev_area:
        st.session_state.area = area
        st.session_state.specific_skill = None
        st.session_state.timeline_year = None
        _persist_wizard_state()
        st.rerun()
    st.session_state.area = area

    # Step 3 — Skill
    specifics = get_skills_for_area(domain, area)
    st.markdown(
        '<span class="fl-step">STEP 3</span> **Choose a specific skill or activity**',
        unsafe_allow_html=True,
    )
    prev_skill = st.session_state.specific_skill
    specific = st.selectbox(
        "Skill",
        specifics,
        index=specifics.index(st.session_state.specific_skill) if st.session_state.specific_skill in specifics else 0,
        key="_skill_select",
        label_visibility="collapsed",
    )
    if specific != prev_skill:
        st.session_state.specific_skill = specific
        st.session_state.timeline_year = None
        _persist_wizard_state()
        st.rerun()
    st.session_state.specific_skill = specific

    icon = DOMAIN_ICONS.get(domain, "🔮")
    st.markdown(
        f"""
        <div class="fl-breadcrumb">
            {icon} <strong>{domain}</strong> → <strong>{area}</strong> → <strong>{specific}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return True


def _render_timeline(profile) -> None:
    st.markdown('<div class="fl-section">📅 How this skill evolved</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Exactly how this specific activity changed decade by decade — from the past through today into forecast years.</div>',
        unsafe_allow_html=True,
    )

    years = [p.year for p in profile.timeline]
    if st.session_state.timeline_year not in years:
        st.session_state.timeline_year = years[0]
    _fl_boot.record_decade_render_snapshot(
        st,
        timeline_year=st.session_state.timeline_year,
        surface="timeline",
    )

    nav_html = '<div class="fl-timeline-nav">'
    for y in years:
        pt = next(p for p in profile.timeline if p.year == y)
        active = " fl-timeline-era-active" if y == st.session_state.timeline_year else ""
        forecast = " 🔮" if pt.is_forecast else ""
        nav_html += f'<div class="fl-timeline-era{active}">{y}{forecast}</div>'
    nav_html += "</div>"
    st.markdown(nav_html, unsafe_allow_html=True)

    year_cols = st.columns(min(len(years), 8))
    for i, y in enumerate(years):
        with year_cols[i % len(year_cols)]:
            pt = next(p for p in profile.timeline if p.year == y)
            label = f"{y}{'  🔮' if pt.is_forecast else ''}"
            if st.button(label, key=f"year_{y}", use_container_width=True):
                _fl_boot.apply_future_lens_decade_selection(
                    st,
                    timeline_year=y,
                    source=f"timeline_button_{y}",
                )
                try:
                    from future_lens_activity import log_technology_timeline_review

                    log_technology_timeline_review(topic=str(y))
                except Exception:
                    pass
                st.rerun()

    point = next(p for p in profile.timeline if p.year == st.session_state.timeline_year)
    forecast_cls = " fl-year-forecast" if point.is_forecast else ""
    badge = '<span class="fl-forecast-badge">FORECAST</span>' if point.is_forecast else ""
    st.markdown(
        f'<div class="fl-year{forecast_cls}">{point.year}{badge}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="fl-card fl-card-highlight">
            <strong style="font-size:1.1rem;">{point.headline}</strong><br><br>
            {point.description}<br><br>
            <span style="color:#a78bfa;font-weight:700;">Tools & methods:</span> {point.tools}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Full evolution at a glance**")
    for point in profile.timeline:
        tag = " 🔮" if point.is_forecast else ""
        st.markdown(
            f"**{point.year}{tag}** — {point.headline}: {point.description[:120]}{'…' if len(point.description) > 120 else ''}"
        )


def _render_drivers(profile) -> None:
    st.markdown('<div class="fl-section">🔍 What drove the changes?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Five forces shaped how this skill transformed — and will keep shaping it.</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(len(profile.drivers))
    for col, driver in zip(cols, profile.drivers):
        with col:
            st.markdown(
                f"""
                <div class="fl-driver">
                    <div class="fl-driver-icon">{driver.icon}</div>
                    <div class="fl-driver-name">{driver.name}</div>
                    <div class="fl-driver-desc">{driver.description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_future_advice(profile) -> None:
    try:
        from future_lens_activity import log_skill_forecast_review

        skill_sig = (profile.domain, profile.area, profile.name)
        if st.session_state.get("_cc_fl_skill_forecast_sig") != skill_sig:
            st.session_state["_cc_fl_skill_forecast_sig"] = skill_sig
            log_skill_forecast_review(skill=profile.name)
    except Exception:
        pass
    st.markdown('<div class="fl-section">💡 Future Advice</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Connect the forecast to practical life decisions — what to learn, focus on, and watch out for.</div>',
        unsafe_allow_html=True,
    )
    advice = profile.advice
    sections = [
        ("📖 What should I learn?", advice.learn),
        ("⭐ Skills that will matter", advice.skills_that_matter),
        ("🛑 Stop spending time on", advice.stop_spending_time_on),
        ("🎯 Focus on", advice.focus_on),
        ("🚀 Emerging opportunities", advice.opportunities),
        ("⚠️ Risks to watch", advice.risks),
    ]
    c1, c2 = st.columns(2)
    for i, (title, items) in enumerate(sections):
        col = c1 if i % 2 == 0 else c2
        with col:
            items_html = "".join(f'<div class="fl-advice-item">{item}</div>' for item in items)
            st.markdown(
                f'<div class="fl-advice-title">{title}</div>{items_html}',
                unsafe_allow_html=True,
            )


def _maybe_log_career_analysis(profile) -> None:
    """Log career transition analysis once per domain/area/skill (Command Center Continue)."""
    try:
        from future_lens_activity import log_career_analysis

        sig = (profile.domain, profile.area, profile.name)
        if st.session_state.get("_cc_fl_career_sig") == sig:
            return
        st.session_state["_cc_fl_career_sig"] = sig
        st.session_state["wizard_complete"] = True
        scenario = f"{profile.domain} / {profile.area} / {profile.name}"
        log_career_analysis(
            scenario=scenario,
            domain=profile.domain,
            area=profile.area,
            skill=profile.name,
            sim_year=st.session_state.get("sim_year"),
            timeline_year=st.session_state.get("timeline_year"),
        )
    except Exception:
        pass


def _day_schedule(day_text: str) -> str:
    """Split a day description into visual time blocks."""
    parts = day_text.replace(". ", ".|").split("|")
    labels = ["Morning", "Midday", "Afternoon", "Evening"]
    blocks = []
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        label = labels[i] if i < len(labels) else f"Block {i + 1}"
        blocks.append(
            f'<div class="fl-day-block"><div class="fl-day-time">{label}</div>{part}</div>'
        )
    return "".join(blocks) if blocks else f'<div class="fl-day-block">{day_text}</div>'


def _render_simulation_mode(profile) -> None:
    st.markdown('<div class="fl-section">🚀 Future Simulation Mode</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="fl-sub">Step into 2030, 2040, or 2050. Experience the tools, work, learning, and a day in the life for this skill.</div>',
        unsafe_allow_html=True,
    )

    year_cols = st.columns(3)
    for col, y in zip(year_cols, (2030, 2040, 2050)):
        with col:
            active = st.session_state.sim_year == y
            if st.button(
                f"{'▶ ' if active else ''}{y}{'  (active)' if active else ''}",
                key=f"sim_{y}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                _fl_boot.apply_future_lens_decade_selection(
                    st,
                    sim_year=y,
                    source=f"sim_button_{y}",
                )
                try:
                    from future_lens_activity import log_simulation_completed

                    project = f"{profile.domain} / {profile.area}"
                    sim_sig = (project, profile.name, y)
                    if st.session_state.get("_cc_fl_sim_year_sig") != sim_sig:
                        st.session_state["_cc_fl_sim_year_sig"] = sim_sig
                        log_simulation_completed(
                            simulation=profile.name,
                            project=project,
                            domain=profile.domain,
                            area=profile.area,
                            sim_year=y,
                        )
                except Exception:
                    pass
                st.rerun()

    year = st.session_state.sim_year
    _fl_boot.record_decade_render_snapshot(st, sim_year=year, surface="simulation")
    scene = profile.simulation[year]
    progress = min(1.0, (year - 2020) / 30)
    st.progress(progress, text=f"Future immersion · {year} · {int(progress * 100)}% toward 2050")

    st.markdown(
        f"""
        <div class="fl-card fl-card-highlight" style="text-align:center;margin-bottom:1rem;">
            <strong style="font-size:1.15rem;">You are in {year}</strong><br>
            <span style="color:#94a3b8;">Simulating: {profile.name} · {profile.area} · {profile.domain}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            f'<div class="fl-sim-scene"><div class="fl-sim-label">🛠️ TOOLS YOU USE</div>{scene["tools"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="fl-sim-scene"><div class="fl-sim-label">💼 HOW WORK IS DONE</div>{scene["work"]}</div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="fl-sim-scene"><div class="fl-sim-label">📚 HOW LEARNING HAPPENS</div>{scene["learning"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="fl-sim-scene"><div class="fl-sim-label">🌅 A NORMAL DAY</div>{_day_schedule(scene["day"])}</div>',
            unsafe_allow_html=True,
        )


# ── Sidebar (suite-standard order) ───────────────────────────────────────────

with st.sidebar:
    try:
        from suite_app_shell import render_suite_sidebar_account_shell

        render_suite_sidebar_account_shell(st)
    except Exception:
        try:
            from suite_command_center_link import render_command_center_sidebar_link

            render_command_center_sidebar_link(st)
        except Exception:
            pass

    try:
        from future_lens_sidebar import render_saved_session_controls

        render_saved_session_controls(st, on_reset=_fl_boot.default_reset_future_lens_session)
    except Exception as exc:
        trace = st.session_state.setdefault("_fl_reset_render_trace", {})
        trace["attempted"] = True
        trace["completed"] = False
        trace["error"] = str(exc)

    try:
        from suite_deploy_probe import render_future_lens_developer_diagnostics

        render_future_lens_developer_diagnostics(st)
    except Exception:
        try:
            render_wizard_trace(st)
        except Exception:
            pass

    st.divider()
    st.markdown("## 🔮 Future Lens")
    st.caption("Domain → Area → Skill")
    st.divider()
    if st.session_state.get("broad_domain"):
        st.markdown(f"**Domain:** {DOMAIN_ICONS.get(st.session_state.broad_domain, '')} {st.session_state.broad_domain}")
    else:
        st.markdown("**Domain:** —")
    st.markdown(f"**Area:** {st.session_state.get('area') or '—'}")
    st.markdown(f"**Skill:** {st.session_state.get('specific_skill') or '—'}")
    st.divider()
    st.markdown("**How to use**")
    st.markdown(
        "1. Pick a domain\n2. Narrow to an area\n3. Choose one skill\n4. Explore the timeline\n5. Read the advice\n6. Simulate the future"
    )

# ── Main ──────────────────────────────────────────────────────────────────────

_render_hero()

if _render_selection_wizard():
    profile = build_skill_profile(
        st.session_state.broad_domain,
        st.session_state.area,
        st.session_state.specific_skill,
    )
    st.divider()
    _fl_boot.apply_future_lens_view_from_restore(st)
    _maybe_log_career_analysis(profile)
    tab_label = st.radio(
        "Section",
        list(FL_TAB_LABELS),
        horizontal=True,
        key=FL_ACTIVE_TAB_KEY,
        label_visibility="collapsed",
    )
    _fl_boot.sync_future_lens_view_after_tab(st, tab_label)
    if tab_label == FL_TAB_LABELS[0]:
        _render_timeline(profile)
    elif tab_label == FL_TAB_LABELS[1]:
        _render_drivers(profile)
    elif tab_label == FL_TAB_LABELS[2]:
        _render_future_advice(profile)
    else:
        _render_simulation_mode(profile)

try:
    _fl_boot.autosave_future_lens_state(st)
    from suite_user_persistence import clear_workspace_autosave_block

    clear_workspace_autosave_block(st, "future_lens")
except Exception:
    pass

st.caption("Future Lens · Daniel AI Suite · educational simulator · forecasts are illustrative")
