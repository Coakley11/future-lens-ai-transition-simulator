"""Timeline and domain content for Future Lens (Phase 1 demo data)."""

from __future__ import annotations

from dataclasses import dataclass

TIMELINE_YEARS: tuple[int, ...] = (1980, 1990, 2000, 2010, 2020, 2025, 2030, 2040, 2050)

IMPACT_PROFILES: dict[str, dict[str, str]] = {
    "Conservative": {
        "label": "Conservative",
        "emoji": "🐢",
        "description": "AI assists humans but rarely replaces core judgment. Change is gradual.",
        "speed": "0.6",
        "tone": "Humans stay in the loop for most high-stakes decisions.",
    },
    "Balanced": {
        "label": "Balanced",
        "emoji": "⚖️",
        "description": "AI handles routine work; humans focus on strategy, creativity, and relationships.",
        "speed": "1.0",
        "tone": "Partnership model — AI does drafts, humans approve and refine.",
    },
    "Aggressive": {
        "label": "Aggressive",
        "emoji": "🚀",
        "description": "AI automates most workflows; humans orchestrate systems and define values.",
        "speed": "1.4",
        "tone": "Radical transformation — new roles emerge quickly, old tasks shrink fast.",
    },
}


@dataclass(frozen=True)
class TimelineEra:
    year: int
    headline: str
    how_people_worked: str
    tools: str
    skills: str
    ai_changed: str
    whats_next: str


@dataclass(frozen=True)
class DomainInfo:
    key: str
    name: str
    icon: str
    category: str
    tagline: str
    color: str


DOMAINS: tuple[DomainInfo, ...] = (
    DomainInfo("teaching", "Teaching", "👩‍🏫", "Work & Careers", "Classrooms become coaching studios.", "#8b5cf6"),
    DomainInfo("programming", "Programming", "💻", "Work & Careers", "Code becomes intent and review.", "#6366f1"),
    DomainInfo("data_analysis", "Data Analysis", "📈", "Work & Careers", "Insights arrive before you ask.", "#3b82f6"),
    DomainInfo("accounting", "Accounting", "🧾", "Work & Careers", "Compliance runs in the background.", "#0ea5e9"),
    DomainInfo("office_work", "Office Work", "🏢", "Work & Careers", "Inboxes become action dashboards.", "#06b6d4"),
    DomainInfo("learning_math", "Learning Math", "➗", "Education", "Practice adapts to every mistake.", "#a855f7"),
    DomainInfo("tutoring", "Tutoring", "🎓", "Education", "1:1 support scales globally.", "#d946ef"),
    DomainInfo("research", "Research", "🔬", "Education", "Literature reviews in minutes.", "#ec4899"),
    DomainInfo("writing_papers", "Writing Papers", "📝", "Education", "Structure and citations automated.", "#f43f5e"),
    DomainInfo("portfolio_mgmt", "Portfolio Management", "💼", "Investing", "Always-on risk monitoring.", "#14b8a6"),
    DomainInfo("financial_research", "Financial Research", "🔍", "Investing", "AI scans markets 24/7.", "#10b981"),
    DomainInfo("retirement_planning", "Retirement Planning", "🌅", "Investing", "Life-path simulations on demand.", "#22c55e"),
    DomainInfo("basketball", "Playing Basketball", "🏀", "Sports", "Biomechanics in your pocket.", "#f97316"),
    DomainInfo("sports_training", "Sports Training", "🏋️", "Sports", "Personalized drills every session.", "#fb923c"),
    DomainInfo("fantasy_sports", "Fantasy Sports", "⚾", "Sports", "Lineup engines + human intuition.", "#eab308"),
    DomainInfo("guitar", "Learning Guitar", "🎸", "Music", "Real-time fingering feedback.", "#e879f9"),
    DomainInfo("piano", "Learning Piano", "🎹", "Music", "AI metronome + expression coach.", "#c026d3"),
    DomainInfo("songwriting", "Songwriting", "🎵", "Music", "Co-write with infinite inspiration.", "#a21caf"),
    DomainInfo("performance", "Performance", "🎤", "Music", "Live coaching through ear monitors.", "#86198f"),
    DomainInfo("photography", "Photography", "📷", "Media", "Capture decisions, not settings.", "#38bdf8"),
    DomainInfo("video_creation", "Video Creation", "🎬", "Media", "Edit by describing the story.", "#0ea5e9"),
    DomainInfo("social_media", "Social Media", "📱", "Media", "Audience intelligence at scale.", "#0284c7"),
)

DOMAIN_CATEGORIES: tuple[str, ...] = (
    "Work & Careers",
    "Education",
    "Investing",
    "Sports",
    "Music",
    "Media",
)


def _timeline_data() -> dict[int, TimelineEra]:
    return {
        1980: TimelineEra(
            1980,
            "The analog office era",
            "Most work happened in person — memos, meetings, and paper files.",
            "Typewriters, landlines, filing cabinets, early PCs in big companies.",
            "Handwriting, filing, basic computer literacy, domain expertise.",
            "Almost no AI — expert systems were lab experiments.",
            "Personal computers and email begin reshaping office rhythm.",
        ),
        1990: TimelineEra(
            1990,
            "The internet arrives at work",
            "Email and early software replace some paper workflows.",
            "Windows PCs, fax machines, early web browsers, spreadsheets.",
            "Digital literacy, networking basics, software tool fluency.",
            "Search engines and automation scripts hint at what's coming.",
            "Mobile devices and cloud storage start decentralizing work.",
        ),
        2000: TimelineEra(
            2000,
            "Always-on connectivity",
            "Remote collaboration grows; software eats repetitive tasks.",
            "Laptops, CRMs, ERPs, Google Search, early smartphones.",
            "Cross-functional communication, data entry, web research.",
            "Recommendation systems and targeted ads show machine learning in the wild.",
            "Social platforms and app ecosystems reshape media and marketing.",
        ),
        2010: TimelineEra(
            2010,
            "The cloud + mobile decade",
            "Work becomes location-flexible; SaaS tools multiply.",
            "Slack, Zoom, AWS, smartphones, tablets, app stores.",
            "Agile collaboration, UX awareness, basic analytics.",
            "AI assists translation, search ranking, and ad targeting at scale.",
            "Machine learning moves from research labs into products.",
        ),
        2020: TimelineEra(
            2020,
            "Remote work + AI acceleration",
            "Hybrid work normalizes; digital tools become the default office.",
            "Video calls, Notion, GitHub, cloud AI APIs, LLM assistants.",
            "Prompting, async communication, data storytelling, adaptability.",
            "ChatGPT-era AI drafts content, code, and analysis — humans review.",
            "Agents and copilots begin handling multi-step workflows.",
        ),
        2025: TimelineEra(
            2025,
            "Copilots everywhere",
            "Most knowledge workers pair with AI for drafts, research, and planning.",
            "LLM copilots, agent frameworks, AI IDEs, smart wearables.",
            "Judgment, taste, ethics, relationship-building, system design.",
            "AI handles first drafts; humans focus on decisions and creativity.",
            "Personal AI stacks connect apps across work, learning, and life.",
        ),
        2030: TimelineEra(
            2030,
            "AI as daily infrastructure",
            "Routine knowledge work is largely automated; roles shift to oversight.",
            "Autonomous agents, voice-first interfaces, ambient computing.",
            "Orchestration, verification, coaching, cross-domain synthesis.",
            "Most teams have AI teammates with memory and tool access.",
            "Regulation and trust frameworks mature; human-AI teams standard.",
        ),
        2040: TimelineEra(
            2040,
            "Human + AI partnership norm",
            "People manage fleets of AI agents; work centers on meaning and strategy.",
            "Personal AI chief-of-staff, simulated environments, neural interfaces (early).",
            "Empathy, leadership, creative direction, ethical governance.",
            "Domain copilots are expert-level; humans set goals and boundaries.",
            "New careers emerge around AI literacy, alignment, and experience design.",
        ),
        2050: TimelineEra(
            2050,
            "The augmented society",
            "Learning, creating, and deciding happen in human-AI loops by default.",
            "Ubiquitous AI, personalized education OS, synthetic media tools, smart cities.",
            "Wisdom, curiosity, community-building, inter-disciplinary thinking.",
            "AI may co-create art, science, and policy — humans define values.",
            "The question shifts from 'Will AI replace me?' to 'What do I want to become?'",
        ),
    }


TIMELINE: dict[int, TimelineEra] = _timeline_data()


FUTURE_WORKFLOWS: dict[str, dict[int, list[str]]] = {
    "teaching": {
        2040: [
            "AI prepares differentiated lesson plans overnight.",
            "AI identifies student misconceptions from class work.",
            "AI drafts parent updates and progress summaries.",
            "Teacher focuses on mentoring, motivation, and classroom culture.",
        ],
    },
    "portfolio_mgmt": {
        2040: [
            "AI continuously monitors portfolio risk and drift.",
            "AI suggests allocation changes based on goals and market regime.",
            "AI handles tax-loss harvesting and document prep.",
            "Human approves strategy and sets values-based constraints.",
        ],
    },
    "piano": {
        2040: [
            "AI backing band adapts to your tempo and style.",
            "AI practice coach listens and gives real-time feedback.",
            "Performance analytics track expression, not just notes.",
            "Musician focuses on artistry and live connection.",
        ],
    },
    "programming": {
        2040: [
            "AI builds features from plain-language specs.",
            "AI runs tests, security scans, and refactors.",
            "Engineer reviews architecture and edge cases.",
            "Focus shifts to product vision and user empathy.",
        ],
    },
    "fantasy_sports": {
        2040: [
            "AI models injury risk and matchup edges in real time.",
            "AI drafts lineup variants for every scoring format.",
            "You choose strategy: safe floor vs. boom-or-bust.",
            "The fun stays human — rivalry, hunches, and trash talk.",
        ],
    },
    "video_creation": {
        2040: [
            "Describe the story; AI assembles rough cuts.",
            "AI handles captions, B-roll, and color consistency.",
            "Creator directs tone, pacing, and emotional beats.",
            "Editing becomes curating and storytelling.",
        ],
    },
}


CAREER_EVOLUTION: dict[str, dict[str, list[str]]] = {
    "Conservative": {
        "decline": ["Manual data entry", "Basic report formatting", "Routine scheduling"],
        "remain": ["Domain expertise", "Client relationships", "Quality review", "Ethical judgment"],
        "emerge": ["AI workflow oversight", "Prompt libraries", "Human-in-the-loop QA"],
    },
    "Balanced": {
        "decline": ["First-draft writing", "Simple coding tasks", "Static spreadsheet analysis"],
        "remain": ["Strategic thinking", "Creative direction", "Team leadership", "Cross-domain synthesis"],
        "emerge": ["Agent orchestration", "AI literacy coaching", "Experience design", "Verification specialists"],
    },
    "Aggressive": {
        "decline": ["Most repetitive knowledge work", "Template-based content", "Rule-only decision jobs"],
        "remain": ["Values setting", "High-trust relationships", "Novel problem framing", "Taste and curation"],
        "emerge": ["AI alignment roles", "Synthetic media directors", "Personal AI architects", "Meaning-makers"],
    },
}


def get_future_workflow(domain_key: str, year: int, impact: str) -> list[str]:
    base = FUTURE_WORKFLOWS.get(domain_key, {}).get(
        year,
        [
            f"AI handles routine tasks in {domain_key.replace('_', ' ')}.",
            "Humans set goals, review outputs, and add creative judgment.",
            "Workflows become faster, more personalized, and less repetitive.",
            "Your edge: taste, trust, and the questions you ask.",
        ],
    )
    if impact == "Conservative":
        return [f"🐢 {line} (gradual adoption)" for line in base[:3]] + [
            "🐢 Human approval required at every major step."
        ]
    if impact == "Aggressive":
        return [f"🚀 {line.replace('AI ', 'AI aggressively ')}" for line in base] + [
            "🚀 Most routine steps run autonomously unless you pause them."
        ]
    return [f"⚖️ {line}" for line in base]
