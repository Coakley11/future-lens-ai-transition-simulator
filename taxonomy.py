"""Three-level skill taxonomy and rich timeline content for Future Lens."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimelinePoint:
    year: int
    headline: str
    description: str
    tools: str
    is_forecast: bool = False


@dataclass(frozen=True)
class DriverDetail:
    name: str
    icon: str
    description: str


@dataclass(frozen=True)
class FutureAdvice:
    learn: tuple[str, ...]
    skills_that_matter: tuple[str, ...]
    stop_spending_time_on: tuple[str, ...]
    focus_on: tuple[str, ...]
    opportunities: tuple[str, ...]
    risks: tuple[str, ...]


@dataclass(frozen=True)
class SkillProfile:
    key: str
    name: str
    icon: str
    domain: str
    area: str
    timeline: tuple[TimelinePoint, ...]
    drivers: tuple[DriverDetail, ...]
    advice: FutureAdvice
    simulation: dict[int, dict[str, str]]


BROAD_DOMAINS: tuple[str, ...] = (
    "Technology",
    "Education",
    "Sports",
    "Music",
    "Finance",
    "Healthcare",
    "Science",
    "Transportation",
    "Communication",
    "Entertainment",
    "Business",
)

DOMAIN_ICONS: dict[str, str] = {
    "Technology": "💻",
    "Education": "📚",
    "Sports": "🏀",
    "Music": "🎹",
    "Finance": "💰",
    "Healthcare": "🏥",
    "Science": "🔬",
    "Transportation": "🚗",
    "Communication": "💬",
    "Entertainment": "🎬",
    "Business": "💼",
}

AREAS: dict[str, tuple[str, ...]] = {
    "Technology": (
        "Researching information",
        "Internet browsing",
        "Computer programming",
        "Excel & spreadsheets",
        "Data analysis",
        "Writing",
        "Communication",
        "Search engines",
    ),
    "Education": (
        "Learning math",
        "Teaching",
        "Tutoring",
        "Homework",
        "Testing",
        "Classroom instruction",
    ),
    "Sports": (
        "Basketball",
        "Baseball",
        "Football",
        "Training methods",
        "Scouting",
        "Analytics",
        "Coaching",
    ),
    "Music": (
        "Learning piano",
        "Learning guitar",
        "Learning saxophone",
        "Music production",
        "Songwriting",
        "Recording",
        "Live performance",
    ),
    "Finance": (
        "Portfolio management",
        "Financial research",
        "Retirement planning",
        "Budgeting",
        "Risk analysis",
    ),
    "Healthcare": (
        "Diagnosis support",
        "Patient education",
        "Medical research",
        "Care coordination",
    ),
    "Science": (
        "Lab research",
        "Data collection",
        "Publishing findings",
        "Collaboration",
    ),
    "Transportation": (
        "Route planning",
        "Fleet management",
        "Logistics",
        "Navigation",
    ),
    "Communication": (
        "Email",
        "Meetings",
        "Presentations",
        "Social media",
    ),
    "Entertainment": (
        "Video creation",
        "Gaming",
        "Streaming",
        "Storytelling",
    ),
    "Business": (
        "Strategy",
        "Sales",
        "Operations",
        "Customer support",
    ),
}

SKILL_ALIASES: dict[tuple[str, str], str] = {
    ("Technology", "Researching information"): "researching_information",
    ("Technology", "Internet browsing"): "internet_browsing",
    ("Technology", "Computer programming"): "computer_programming",
    ("Technology", "Excel & spreadsheets"): "excel_spreadsheets",
    ("Technology", "Data analysis"): "data_analysis",
    ("Technology", "Writing"): "writing",
    ("Technology", "Communication"): "tech_communication",
    ("Technology", "Search engines"): "search_engines",
    ("Education", "Learning math"): "learning_math",
    ("Education", "Teaching"): "teaching",
    ("Education", "Tutoring"): "tutoring",
    ("Education", "Homework"): "homework",
    ("Education", "Testing"): "testing",
    ("Education", "Classroom instruction"): "classroom_instruction",
    ("Sports", "Basketball"): "basketball",
    ("Sports", "Baseball"): "baseball",
    ("Sports", "Football"): "football",
    ("Sports", "Training methods"): "training_methods",
    ("Sports", "Scouting"): "scouting",
    ("Sports", "Analytics"): "sports_analytics",
    ("Sports", "Coaching"): "coaching",
    ("Music", "Learning piano"): "learning_piano",
    ("Music", "Learning guitar"): "learning_guitar",
    ("Music", "Learning saxophone"): "learning_saxophone",
    ("Music", "Music production"): "music_production",
    ("Music", "Songwriting"): "songwriting",
    ("Music", "Recording"): "recording",
    ("Music", "Live performance"): "live_performance",
    ("Finance", "Portfolio management"): "portfolio_management",
    ("Finance", "Financial research"): "financial_research",
    ("Finance", "Retirement planning"): "retirement_planning",
    ("Finance", "Budgeting"): "budgeting",
    ("Finance", "Risk analysis"): "risk_analysis",
    ("Healthcare", "Diagnosis support"): "diagnosis_support",
    ("Healthcare", "Patient education"): "patient_education",
    ("Healthcare", "Medical research"): "medical_research",
    ("Healthcare", "Care coordination"): "care_coordination",
    ("Science", "Lab research"): "lab_research",
    ("Science", "Data collection"): "data_collection",
    ("Science", "Publishing findings"): "publishing_findings",
    ("Science", "Collaboration"): "science_collaboration",
    ("Transportation", "Route planning"): "route_planning",
    ("Transportation", "Fleet management"): "fleet_management",
    ("Transportation", "Logistics"): "logistics",
    ("Transportation", "Navigation"): "navigation",
    ("Communication", "Email"): "email",
    ("Communication", "Meetings"): "meetings",
    ("Communication", "Presentations"): "presentations",
    ("Communication", "Social media"): "social_media",
    ("Entertainment", "Video creation"): "video_creation",
    ("Entertainment", "Gaming"): "gaming",
    ("Entertainment", "Streaming"): "streaming",
    ("Entertainment", "Storytelling"): "storytelling",
    ("Business", "Strategy"): "strategy",
    ("Business", "Sales"): "sales",
    ("Business", "Operations"): "operations",
    ("Business", "Customer support"): "customer_support",
}

SKILLS: dict[str, tuple[str, ...]] = {
    "researching_information": (
        "Finding information",
        "Academic research",
        "Reading news",
        "Studying a topic",
    ),
    "internet_browsing": (
        "Navigating websites",
        "Bookmarking & organizing",
        "Deep reading online",
        "Evaluating web sources",
    ),
    "computer_programming": (
        "Writing code",
        "Debugging",
        "Code review",
        "Learning to program",
        "System design",
    ),
    "excel_spreadsheets": (
        "Data entry",
        "Formulas & functions",
        "Pivot tables",
        "Financial modeling",
    ),
    "data_analysis": (
        "Exploratory analysis",
        "Reporting & dashboards",
        "Statistical modeling",
        "Data visualization",
    ),
    "writing": (
        "Creative writing",
        "Technical writing",
        "Editing & revision",
        "Copywriting",
    ),
    "tech_communication": (
        "Email & messaging",
        "Video calls",
        "Async collaboration",
        "Technical documentation",
    ),
    "search_engines": (
        "Query formulation",
        "Result evaluation",
        "Advanced search techniques",
        "Information literacy",
    ),
    "learning_math": (
        "Arithmetic & algebra",
        "Problem solving",
        "Proof & reasoning",
        "Applied mathematics",
    ),
    "teaching": (
        "Creating lessons",
        "Grading",
        "Explaining concepts",
        "Tutoring students",
    ),
    "tutoring": (
        "One-on-one instruction",
        "Homework help",
        "Test preparation",
        "Motivation & coaching",
    ),
    "homework": (
        "Completing assignments",
        "Research for projects",
        "Group projects",
        "Time management",
    ),
    "testing": (
        "Standardized tests",
        "Formative assessment",
        "Designing exams",
        "Grading at scale",
    ),
    "classroom_instruction": (
        "Lecture delivery",
        "Discussion facilitation",
        "Hands-on activities",
        "Differentiated instruction",
    ),
    "basketball": (
        "Practicing basketball",
        "Learning basketball",
        "Shooting development",
        "Coaching basketball",
        "NBA playing style",
        "Scouting players",
    ),
    "baseball": (
        "Batting practice",
        "Pitching development",
        "Fielding drills",
        "Scouting talent",
        "Coaching baseball",
    ),
    "football": (
        "Playbook learning",
        "Film study",
        "Strength training",
        "Game strategy",
        "Coaching football",
    ),
    "training_methods": (
        "Periodization",
        "Recovery planning",
        "Injury prevention",
        "Performance testing",
    ),
    "scouting": (
        "Player evaluation",
        "Talent identification",
        "Draft preparation",
        "Opponent analysis",
    ),
    "sports_analytics": (
        "Statistical modeling",
        "Performance metrics",
        "Predictive analysis",
        "Data visualization",
    ),
    "coaching": (
        "Practice planning",
        "Player development",
        "In-game decisions",
        "Team culture building",
    ),
    "learning_piano": (
        "Reading sheet music",
        "Hand technique",
        "Practice routines",
        "Performance preparation",
    ),
    "learning_guitar": (
        "Chord progressions",
        "Fingerpicking",
        "Improvisation",
        "Song learning",
    ),
    "learning_saxophone": (
        "Embouchure & breath",
        "Scales & technique",
        "Jazz improvisation",
        "Ensemble playing",
    ),
    "music_production": (
        "Beat making",
        "Mixing & mastering",
        "Sound design",
        "DAW workflows",
    ),
    "songwriting": (
        "Lyric writing",
        "Melody composition",
        "Song structure",
        "Co-writing",
    ),
    "recording": (
        "Studio setup",
        "Microphone technique",
        "Multi-track recording",
        "Post-production",
    ),
    "live_performance": (
        "Stage presence",
        "Sound check",
        "Audience engagement",
        "Tour logistics",
    ),
    "portfolio_management": (
        "Asset allocation",
        "Rebalancing",
        "Risk monitoring",
        "Client reporting",
    ),
    "financial_research": (
        "Company analysis",
        "Market scanning",
        "Economic forecasting",
        "Due diligence",
    ),
    "retirement_planning": (
        "Savings projections",
        "Withdrawal strategies",
        "Tax optimization",
        "Longevity planning",
    ),
    "budgeting": (
        "Expense tracking",
        "Savings goals",
        "Debt management",
        "Household forecasting",
    ),
    "risk_analysis": (
        "Scenario modeling",
        "Stress testing",
        "Compliance review",
        "Portfolio hedging",
    ),
    "diagnosis_support": (
        "Symptom analysis",
        "Differential diagnosis",
        "Lab interpretation",
        "Treatment planning",
    ),
    "patient_education": (
        "Explaining conditions",
        "Medication guidance",
        "Lifestyle coaching",
        "Follow-up planning",
    ),
    "medical_research": (
        "Clinical trials",
        "Literature review",
        "Data analysis",
        "Publishing results",
    ),
    "care_coordination": (
        "Care team communication",
        "Discharge planning",
        "Referral management",
        "Patient tracking",
    ),
    "lab_research": (
        "Experiment design",
        "Sample preparation",
        "Instrument operation",
        "Results analysis",
    ),
    "data_collection": (
        "Field sampling",
        "Sensor deployment",
        "Survey design",
        "Quality control",
    ),
    "publishing_findings": (
        "Paper writing",
        "Peer review",
        "Data sharing",
        "Conference presentation",
    ),
    "science_collaboration": (
        "Cross-lab projects",
        "Grant writing",
        "Open science",
        "Team coordination",
    ),
    "route_planning": (
        "Map reading",
        "Traffic optimization",
        "Multi-stop routing",
        "Delivery scheduling",
    ),
    "fleet_management": (
        "Vehicle tracking",
        "Maintenance scheduling",
        "Driver assignment",
        "Cost optimization",
    ),
    "logistics": (
        "Supply chain planning",
        "Warehouse operations",
        "Last-mile delivery",
        "Inventory management",
    ),
    "navigation": (
        "GPS wayfinding",
        "Public transit routing",
        "Autonomous routing",
        "Real-time rerouting",
    ),
    "email": (
        "Composing messages",
        "Inbox management",
        "Professional correspondence",
        "Email automation",
    ),
    "meetings": (
        "Agenda planning",
        "Facilitation",
        "Note-taking",
        "Follow-up actions",
    ),
    "presentations": (
        "Slide design",
        "Public speaking",
        "Storytelling",
        "Audience Q&A",
    ),
    "social_media": (
        "Content creation",
        "Community management",
        "Analytics & growth",
        "Brand voice",
    ),
    "video_creation": (
        "Scriptwriting",
        "Filming",
        "Editing",
        "Distribution",
    ),
    "gaming": (
        "Game design",
        "Streaming gameplay",
        "Esports competition",
        "Community building",
    ),
    "streaming": (
        "Live broadcasting",
        "Audience interaction",
        "Content scheduling",
        "Platform optimization",
    ),
    "storytelling": (
        "Narrative structure",
        "Character development",
        "World building",
        "Serial storytelling",
    ),
    "strategy": (
        "Market analysis",
        "Competitive positioning",
        "Long-range planning",
        "Scenario planning",
    ),
    "sales": (
        "Prospecting",
        "Pitching",
        "Negotiation",
        "Relationship building",
    ),
    "operations": (
        "Process optimization",
        "Resource allocation",
        "Quality control",
        "Vendor management",
    ),
    "customer_support": (
        "Issue resolution",
        "Empathy & de-escalation",
        "Product knowledge",
        "Escalation management",
    ),
}


def get_skill_key(domain: str, area: str) -> str:
    return SKILL_ALIASES.get((domain, area), area.lower().replace(" ", "_").replace("&", ""))


def get_skills_for_area(domain: str, area: str) -> tuple[str, ...]:
    key = get_skill_key(domain, area)
    return SKILLS.get(key, (area,))


# ── Timeline builders ──────────────────────────────────────────────────────


def _research_timeline(specific: str) -> tuple[TimelinePoint, ...]:
    return (
        TimelinePoint(1980, "Library era", "Research meant physical libraries, card catalogs, and hours of manual searching.", "Card catalogs, encyclopedias, interlibrary loan"),
        TimelinePoint(1990, "Early databases", "Libraries plus CD-ROM databases and early online services expanded access.", "Encyclopedias, early databases, fax"),
        TimelinePoint(2000, "Search engines", "Google and the open web made broad research fast — quality filtering became the skill.", "Search engines, bookmarks, PDFs"),
        TimelinePoint(2010, "Mobile information", "Smartphones put massive reference material in every pocket.", "Smartphones, Wikipedia, cloud notes"),
        TimelinePoint(2020, "AI-assisted search", "Search plus AI summaries changed how people scan and synthesize sources.", "Search + AI assistants, citation tools"),
        TimelinePoint(2030, "AI research partners", f"For {specific.lower()}, AI proposes sources, checks bias, and drafts syntheses for human review.", "Personal research copilots, verified source graphs", True),
        TimelinePoint(2040, "Expert synthesis systems", "Real-time expert-level synthesis across domains with transparent reasoning trails.", "Expert AI panels, live fact-check layers", True),
        TimelinePoint(2050, "Human–AI knowledge collaboration", "Near-instant access to curated expertise; humans set questions and judge meaning.", "Collaborative knowledge environments", True),
    )


def _basketball_timeline(specific: str) -> tuple[TimelinePoint, ...]:
    return (
        TimelinePoint(1980, "Tape and instinct", "Coaches studied game tape manually; players learned through repetition and eye test.", "VHS tape, chalkboard"),
        TimelinePoint(1990, "Film rooms", "Systematic film study became standard; scouting reports typed by hand.", "VHS, stat sheets, overhead projectors"),
        TimelinePoint(2000, "Stats emerge", "Plus/minus and efficiency stats entered mainstream basketball culture.", "Spreadsheets, early video"),
        TimelinePoint(2010, "Analytics wave", "Three-point revolution and player tracking changed training and strategy.", "SportVU, analytics dashboards"),
        TimelinePoint(2020, "AI video breakdown", "Automated tagging of plays, shots, and defensive schemes.", "AI video, wearables, apps"),
        TimelinePoint(2030, "Personalized development", f"For {specific.lower()}, AI builds daily micro-drills from biomechanics and game film.", "Real-time biomechanics + AI coaching", True),
        TimelinePoint(2040, "Simulation-first training", "VR reps and AI opponents supplement live practice.", "VR simulators, digital twin athletes", True),
        TimelinePoint(2050, "Augmented performance", "Continuous feedback loops during games and practices.", "Smart court systems, adaptive coaching AI", True),
    )


def _teaching_timeline(specific: str) -> tuple[TimelinePoint, ...]:
    return (
        TimelinePoint(1980, "Chalkboard classroom", "Teachers lectured from textbooks; grading was manual and local.", "Chalkboards, textbooks, overhead transparencies"),
        TimelinePoint(1990, "Photocopies & early PCs", "Worksheets multiplied; computer labs appeared in schools.", "Copiers, early PC labs, grade books"),
        TimelinePoint(2000, "Internet in schools", "Online resources supplemented textbooks; email connected teachers and parents.", "Projectors, early LMS, email"),
        TimelinePoint(2010, "Digital classrooms", "Smartboards, Google Docs, and blended learning reshaped instruction.", "Smartboards, tablets, cloud docs"),
        TimelinePoint(2020, "Remote & hybrid teaching", "Zoom classrooms and AI grading assistants changed daily workflows.", "Video platforms, AI feedback tools"),
        TimelinePoint(2030, "AI lesson co-pilot", f"When {specific.lower()}, AI drafts materials and adapts to each student's pace.", "Adaptive lesson AI, real-time analytics", True),
        TimelinePoint(2040, "Personalized learning paths", "Each student gets a tailored curriculum; teachers become coaches.", "AI tutors + human mentorship", True),
        TimelinePoint(2050, "Human-centered education", "Teachers focus on motivation, ethics, and creativity; AI handles routine instruction.", "Immersive learning environments", True),
    )


def _programming_timeline(specific: str) -> tuple[TimelinePoint, ...]:
    return (
        TimelinePoint(1980, "Terminal era", "Programmers typed code into terminals; debugging meant print statements.", "Terminals, punch cards fading, C and BASIC"),
        TimelinePoint(1990, "IDEs & the web", "Visual IDEs and the early web opened programming to millions.", "Visual Basic, early Java, HTML"),
        TimelinePoint(2000, "Open source boom", "Collaborative coding on the internet; frameworks accelerated development.", "Git, Linux, JavaScript frameworks"),
        TimelinePoint(2010, "Cloud & mobile", "Apps everywhere; DevOps and APIs became core skills.", "AWS, mobile SDKs, GitHub"),
        TimelinePoint(2020, "AI code assistants", "Copilots autocomplete functions; developers review and architect.", "GitHub Copilot, Stack Overflow, CI/CD"),
        TimelinePoint(2030, "Intent-driven coding", f"For {specific.lower()}, you describe outcomes; AI generates and tests code.", "Natural-language programming, AI pair programmers", True),
        TimelinePoint(2040, "Software orchestration", "Developers manage AI agent teams building complex systems.", "Multi-agent dev environments", True),
        TimelinePoint(2050, "Human as architect", "People define systems, ethics, and UX; AI handles implementation.", "Autonomous software factories", True),
    )


def _music_piano_timeline(specific: str) -> tuple[TimelinePoint, ...]:
    return (
        TimelinePoint(1980, "Traditional lessons", "Weekly in-person lessons; practice tracked with a metronome and sheet music.", "Acoustic piano, sheet music, metronome"),
        TimelinePoint(1990, "Keyboard technology", "Digital pianos and early sequencers expanded home practice.", "Digital pianos, MIDI, cassette recorders"),
        TimelinePoint(2000, "Online tutorials", "Video lessons and forums democratized piano instruction.", "YouTube, MIDI files, practice software"),
        TimelinePoint(2010, "App-based learning", "Interactive apps gamified practice with instant feedback.", "Tablet apps, smart pianos, Synthesia"),
        TimelinePoint(2020, "AI feedback loops", "Apps listen and correct timing, dynamics, and fingering in real time.", "AI piano coaches, cloud sheet libraries"),
        TimelinePoint(2030, "Adaptive practice", f"For {specific.lower()}, AI designs daily drills targeting your weak spots.", "Haptic feedback, AI repertoire coach", True),
        TimelinePoint(2040, "Immersive performance", "VR concert halls and AI accompaniment partners accelerate mastery.", "VR performance spaces, AI duet partners", True),
        TimelinePoint(2050, "Expressive mastery", "Technical skill is automated; human artistry and emotion define excellence.", "Neural-composer collaboration tools", True),
    )


_AREA_TIMELINES: dict[str, Callable[[str], tuple[TimelinePoint, ...]]] = {
    "researching_information": _research_timeline,
    "basketball": _basketball_timeline,
    "teaching": _teaching_timeline,
    "computer_programming": _programming_timeline,
    "learning_piano": _music_piano_timeline,
}


def _contextual_timeline(domain: str, area: str, specific: str, skill_key: str) -> tuple[TimelinePoint, ...]:
    """Rich area-specific timeline when no bespoke builder exists."""
    area_lower = area.lower()
    templates: dict[str, tuple[tuple[int, str, str, str], ...]] = {
        "learning_math": (
            (1980, "Textbook & chalkboard", "Students worked through problem sets from textbooks with teacher guidance.", "Textbooks, chalkboards, slide rules"),
            (1990, "Calculators in class", "Graphing calculators changed what students could explore in real time.", "Graphing calculators, workbooks"),
            (2000, "Online practice", "Math websites offered unlimited drills and instant checking.", "Online drills, computer algebra systems"),
            (2010, "Adaptive apps", "Khan Academy and apps personalized practice to each learner.", "Tablets, adaptive learning apps"),
            (2020, "AI tutoring", "AI explained steps and adapted difficulty on the fly.", "AI math tutors, interactive whiteboards"),
        ),
        "search_engines": (
            (1980, "Pre-search era", "Finding information meant asking librarians or browsing encyclopedias.", "Encyclopedias, library catalogs"),
            (1990, "Early web directories", "Yahoo and AltaVista organized the growing web by hand.", "Web directories, early crawlers"),
            (2000, "Google revolution", "PageRank made search fast, relevant, and universal.", "Google, Boolean queries, bookmarks"),
            (2010, "Instant answers", "Search boxes predicted queries and answered questions directly.", "Autocomplete, knowledge panels"),
            (2020, "AI overviews", "Search engines began synthesizing answers from multiple sources.", "AI summaries, voice search"),
        ),
        "music_production": (
            (1980, "Tape & analog", "Recording meant expensive studio time and magnetic tape.", "Tape machines, analog mixers, hardware synths"),
            (1990, "DAW emergence", "Digital audio workstations brought multitrack recording to desktops.", "Pro Tools, early DAWs, samplers"),
            (2000, "Home studio boom", "Affordable interfaces and plugins democratized production.", "Home interfaces, VST plugins, MP3"),
            (2010, "Cloud collaboration", "Producers shared stems online and collaborated remotely.", "Cloud DAWs, Splice, streaming beats"),
            (2020, "AI-assisted production", "AI separated stems, suggested chords, and mastered tracks.", "AI mastering, stem separation, co-producers"),
        ),
        "financial_research": (
            (1980, "Paper & phone calls", "Analysts read annual reports and called companies for insights.", "Annual reports, Bloomberg terminals emerging"),
            (1990, "Terminal era", "Bloomberg and Reuters terminals centralized market data.", "Bloomberg, spreadsheets, fax"),
            (2000, "Online data explosion", "Real-time quotes and SEC filings went online.", "Online brokers, Edgar filings, Excel models"),
            (2010, "Big data finance", "Alternative data and quant models transformed research.", "Python, alt data, cloud compute"),
            (2020, "AI market scanning", "AI monitored news, filings, and sentiment 24/7.", "NLP on filings, AI sentiment, auto-summaries"),
        ),
    }

    if skill_key in templates:
        base = templates[skill_key]
    elif "sport" in domain.lower() or domain == "Sports":
        base = (
            (1980, "Eye test era", f"{specific} relied on coach observation and basic stats.", "Stopwatch, notebook, basic video"),
            (1990, "Video review", "Game film became standard for analysis and improvement.", "VHS, stat sheets"),
            (2000, "Spreadsheet stats", "Performance data entered mainstream sports culture.", "Spreadsheets, early tracking"),
            (2010, "Tracking revolution", "Wearables and cameras captured every movement.", "GPS trackers, optical tracking"),
            (2020, "AI performance analysis", "AI tagged plays and recommended training adjustments.", "AI video, wearables, apps"),
        )
    elif domain == "Healthcare":
        base = (
            (1980, "Paper records", f"{specific} relied on paper charts and physician memory.", "Paper charts, basic lab equipment"),
            (1990, "Early digital systems", "Hospitals began digitizing records and lab results.", "Early EMR, lab information systems"),
            (2000, "Evidence-based medicine", "Clinical guidelines and databases guided decisions.", "PubMed, clinical guidelines, EMR"),
            (2010, "Digital health", "Telemedicine and apps connected patients and providers.", "Telehealth, patient portals, EHR"),
            (2020, "AI clinical support", "AI flagged risks and suggested diagnoses for review.", "AI diagnostics, clinical decision support"),
        )
    elif domain == "Music":
        base = (
            (1980, "Analog craft", f"{specific} was learned through teachers, tapes, and repetition.", "Instruments, sheet music, tape recorders"),
            (1990, "Digital tools", "MIDI and digital recording changed practice and production.", "MIDI, early DAWs, CDs"),
            (2000, "Internet learning", "Online tabs, tutorials, and forums spread knowledge.", "Online tabs, MP3, forums"),
            (2010, "Mobile & apps", "Apps made practice interactive and portable.", "Tablet apps, YouTube, smart instruments"),
            (2020, "AI music coaches", "AI gave real-time feedback on technique and composition.", "AI coaches, cloud libraries"),
        )
    elif domain == "Education":
        base = (
            (1980, "Traditional classroom", f"{specific} happened in person with textbooks and lectures.", "Textbooks, chalkboards, grade books"),
            (1990, "Technology enters", "Computers and copiers changed how materials were created.", "PC labs, copiers, early software"),
            (2000, "Internet resources", "Online materials supplemented classroom instruction.", "Websites, email, early LMS"),
            (2010, "Blended learning", "Digital tools integrated into daily teaching and learning.", "Smartboards, cloud docs, tablets"),
            (2020, "Hybrid & AI-assisted", "Remote learning and AI feedback transformed workflows.", "Video classes, AI grading, adaptive tools"),
        )
    else:
        base = (
            (1980, "Manual craft", f"{specific} relied on manual tools, local experts, and slow feedback.", "Paper, in-person mentors, basic tools"),
            (1990, "Early digital", f"Computers began supporting {area.lower()}.", "PC software, fax, early databases"),
            (2000, "Internet era", f"{area} moved online with faster communication and data.", "Email, web apps, spreadsheets"),
            (2010, "Cloud & mobile", "Workflows became portable, collaborative, and always connected.", "Cloud apps, smartphones"),
            (2020, "AI assistance", "AI began drafting, analyzing, and suggesting next steps.", "Copilots, automation, analytics"),
        )

    points = [
        TimelinePoint(year, headline, desc, tools, False)
        for year, headline, desc, tools in base
    ]
    points.extend([
        TimelinePoint(2030, "AI partnership", f"For {specific.lower()}, AI handles routine steps; humans focus on judgment.", "Domain-specific AI agents", True),
        TimelinePoint(2040, "Orchestrated systems", "Humans manage AI teams executing complex workflows.", "Multi-agent workflows", True),
        TimelinePoint(2050, "Human direction", "People define goals and ethics while AI executes at scale.", "Integrated human–AI environments", True),
    ])
    return tuple(points)


def _build_timeline(domain: str, area: str, specific: str, skill_key: str) -> tuple[TimelinePoint, ...]:
    builder = _AREA_TIMELINES.get(skill_key)
    if builder:
        return builder(specific)
    return _contextual_timeline(domain, area, specific, skill_key)


# ── Drivers ─────────────────────────────────────────────────────────────────


def _build_drivers(domain: str, area: str, specific: str) -> tuple[DriverDetail, ...]:
    context = {
        "Technology": {
            "Technology": "From mainframes to smartphones to AI — each wave made this skill faster and more accessible.",
            "Economics": "Cheaper computing shifted value from tool operation to judgment and creativity.",
            "Culture": "Always-on connectivity changed expectations for speed and availability.",
            "AI": "AI now drafts, searches, and synthesizes — reshaping what humans must do themselves.",
            "Automation": "Routine steps automate away; the skill becomes curation and verification.",
        },
        "Education": {
            "Technology": "Classrooms evolved from chalkboards to smartboards to AI-adaptive learning platforms.",
            "Economics": "Budget pressures push schools toward scalable, technology-enhanced instruction.",
            "Culture": "Students expect personalized, on-demand learning like they get from apps and games.",
            "AI": "AI tutors and graders free teachers to focus on motivation and deep explanation.",
            "Automation": "Routine grading and content delivery automate; teaching becomes coaching.",
        },
        "Sports": {
            "Technology": "Video, wearables, and tracking systems turned gut feel into measurable data.",
            "Economics": "Analytics-driven decisions create competitive edges worth millions.",
            "Culture": "Fans and athletes expect data-backed insights and instant highlight breakdowns.",
            "AI": "AI tags film, predicts injuries, and designs personalized training programs.",
            "Automation": "Routine analysis automates; coaches focus on leadership and in-game decisions.",
        },
        "Music": {
            "Technology": "From analog tape to DAWs to AI co-producers — creation tools kept democratizing.",
            "Economics": "Home studios replaced expensive recording; streaming changed revenue models.",
            "Culture": "Social media and platforms made distribution instant but competition fierce.",
            "AI": "AI separates stems, suggests harmonies, and gives real-time performance feedback.",
            "Automation": "Technical production tasks automate; artistry and taste become the differentiator.",
        },
    }
    defaults = {
        "Technology": "New tools continuously lowered barriers and raised output expectations.",
        "Economics": "Cost pressures and market competition reward efficiency and scale.",
        "Culture": "Social norms and expectations around this skill shifted with each generation.",
        "AI": "Artificial intelligence is the latest and most transformative driver of change.",
        "Automation": "Tasks that were manual become automated, shifting human roles upstream.",
    }
    domain_ctx = context.get(domain, {})
    return (
        DriverDetail("Technology", "⚙️", domain_ctx.get("Technology", defaults["Technology"])),
        DriverDetail("Economics", "📊", domain_ctx.get("Economics", defaults["Economics"])),
        DriverDetail("Culture", "🌍", domain_ctx.get("Culture", defaults["Culture"])),
        DriverDetail("AI", "🤖", domain_ctx.get("AI", f"AI is transforming {specific.lower()} faster than any prior technology.")),
        DriverDetail("Automation", "⚡", domain_ctx.get("Automation", f"Automation handles repetitive parts of {specific.lower()}; humans focus on what machines cannot do.")),
    )


# ── Advice ──────────────────────────────────────────────────────────────────


def _advice_for(domain: str, area: str, specific: str, skill_key: str) -> FutureAdvice:
    advice_map: dict[str, FutureAdvice] = {
        "researching_information": FutureAdvice(
            learn=("Source evaluation and bias detection", "Synthesis and argument building", "Prompting research AI effectively"),
            skills_that_matter=("Question design", "Cross-domain linking", "Teaching others what you learned"),
            stop_spending_time_on=("Manual bibliography formatting", "Shallow searching without verification", "Hoarding bookmarks you never read"),
            focus_on=("Deep reading of primary sources", "Building mental models", "Curating trusted source networks"),
            opportunities=("Personal research assistants", "Citizen science at scale", "Lifelong learning on demand"),
            risks=("Echo chambers from personalized feeds", "Fabricated citations", "Information overload paralysis"),
        ),
        "basketball": FutureAdvice(
            learn=("Biomechanics basics", "Data literacy for sports analytics", "How to interpret AI-generated training plans"),
            skills_that_matter=("Game IQ and decision-making", "Leadership and communication", "Adaptability to new training tech"),
            stop_spending_time_on=("Mindless reps without feedback", "Ignoring recovery and injury prevention data", "Arguing with stats you don't understand"),
            focus_on=("Deliberate practice with measurable goals", "Mental performance and visualization", "Building coachable habits"),
            opportunities=("Personalized AI coaching apps", "Analytics roles in sports organizations", "Content creation around skill development"),
            risks=("Over-reliance on metrics over feel", "Injury from ignoring biomechanics alerts", "Comparison culture from constant tracking"),
        ),
        "teaching": FutureAdvice(
            learn=("How adaptive learning platforms work", "AI literacy for educators", "Trauma-informed and inclusive pedagogy"),
            skills_that_matter=("Motivation and relationship-building", "Explaining complex ideas simply", "Designing experiences, not just content"),
            stop_spending_time_on=("Creating worksheets AI can generate", "One-size-fits-all lectures", "Grading routine assignments by hand"),
            focus_on=("Coaching critical thinking", "Ethical use of AI in classrooms", "Human connection and mentorship"),
            opportunities=("Global reach through hybrid teaching", "Curriculum design for AI-augmented learning", "Specialist roles in learning science"),
            risks=("Students skipping deep learning for AI shortcuts", "Equity gaps in AI access", "Teacher burnout from tool overload"),
        ),
        "computer_programming": FutureAdvice(
            learn=("System design and architecture", "AI prompt engineering for code", "Security and testing fundamentals"),
            skills_that_matter=("Problem decomposition", "Code review and quality judgment", "Understanding user needs"),
            stop_spending_time_on=("Boilerplate coding AI handles well", "Memorizing syntax", "Manual debugging of obvious errors"),
            focus_on=("Defining requirements and constraints", "Ethical AI in software", "Building reliable systems humans trust"),
            opportunities=("AI orchestration engineering", "Domain-specific tool building", "Open-source AI tooling"),
            risks=("Shipping AI code without review", "Skill atrophy in fundamentals", "Job displacement for routine coding"),
        ),
        "learning_piano": FutureAdvice(
            learn=("Music theory fundamentals", "How AI feedback tools work", "Expression and performance psychology"),
            skills_that_matter=("Consistent practice habits", "Active listening", "Artistic interpretation"),
            stop_spending_time_on=("Mindless repetition without goals", "Chasing perfect technique over musicality", "Collecting tutorials without practicing"),
            focus_on=("Deliberate practice on weak passages", "Playing with others", "Developing your unique voice"),
            opportunities=("AI-accelerated skill development", "Global online recitals and collaboration", "Composition with AI co-writers"),
            risks=("Relying on AI for expression", "Losing the joy of slow mastery", "Comparison with AI-generated performances"),
        ),
    }
    if skill_key in advice_map:
        return advice_map[skill_key]

    return FutureAdvice(
        learn=(f"Domain fundamentals of {specific.lower()}", "How to verify and guide AI outputs", "Adaptability to new tools in your field"),
        skills_that_matter=("Critical thinking", "Communication and collaboration", "Judgment under uncertainty"),
        stop_spending_time_on=(f"Manual busywork in {specific.lower()} that AI automates", "Memorizing facts retrievable instantly", "Resisting useful new tools"),
        focus_on=(f"Creative and strategic aspects of {specific.lower()}", "Quality control over AI outputs", "Building relationships and trust"),
        opportunities=(f"AI-augmented {area.lower()}", "New hybrid roles combining domain + AI skills", "Reaching more people with less friction"),
        risks=("Over-trusting AI without verification", "Skill atrophy in core fundamentals", "Bias and privacy issues in automated systems"),
    )


# ── Simulation ──────────────────────────────────────────────────────────────


def _build_simulation(domain: str, area: str, specific: str, skill_key: str) -> dict[int, dict[str, str]]:
    sims: dict[str, dict[int, dict[str, str]]] = {
        "researching_information": {
            2030: {
                "tools": "Personal research copilot that proposes sources, flags bias, and drafts synthesis outlines.",
                "work": "You define the question; AI gathers and ranks sources; you verify and write the final argument.",
                "learning": "AI quizzes you on sources you read and suggests gaps in your understanding.",
                "day": "Morning: AI briefing on overnight developments in your topic. Midday: deep read of 3 primary sources AI flagged. Evening: co-write synthesis with AI, you edit for voice and accuracy.",
            },
            2040: {
                "tools": "Expert synthesis panels — multiple AI specialists debate findings; you adjudicate.",
                "work": "Research projects that took weeks now take hours; your role is question design and quality judgment.",
                "learning": "Immersive topic simulations where you explore scenarios and test hypotheses in real time.",
                "day": "30-minute standup with AI research team. Review synthesized report. One hour verifying key claims. Present findings to colleagues.",
            },
            2050: {
                "tools": "Collaborative knowledge environment — instant access to curated, verified expertise on any topic.",
                "work": "Humans set research agendas and ethical boundaries; AI handles discovery and synthesis at scale.",
                "learning": "Learning is embedded in projects — AI teaches exactly what you need, when you need it.",
                "day": "Define tomorrow's research questions over coffee. AI delivers verified briefs by lunch. Afternoon: mentor a student on evaluating AI-generated research.",
            },
        },
        "basketball": {
            2030: {
                "tools": "Real-time biomechanics sensors + AI coaching app that builds daily micro-drills.",
                "work": "Practice plans auto-generated from game film; you execute drills and log how they feel.",
                "learning": "AI breaks down your shooting form frame-by-frame and compares to optimal models.",
                "day": "Morning: 20-min AI-designed warm-up. Team practice with wearable feedback. Evening: review AI-tagged game clips and set tomorrow's focus.",
            },
            2040: {
                "tools": "VR simulator with AI opponents mimicking upcoming team's schemes.",
                "work": "Half your reps happen in VR; live practice focuses on chemistry and decision-making.",
                "learning": "Mental reps via immersive simulation — read defenses and call plays in VR.",
                "day": "VR session: 200 simulated possessions. Live practice: 90 minutes with smart-court tracking. Recovery guided by AI injury-prevention protocol.",
            },
            2050: {
                "tools": "Smart court with continuous AR feedback during play.",
                "work": "In-game AI whispers optimal spacing and matchup alerts through your earpiece.",
                "learning": "Career-long digital twin tracks development from youth to pro.",
                "day": "Game day: real-time analytics overlay during warm-ups. Play with adaptive coaching cues. Post-game: AI-generated development plan for next week.",
            },
        },
    }

    if skill_key in sims:
        return sims[skill_key]

    return {
        2030: {
            "tools": f"AI copilots tuned for {specific.lower()} in {area.lower()}",
            "work": f"You set goals for {specific.lower()}; AI drafts options; you approve and refine.",
            "learning": f"Adaptive lessons for {specific.lower()} based on your mistakes and pace.",
            "day": f"Morning: AI briefing on today's {specific.lower()} priorities. Midday: hands-on practice with AI feedback. Evening: reflection session with AI coach.",
        },
        2040: {
            "tools": f"Multi-agent studio for {specific.lower()}",
            "work": f"You orchestrate AI specialists for {specific.lower()}; focus on strategy and quality.",
            "learning": f"Immersive simulations of {specific.lower()} with instant feedback.",
            "day": f"Short human checkpoints; AI handles prep and first drafts for {specific.lower()}. You review and decide.",
        },
        2050: {
            "tools": "Integrated human–AI environment",
            "work": f"Humans define values and vision for {specific.lower()}; AI executes complex workflows.",
            "learning": f"Continuous micro-learning embedded in every {specific.lower()} project.",
            "day": f"Creative direction and ethical judgment dominate; {specific.lower()} execution is highly automated.",
        },
    }


def build_skill_profile(domain: str, area: str, specific: str) -> SkillProfile:
    skill_key = get_skill_key(domain, area)
    icon = DOMAIN_ICONS.get(domain, "🔮")

    return SkillProfile(
        key=f"{domain}:{area}:{specific}",
        name=specific,
        icon=icon,
        domain=domain,
        area=area,
        timeline=_build_timeline(domain, area, specific, skill_key),
        drivers=_build_drivers(domain, area, specific),
        advice=_advice_for(domain, area, specific, skill_key),
        simulation=_build_simulation(domain, area, specific, skill_key),
    )
