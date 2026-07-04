# Future Lens: AI Transition Simulator

**An interactive timeline simulator** built with Python and Streamlit. Explore how work, learning, creativity, sports, investing, and everyday life evolved from **1980 to today** — and how AI may reshape them through **2050** — with account-owned workspace isolation in the Daniel Cohen AI Suite.

**Live demo:** [future-lens-ai-transition-simulator.streamlit.app](https://future-lens-ai-transition-simulator-m6n4kaku28ztzlxfts2xt6.streamlit.app)  
**Deploy branch:** `dev` · **Entry point:** `streamlit_app.py`

Built as part of the **Daniel Cohen AI Suite** (shared workspace auth, cloud persistence, and Command Center handoffs).

---

## Executive Summary

Most "future of work" demos tell users what might happen; Future Lens lets them explore how change actually unfolds. Future Lens is an **interactive AI transition simulator** where users pick a domain, drill into areas and skills, read historical evolution from 1980 to today, explore transition drivers, get future-facing advice, and run forward simulations through 2050.

The app covers 11 broad domains, 50+ areas, and skill-level timelines through a Domain → Area → Skill wizard with Evolution, Drivers, Future Advice, and Simulation tabs.

The goal is to help users understand how technology changes real skills over time — what changed, why it changed, what may happen next, and how to adapt.

The app is designed as a portfolio piece demonstrating **structured information architecture, taxonomy-driven UX, persistence under Streamlit reruns, suite workspace patterns, and narrative simulation design** — not a generic chat wrapper.

Current scope includes a broad cross-domain taxonomy, decade-aware narrative content, simulation state persistence, suite account ownership, and cloud-ready deployment.

---

## Example Questions This App Can Help Answer

**Career & Work**
- How has computer programming changed from 1980 to today?
- Which skills are becoming more valuable as AI changes business operations?
- What should I focus on learning if my role is being affected by automation?

**Education & Learning**
- How have tutoring, homework, testing, and classroom instruction evolved?
- What should students learn differently in an AI-assisted world?
- Which learning skills still matter when tools can answer questions instantly?

**Sports, Music & Creativity**
- How have analytics changed basketball, baseball, scouting, and coaching?
- How has music production or songwriting changed with digital tools and AI?
- Which creative skills remain human advantages?

**Finance, Healthcare & Science**
- How is AI changing portfolio research, budgeting, diagnosis support, or lab research?
- What risks and opportunities appear as each field becomes more automated?
- Which parts of a workflow are likely to be augmented rather than replaced?

**Future Planning**
- What could this skill look like in 2030, 2040, or 2050?
- Which drivers are pushing the transition?
- What should I stop spending time on, and what should I focus on instead?

---

## At a Glance

| | |
|---|---|
| **Role** | Full-stack Python exploratory app — taxonomy-driven timelines, simulation UX, and test-driven persistence |
| **Stack** | Python 3.11+ · Streamlit · custom taxonomy engine · optional Supabase · suite deep links |
| **Scale** | 11 domains · 50+ areas · Domain → Area → Skill wizard · Evolution / Drivers / Future Advice / Simulation tabs |
| **Differentiators** | Structured skill taxonomy · decade-aware simulation state · workspace-scoped UI restore |

---

## Development Scope

Future Lens is part of a seven-application analytics suite developed by a single developer.

The project combines taxonomy design, narrative product UX, simulation workflows, persistence systems, authentication, cloud deployment, and cross-application workflows into a unified platform — one of several sibling apps (Command Center, Baseball, Music, Investment, NBA, AMI) sharing suite infrastructure.

---

## For Employers & Reviewers

This project demonstrates product thinking for exploratory AI UX:

| Skill area | Evidence in Future Lens |
|------------|-------------------------|
| **Information architecture** | Domain → Area → Skill wizard backed by `taxonomy.py` |
| **Product design** | Multi-tab flow: Evolution, Drivers, Future Advice, Simulation |
| **Narrative UX** | Decade-bucketed history, transition drivers, and future advice |
| **Persistence design** | Workspace-scoped simulation year, active tab, and taxonomy selection |
| **Systems design** | Suite auth, resume launch, disk + cloud restore, ownership registry |
| **Cross-application integration** | Command Center deep links, suite activity events, AMI-ready context |

Inspect `tests/test_workspace_account_ownership.py` and `tests/test_future_lens_workspace.py` without running the full UI.

---

## Why This Project Is Different

Most future-of-AI demos are either prediction essays or open-ended chat prompts.

Future Lens was designed as a **structured transition simulator** — users choose a real domain, narrow to a specific skill, inspect its history, understand the forces changing it, and simulate where it may go next.

The same platform architecture supports historical timelines, transition drivers, practical advice, forward simulations, workspace restore, and suite handoffs through a shared taxonomy and persistence layer.

By grounding forecasts in historical timelines and skill-level transitions, Future Lens makes AI change feel concrete, comparable, and easier to reason about.

| Typical future-of-AI demo | This platform |
|---------------------------|---------------|
| Single chat thread | Domain → Area → Skill wizard with tabs |
| Static prediction essay | Interactive timeline + simulation workflow |
| No historical grounding | 1980–today evolution timeline per skill |
| Generic advice | Skill-specific learn / focus / risk / opportunity guidance |
| Stateless refresh | Workspace-scoped disk + cloud restore |
| One global user | Account-owned workspace per login |
| Isolated prototype | Suite-integrated with Command Center handoffs |

Future Lens is a **structured AI transition product**, not a generic future-of-work slideshow.

---

## Key Features

| Tab / Area | Highlights |
|------------|------------|
| **Evolution** | Historical timeline for selected skill (1980 → today) |
| **Drivers** | Forces shaping the transition |
| **Future Advice** | Actionable guidance for the selected skill |
| **Simulation** | Forward scenarios through 2050 |
| **Taxonomy wizard** | Broad domains, areas, and skill profiles |
| **Account & Workspace** | Real Accounts auth, owned workspace, foreign URL rejection |

---

## Analytics & AI Methods

| Method | Use |
|--------|-----|
| Taxonomy engine | `taxonomy.py` — domains, areas, skill profiles |
| Timeline narratives | Decade-bucketed evolution copy |
| Simulation state | `sim_year` and tab persistence across reruns |
| Transition driver modeling | Forces, risks, opportunities, and adaptation advice |
| Activity events | Suite activity feed tags with `workspace_id` |
| AMI integration (suite) | Command Center deep links and resume launch |

---

## Technical Architecture

```
streamlit_app.py                # Page shell, wizard, tab routing
future_lens_boot.py             # bootstrap_persistence, resume launch
future_lens_persistent_state.py # prepare_future_lens_workspace, disk sync
future_lens_wizard.py           # Domain/area/skill selection + trace
taxonomy.py                     # Skill taxonomy and profiles
├── suite_workspace.py          # bootstrap_suite_workspace
├── suite_workspace_registry.py # Account-owned workspace registry
├── suite_auth.py               # Real Accounts + ownership enforcement
└── suite_user_persistence.py   # sync_workspace_protocol
```

**Persistence paths**

| Layer | Path / key |
|-------|------------|
| Active workspace (account) | `data/workspaces/_active/{owner_user_id}.json` |
| Ownership registry | `data/workspaces/_ownership_registry.json` |
| App state | `data/workspaces/{workspace_id}/future_lens_user_state.json` |
| Cloud | Supabase scoped via `future_lens__{workspace}` |

**Startup order (workspace isolation v2)**

1. `apply_suite_auth_gate(st)` — auth gate before persistence boot
2. `bootstrap_persistence(st)` → `bootstrap_suite_workspace(st)` → `prepare_future_lens_workspace(st)`
3. `apply_suite_resume_launch(st, "future_lens")`

---

## Screenshots

| # | Page | Filename (placeholder) | What to show |
|---|------|------------------------|--------------|
| 1 | Domain wizard | `screenshots/01-domain-wizard.png` | Domain → Area → Skill selection |
| 2 | Evolution | `screenshots/02-evolution-timeline.png` | Historical timeline for a skill |
| 3 | Drivers | `screenshots/03-drivers.png` | Transition drivers panel |
| 4 | Simulation | `screenshots/04-simulation-2050.png` | Forward simulation controls |

---

## Portfolio Value

Future Lens shows that you can:

- Design a **taxonomy-driven product** that turns broad AI-transition ideas into navigable user workflows
- Build **interactive narrative UX** across historical context, drivers, advice, and future simulation
- Model **skill evolution over time** with decade-aware timelines and forward-looking scenarios
- Implement **workspace-scoped persistence** that survives Streamlit reruns and restores user selections
- Integrate **suite-wide infrastructure** — auth, ownership registry, cloud sync, resume launch, and Command Center handoffs
- Translate an ambiguous topic ("how AI changes work") into a structured, reviewable application
- Transform an ambiguous strategic topic into a structured, testable software product
- Support portfolio review with focused tests for persistence, wizard behavior, workspace ownership, and import smoke coverage

A hiring manager can grasp scope and sophistication in **2–3 minutes** from this README plus the live demo.

---

## Local Setup

### Requirements

- **Python 3.11+**
- `pip install -r requirements.txt`

### Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Optional environment variables

| Variable | Purpose |
|----------|---------|
| `SUITE_SUPABASE_URL` | Cloud persistence |
| `SUITE_SUPABASE_ANON_KEY` | Supabase client |
| `SUITE_AUTH_ENABLED` | Real Account sign-in |

### Streamlit Cloud

1. Connect repo on [share.streamlit.io](https://share.streamlit.io)
2. **Main file:** `streamlit_app.py`
3. **Branch:** `dev`

---

## Roadmap

**Near term**
- [ ] Manual Daniel/Ariel workspace validation (sim year, tab, taxonomy selection)
- [ ] Richer simulation parameter controls
- [ ] Cross-device restore validation (Sprint D)

**Medium term**
- [ ] LLM-backed future advice with grounded citations
- [ ] Export/share simulation snapshots
- [ ] CI matrix with workspace ownership tests on every PR

---

## Testing

```bash
python -m pytest tests/test_workspace_account_ownership.py tests/test_future_lens_workspace.py -q
```

Workspace isolation acceptance: `sim_year`, active tab, and taxonomy selections scoped per workspace; foreign `?suite_workspace=` URLs rejected at startup.

---

## Status

Phase 1 prototype — demo timeline data and future simulations. Workspace isolation v2 aligns with Baseball/Music account-owned pattern.

## Author

Daniel Cohen
