# Future Lens: AI Transition Simulator

**An interactive timeline simulator** built with Python and Streamlit. Explore how work, learning, creativity, sports, investing, and everyday life evolved from **1980 to today** — and how AI may reshape them through **2050** — with account-owned workspace isolation in the Daniel Cohen AI Suite.

**Live demo:** [future-lens-ai-transition-simulator.streamlit.app](https://future-lens-ai-transition-simulator-m6n4kaku28ztzlxfts2xt6.streamlit.app)  
**Deploy branch:** `dev` · **Entry point:** `streamlit_app.py`

Built as part of the **Daniel Cohen AI Suite** (shared workspace auth, cloud persistence, and Command Center handoffs).

---

## At a Glance

| | |
|---|---|
| **Role** | Full-stack Python exploratory app — taxonomy-driven timelines, simulation UX, and test-driven persistence |
| **Stack** | Python 3.11+ · Streamlit · custom taxonomy engine · optional Supabase · suite deep links |
| **Scale** | Domain → Area → Skill wizard · Evolution / Drivers / Future Advice / Simulation tabs |
| **Differentiators** | Structured skill taxonomy · decade-aware simulation state · workspace-scoped UI restore |

---

## For Employers & Reviewers

This project demonstrates product thinking for exploratory AI UX: a guided taxonomy (domain/area/skill), multi-tab narrative flow, and **per-account workspace isolation** so authenticated users restore their own simulation year, tab state, and selections. Inspect `tests/test_workspace_account_ownership.py` and `tests/test_future_lens_workspace.py` without running the full UI.

---

## 1. Executive Summary

Most “future of work” demos are static slide decks. Future Lens is an **interactive simulator** where users pick a domain, drill into skills, read evolution history, explore drivers, get future advice, and run forward simulations.

The app is designed as a portfolio piece demonstrating **structured information architecture, persistence under Streamlit reruns, suite workspace patterns, and narrative UX** — not a generic chat wrapper.

---

## 2. Why This Project Is Different

| Typical future-of-AI demo | This platform |
|---------------------------|---------------|
| Single chat thread | Domain → Area → Skill wizard with tabs |
| No historical grounding | 1980–today evolution timeline per skill |
| Stateless refresh | Workspace-scoped disk + cloud restore |
| One global user | Account-owned workspace per login |

---

## 3. Key Features

| Tab / Area | Highlights |
|------------|------------|
| **Evolution** | Historical timeline for selected skill (1980 → today) |
| **Drivers** | Forces shaping the transition |
| **Future Advice** | Actionable guidance for the selected skill |
| **Simulation** | Forward scenarios through 2050 |
| **Taxonomy wizard** | Broad domains, areas, and skill profiles |
| **Account & Workspace** | Real Accounts auth, owned workspace, foreign URL rejection |

---

## 4. Analytics & AI Methods

| Method | Use |
|--------|-----|
| Taxonomy engine | `taxonomy.py` — domains, areas, skill profiles |
| Timeline narratives | Decade-bucketed evolution copy |
| Simulation state | `sim_year` and tab persistence across reruns |
| Activity events | Suite activity feed tags with `workspace_id` |
| AMI integration (suite) | Command Center deep links and resume launch |

---

## 5. Technical Architecture

```
streamlit_app.py              # Page shell, wizard, tab routing
future_lens_boot.py           # bootstrap_persistence, resume launch
future_lens_persistent_state.py # prepare_future_lens_workspace, disk sync
future_lens_wizard.py         # Domain/area/skill selection + trace
taxonomy.py                   # Skill taxonomy and profiles
├── suite_workspace.py        # bootstrap_suite_workspace
├── suite_workspace_registry.py # Account-owned workspace registry
├── suite_auth.py             # Real Accounts + ownership enforcement
└── suite_user_persistence.py # sync_workspace_protocol
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

## 6. Screenshots

| # | Page | Filename (placeholder) | What to show |
|---|------|------------------------|--------------|
| 1 | Domain wizard | `screenshots/01-domain-wizard.png` | Domain → Area → Skill selection |
| 2 | Evolution | `screenshots/02-evolution-timeline.png` | Historical timeline for a skill |
| 3 | Drivers | `screenshots/03-drivers.png` | Transition drivers panel |
| 4 | Simulation | `screenshots/04-simulation-2050.png` | Forward simulation controls |

---

## 7. Local Setup

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

## 8. Roadmap

**Near term**
- [ ] Manual Daniel/Ariel workspace validation (sim year, tab, taxonomy selection)
- [ ] Richer simulation parameter controls
- [ ] Cross-device restore validation (Sprint D)

**Medium term**
- [ ] LLM-backed future advice with grounded citations
- [ ] Export/share simulation snapshots
- [ ] CI matrix with workspace ownership tests on every PR

---

## 9. Testing

```bash
python -m pytest tests/test_workspace_account_ownership.py tests/test_future_lens_workspace.py -q
```

Workspace isolation acceptance: `sim_year`, active tab, and taxonomy selections scoped per workspace; foreign `?suite_workspace=` URLs rejected at startup.

---

## Status

Phase 1 prototype — demo timeline data and future simulations. Workspace isolation v2 aligns with Baseball/Music account-owned pattern.

## Author

Daniel Cohen
