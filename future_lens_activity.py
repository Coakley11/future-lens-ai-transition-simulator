"""Future Lens activity hooks — completed simulations and reviews only."""

from __future__ import annotations

from typing import Any


def _active_workspace_id() -> str:
    try:
        from suite_workspace import get_active_workspace_id

        return get_active_workspace_id()
    except Exception:
        return "daniel"


def _record(
    event: str,
    *,
    page: str = "",
    metrics: dict[str, Any] | None = None,
    summary: str = "",
    resume_key: str = "",
    resume_title: str = "",
    resume_subtitle: str = "",
) -> None:
    try:
        from suite_activity_client import record_activity

        payload = dict(metrics or {})
        payload.setdefault("workspace_id", _active_workspace_id())
        record_activity(
            "future_lens",
            event,
            page=page or "Future Lens",
            metrics=payload,
            summary=summary,
            resume_key=resume_key,
            resume_title=resume_title,
            resume_subtitle=resume_subtitle,
            local_state=payload,
        )
    except Exception:
        pass


def log_simulation_completed(*, simulation: str, project: str = "", domain: str = "", area: str = "", sim_year: int | None = None) -> None:
    sim = str(simulation or domain or "").strip()
    proj = str(project or "").strip()
    lower = sim.lower()
    if "teach" in lower or "education" in lower:
        title = "Continue teaching simulation"
    elif "career" in lower or "transition" in lower or "ai" in lower:
        title = "Continue AI career transition analysis"
    else:
        title = f"Continue {sim} simulation"
    metrics: dict[str, Any] = {"simulation": sim, "project": proj, "domain": domain}
    if domain:
        metrics["broad_domain"] = domain
    if area:
        metrics["area"] = area
    if sim:
        metrics["specific_skill"] = sim
    if sim_year is not None:
        metrics["sim_year"] = sim_year
    _record(
        "simulation_completed",
        page="Simulation",
        metrics=metrics,
        summary=f"Simulated future of {sim}" if sim else "Completed a future scenario",
        resume_key=f"sim:{sim[:40]}",
        resume_title=title,
        resume_subtitle=proj or sim,
    )


def log_career_analysis(
    *,
    scenario: str,
    domain: str = "",
    area: str = "",
    skill: str = "",
    sim_year: int | None = None,
    timeline_year: int | None = None,
) -> None:
    label = str(scenario or "").strip()
    dom = str(domain or "").strip()
    ar = str(area or "").strip()
    sk = str(skill or "").strip()
    project = f"{dom} / {ar}".strip(" /") if dom or ar else label
    metrics: dict[str, Any] = {
        "scenario": label,
        "project": project,
        "simulation": sk or label,
        "domain": dom,
        "broad_domain": dom,
        "area": ar,
        "specific_skill": sk,
    }
    if sim_year is not None:
        metrics["sim_year"] = sim_year
    if timeline_year is not None:
        metrics["timeline_year"] = timeline_year
    _record(
        "career_analysis",
        page="Simulation",
        metrics=metrics,
        summary=f"Compared future career scenarios ({label})" if label else "Compared future career scenarios",
        resume_key=f"career:{label[:40]}",
        resume_title="Continue career transition analysis",
        resume_subtitle=project or label,
    )


def log_skill_forecast_review(*, skill: str = "") -> None:
    _record(
        "skill_forecast_review",
        page="Future Lens",
        metrics={"simulation": skill},
        summary="Reviewed future skill recommendations",
        resume_key="future:skills",
        resume_title="Review future skill recommendations",
        resume_subtitle=skill or "Skill forecast",
    )


def log_technology_timeline_review(*, topic: str = "") -> None:
    _record(
        "technology_timeline_review",
        page="Future Lens",
        metrics={"simulation": topic, "project": topic},
        summary=f"Completed technology timeline: {topic}" if topic else "Completed technology timeline",
        resume_key=f"timeline:{topic[:40]}",
        resume_title="Continue technology timeline",
        resume_subtitle=topic,
    )
