"""
Command Center activity hooks — completed simulations and reviews only.
"""

from __future__ import annotations

from typing import Any


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

        record_activity(
            "future_lens",
            event,
            page=page or "Future Lens",
            metrics=metrics or {},
            summary=summary,
            resume_key=resume_key,
            resume_title=resume_title,
            resume_subtitle=resume_subtitle,
            local_state=metrics,
        )
    except Exception:
        pass


def log_simulation_completed(*, simulation: str, project: str = "", domain: str = "") -> None:
    sim = str(simulation or domain or "").strip()
    proj = str(project or "").strip()
    lower = sim.lower()
    if "teach" in lower or "education" in lower:
        title = "Continue teaching simulation"
    elif "career" in lower or "transition" in lower or "ai" in lower:
        title = "Continue AI career transition analysis"
    else:
        title = f"Continue {sim} simulation"
    _record(
        "simulation_completed",
        page="Simulation",
        metrics={"simulation": sim, "project": proj, "domain": domain},
        summary=f"Simulated future of {sim}" if sim else "Completed a future scenario",
        resume_key=f"sim:{sim[:40]}",
        resume_title=title,
        resume_subtitle=proj or sim,
    )


def log_career_analysis(*, scenario: str) -> None:
    label = str(scenario or "").strip()
    _record(
        "career_analysis",
        page="Simulation",
        metrics={"scenario": label, "project": label},
        summary=f"Compared future career scenarios ({label})" if label else "Compared future career scenarios",
        resume_key=f"career:{label[:40]}",
        resume_title="Continue career transition analysis",
        resume_subtitle=label,
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
