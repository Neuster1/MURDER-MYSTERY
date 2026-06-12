"""
╔══════════════════════════════════════════════════════════╗
║         🔍 THE MANOR HOUSE MYSTERY — STREAMLIT 🔍        ║
║        AI-Generated Mystery · Powered by Gemini          ║
╚══════════════════════════════════════════════════════════╝
Run with:  streamlit run murder_mystery_app.py
"""

import streamlit as st
import json
import random
import time
import threading
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="The Manor House Mystery",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
#  GLOBAL STYLES  (detective noir dark theme)
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Crimson+Text:ital@0;1&family=IM+Fell+English:ital@0;1&display=swap');

/* ── Root palette ── */
:root {
  --bg:        #0d0d0d;
  --surface:   #141414;
  --card:      #1a1a1a;
  --border:    #2e2a24;
  --gold:      #c9a84c;
  --gold-dim:  #8a6e30;
  --red:       #c0392b;
  --red-dim:   #7b241c;
  --cyan:      #4ecdc4;
  --magenta:   #b87ebe;
  --green:     #27ae60;
  --text:      #e8dcc8;
  --text-dim:  #9a8e7a;
  --white:     #f5f0e8;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Typography ── */
h1, h2, h3, h4 {
  font-family: 'Playfair Display', serif !important;
  color: var(--gold) !important;
  letter-spacing: 0.04em;
}
p, li, label, div {
  font-family: 'Crimson Text', serif !important;
  font-size: 1.08rem;
  color: var(--text);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #0a0a0a !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Buttons ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--gold-dim) !important;
  color: var(--gold) !important;
  font-family: 'Playfair Display', serif !important;
  letter-spacing: 0.05em;
  border-radius: 2px !important;
  transition: all 0.2s;
}
.stButton > button:hover {
  background: var(--gold-dim) !important;
  color: #000 !important;
  border-color: var(--gold) !important;
}

/* ── Text input / text area ── */
.stTextInput > div > div > input,
.stTextArea textarea {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  font-family: 'Crimson Text', serif !important;
  border-radius: 2px !important;
}

/* ── Select box ── */
.stSelectbox > div > div {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--card) !important;
  color: var(--gold) !important;
  font-family: 'Playfair Display', serif !important;
  border: 1px solid var(--border) !important;
}
.streamlit-expanderContent {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
}

/* ── Radio ── */
.stRadio label { color: var(--text) !important; }
.stRadio div[role="radiogroup"] > label { font-size: 1rem !important; }

/* ── Checkbox ── */
.stCheckbox label { color: var(--text) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; opacity: 0.5; }

/* ── Metric ── */
[data-testid="stMetricValue"] { color: var(--gold) !important; font-family: 'Playfair Display', serif !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: var(--text-dim) !important; }

/* ── Progress bar ── */
.stProgress > div > div { background: var(--gold) !important; }

/* ── Notification boxes ── */
.stSuccess { background: #0f2e1a !important; border-left: 3px solid var(--green) !important; color: #6fcf97 !important; }
.stWarning { background: #2e2000 !important; border-left: 3px solid var(--gold) !important; color: var(--gold) !important; }
.stError   { background: #2e0f0f !important; border-left: 3px solid var(--red) !important; color: #e57373 !important; }
.stInfo    { background: #0f1e2e !important; border-left: 3px solid var(--cyan) !important; color: var(--cyan) !important; }

/* ══ CUSTOM COMPONENTS ══════════════════════════════ */

/* Detective card */
.det-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold-dim);
  padding: 1.1rem 1.3rem;
  margin: 0.5rem 0;
  font-family: 'Crimson Text', serif;
}

/* Clue card */
.clue-card {
  background: #111108;
  border: 1px solid #3a3520;
  border-left: 4px solid var(--gold);
  padding: 0.9rem 1.2rem;
  margin: 0.4rem 0;
}
.clue-card h4 { color: var(--gold) !important; margin-bottom: 0.3rem; }

/* Contradiction badge */
.badge-contra {
  display: inline-block;
  background: var(--red-dim);
  color: #ff9999;
  border: 1px solid var(--red);
  border-radius: 3px;
  padding: 1px 8px;
  font-size: 0.78rem;
  font-family: monospace;
  letter-spacing: 0.06em;
  margin-left: 6px;
}
.badge-secret {
  display: inline-block;
  background: #2a1030;
  color: var(--magenta);
  border: 1px solid var(--magenta);
  border-radius: 3px;
  padding: 1px 8px;
  font-size: 0.78rem;
  font-family: monospace;
  letter-spacing: 0.06em;
  margin-left: 6px;
}
.badge-truth {
  display: inline-block;
  background: #102a10;
  color: #7fff7f;
  border: 1px solid #27ae60;
  border-radius: 3px;
  padding: 1px 8px;
  font-size: 0.78rem;
  font-family: monospace;
  letter-spacing: 0.06em;
  margin-left: 6px;
}

/* Title banner */
.title-banner {
  text-align: center;
  padding: 2rem 1rem 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.5rem;
}
.title-banner h1 {
  font-size: 2.6rem !important;
  text-shadow: 0 0 18px #c9a84c55;
  margin-bottom: 0.2rem;
}
.title-banner p {
  color: var(--text-dim) !important;
  font-style: italic;
  font-family: 'IM Fell English', serif !important;
}

/* Suspect CHARACTER card */
.suspect-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 3px solid var(--gold-dim);
  padding: 0.8rem;
  margin: 0.4rem 0;
  text-align: center;
  border-radius: 2px;
}
.suspect-card .char-art {
  font-size: 0.68rem;
  line-height: 1.15;
  color: var(--text-dim);
  font-family: monospace !important;
  white-space: pre;
  display: block;
  text-align: left;
  margin: 0.4rem auto;
  width: fit-content;
}
.suspect-card h4 { margin: 0.3rem 0 0.1rem; font-size: 1rem !important; }
.suspect-card p  { margin: 0; font-size: 0.88rem; color: var(--text-dim); }

/* Score HUD */
.score-hud {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  background: #0a0a0a;
  border: 1px solid var(--border);
  padding: 0.5rem 1.2rem;
  border-radius: 2px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.score-hud .item { font-family: 'Playfair Display', serif; }
.score-hud .val  { color: var(--gold); font-size: 1.3rem; font-weight: 700; }
.score-hud .lbl  { color: var(--text-dim); font-size: 0.78rem; display: block; }

/* Accusation drama box */
.drama-box {
  background: #1a0505;
  border: 2px solid var(--red);
  padding: 1.5rem;
  text-align: center;
  margin: 1rem 0;
}
.drama-box h2 { font-size: 1.8rem !important; }

/* hidden truth box */
.truth-box {
  background: #050a05;
  border: 2px solid #27ae60;
  padding: 1.2rem;
  margin: 0.8rem 0;
  position: relative;
}
.truth-box::before {
  content: "◈ HIDDEN TRUTH";
  position: absolute; top: -11px; left: 12px;
  background: #050a05;
  color: #27ae60;
  font-family: monospace;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  padding: 0 6px;
}

/* Manor map */
.manor-map {
  background: #0a0a0a;
  border: 1px solid var(--border);
  padding: 0.8rem 1rem;
  font-family: monospace !important;
  font-size: 0.8rem;
  color: var(--cyan);
  white-space: pre;
  line-height: 1.4;
}

/* Gemini hint box */
.hint-box {
  background: #180e20;
  border: 1px solid #5a3c7a;
  border-left: 4px solid var(--magenta);
  padding: 1rem 1.3rem;
  font-style: italic;
  font-family: 'IM Fell English', serif !important;
  color: var(--magenta);
  margin: 0.6rem 0;
}

/* Notebook entry */
.nb-entry {
  border-left: 2px solid var(--gold-dim);
  padding-left: 0.8rem;
  margin: 0.3rem 0;
  color: var(--text);
}

/* Timer colors */
.timer-red    { color: #e74c3c; font-weight: bold; animation: pulse 1s infinite; }
.timer-yellow { color: #f39c12; }
.timer-green  { color: var(--green); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* Welcome screen cards */
.welcome-opt {
  background: var(--card);
  border: 1px solid var(--border);
  padding: 1.2rem;
  margin: 0.4rem 0;
  cursor: pointer;
}

/* Rating stars */
.rating { font-size: 1.5rem; letter-spacing: 0.1em; }

/* Premade badge */
.premade-badge {
  display: inline-block;
  background: #1a1000;
  color: var(--gold-dim);
  border: 1px solid var(--gold-dim);
  border-radius: 3px;
  padding: 2px 10px;
  font-size: 0.75rem;
  font-family: monospace;
  letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  GEMINI API
# ═══════════════════════════════════════════════════════

def call_gemini_once(prompt: str, api_key: str) -> str | None:
    """Single attempt — no retries. Returns text or None on any error."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9},
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None


def call_gemini(prompt: str, api_key: str) -> str | None:
    """Retrying wrapper used for hints / case reports (UI-visible).
    Capped at 3 retries with a max 15s sleep to avoid blocking the
    Streamlit server thread for minutes on persistent rate limits."""
    max_retries = 3
    wait = 8   # 8s → 16s → give up (max ~24s total block)
    for attempt in range(max_retries):
        result = call_gemini_once(prompt, api_key)
        if result is not None:
            return result
        if attempt < max_retries - 1:
            st.info(f"⏳ Gemini is busy — retrying in {wait}s… (attempt {attempt + 1}/{max_retries})")
            time.sleep(min(wait, 15))   # hard cap: never sleep >15s on server thread
            wait *= 2
    st.error("Gemini is unavailable right now. Please wait a moment and try again.")
    return None


# ═══════════════════════════════════════════════════════
#  PROMPTS
# ═══════════════════════════════════════════════════════

_VICTIM_ROLES = [
    "a disgraced diplomat hiding a double life",
    "a reclusive naturalist with a dangerous secret",
    "a retired naval admiral visiting old enemies",
    "a celebrated opera singer blackmailing half the guests",
    "a fraudulent spiritualist running séances at the manor",
    "a railway magnate whose will was recently forged",
    "a foreign countess dealing in stolen antiquities",
    "a renowned portrait painter who knew too much",
    "a newspaper editor carrying explosive correspondence",
    "a widowed apothecary who controlled the manor's medicines",
]

_SETTING_TWISTS = [
    "during a violent thunderstorm that has cut off all roads",
    "the night before a secret auction of stolen jewels",
    "on the eve of a scandalous public trial",
    "during a masquerade ball where no one admits their true identity",
    "while the manor's owner lies in a mysterious coma upstairs",
    "on the anniversary of a death that was ruled an accident",
    "as a séance is underway in the east wing",
    "the same night a priceless relic goes missing",
    "while a blizzard traps all guests for three days",
    "just hours after a threatening letter was delivered to every guest",
]

_SUSPECT_ARCHETYPES = [
    ["disgraced army surgeon", "embittered governess", "charming foreign diplomat"],
    ["jealous twin sibling", "opium-addicted poet", "scheming solicitor"],
    ["fallen aristocrat", "mysterious veiled widow", "corrupt parish vicar"],
    ["shady antiques dealer", "ambitious lady's companion", "ex-convict valet"],
    ["vengeful former servant", "eccentric astronomer", "cold-eyed insurance broker"],
    ["retired spy posing as a cook", "obsessive taxidermist", "penniless countess"],
    ["theatrical illusionist", "grieving father hiding rage", "blackmailer posing as a journalist"],
    ["disgraced judge", "secretly pregnant heiress", "war-profiteer in disguise"],
    ["radical suffragette", "paranoid cryptographer", "guilt-ridden priest"],
    ["forger posing as an art restorer", "runaway bride", "vengeful chemist"],
]

_MURDER_METHODS = [
    "poisoned claret at the dinner table",
    "a blow to the head disguised as a fall down the stairs",
    "a rigged gas lamp causing suffocation",
    "cyanide in the victim's evening medicine",
    "a crossbow bolt fired through a secret passage",
    "an overdose of laudanum slipped into the victim's tea",
    "strangulation staged to look like a heart seizure",
    "a hidden trapdoor above the cellar stairs",
    "a sharpened letter-opener left in the dark",
    "slow arsenic poisoning over several days",
]

_ART_STYLES = [
    "bold block ASCII using # and = for shading",
    "delicate line art using . and - and | only",
    "silhouette style using solid # blocks",
    "detailed portrait style mixing * . - | / \\ characters",
    "woodcut-style using X O and # patterns",
]


def build_mystery_prompt() -> str:
    victim_role   = random.choice(_VICTIM_ROLES)
    twist         = random.choice(_SETTING_TWISTS)
    archetypes    = random.choice(_SUSPECT_ARCHETYPES)
    method        = random.choice(_MURDER_METHODS)
    art_style     = random.choice(_ART_STYLES)
    seed          = random.randint(1000, 9999)

    archetype_str = "\n".join(f"  - Suspect {i+1}: {a}" for i, a in enumerate(archetypes))

    return f"""You are a creative writer for a murder mystery game.
Generate a completely original murder mystery set in a Victorian manor.
Seed: {seed} — use this to ensure your output is unique and different every time.

SCENARIO SEEDS (you MUST incorporate all of these):
- Victim's role: {victim_role}
- Setting twist: {twist}
- Murder method: {method}
- Suspect archetypes to inspire (adapt freely, give unique names):
{archetype_str}
- ASCII art style: {art_style}

Return ONLY valid JSON — no markdown, no backticks, no explanation.

{{
  "victim": {{
    "name": "Full Name",
    "role": "their role or reason for being at the manor",
    "found": "one sentence describing how/where they were found"
  }},
  "suspects": [
    {{
      "name": "Full Name",
      "description": "one sentence background",
      "alibi": "first-person alibi claim",
      "secret": "first-person hidden motive",
      "contradiction_clue": "exact name of the ONE crime scene clue that disproves their alibi",
      "contradiction_explanation": "2-3 sentences proving they lied",
      "ascii_art": "CRITICAL: A 13-line ASCII portrait of THIS SPECIFIC CHARACTER in {art_style}. Use \\n between lines. Safe chars only: letters digits spaces . , - _ | / \\ ( ) [ ] * + = # @ ! ? ~ ^ ' Each line max 24 chars wide. This portrait MUST visually reflect who this character IS — their unique costume, prop, and silhouette. Examples: a surgeon has a medical bag and coat; a widow has a long veil (~~~); a vicar has a collar and cross (+); a valet stands rigid with a tray; a poet is dishevelled with a quill; a spy looks ordinary but hides a knife. NO two suspects may look alike. NO generic faces. NO backticks, NO markdown — raw flat string only."
    }}
  ],
  "crime_scene_clues": [
    {{
      "name": "short clue name",
      "detail": "2-3 sentences of detective observations",
      "contradicts_suspect": "suspect name or null"
    }}
  ],
  "manor_clues": [
    {{
      "location": "use one of: library, kitchen, cellar, garden, guest bedroom",
      "text": "one sentence of what is found there"
    }}
  ],
  "hidden_truths": [
    {{
      "id": "truth_1",
      "title": "Short cryptic title",
      "trigger_keyword": "a single rare Victorian-era word the player must type",
      "description": "2 sentences of an extremely subtle hidden detail implicating the real killer"
    }},
    {{
      "id": "truth_2",
      "title": "Another cryptic title",
      "trigger_keyword": "another single rare trigger word, different from truth_1",
      "description": "Another hidden truth, different angle, equally obscure"
    }}
  ]
}}

Rules:
- Exactly 3 suspects — all named differently, all visually and narratively distinct
- Each suspect's contradiction_clue must exactly match a name in crime_scene_clues
- Exactly 5 crime_scene_clues (3 contradict one suspect each, 2 are general evidence)
- Exactly 5 manor_clues using these locations: library, kitchen, cellar, garden, guest bedroom
- Exactly 2 hidden_truths — each trigger_keyword is a single unusual word unlikely to be guessed
- ascii_art for each suspect MUST be a flat string with literal \\n separators, not a JSON array
- Each suspect's ascii_art MUST look completely different from the others — unique silhouette, unique props
- Do NOT reveal who the murderer is
"""

def hint_prompt(victim, suspects, suspect_data, scene_clues_found, manor_clues_found, murderer):
    known_scene = scene_clues_found or ["none"]
    known_manor = manor_clues_found or ["none"]
    exposed     = [n for n, d in suspect_data.items() if d["contradiction"]["found"]]
    return f"""
You are a mysterious Victorian narrator in a murder mystery game.
Victim: {victim['name']}. Suspects: {', '.join(suspects)}.
Crime scene clues found: {', '.join(known_scene)}.
Manor clues found: {', '.join(known_manor)}.
Alibis disproven: {', '.join(exposed) if exposed else 'none'}.
The murderer is {murderer} — do NOT say this directly.
Give ONE cryptic 2-3 sentence hint in gothic Victorian narrator style.
"""

def case_report_prompt(victim, suspects, suspect_data, murderer,
                        scene_clues_found, manor_clues_found, score, won,
                        truths_found=None):
    exposed = [n for n, d in suspect_data.items() if d["contradiction"]["found"]]
    secrets = [f"{n}: {d['secret']}" for n, d in suspect_data.items() if d["secret_revealed"]]
    truths_str = f"Hidden truths uncovered: {', '.join(truths_found)}" if truths_found else "No hidden truths found."
    return f"""
Write a short dramatic Victorian-style official case report for a murder mystery.

Victim: {victim['name']} ({victim['role']})
Murderer: {murderer}
Motive: {suspect_data[murderer]['secret']}
Solved: {'YES' if won else 'NO — killer escaped'}
Contradictions exposed: {', '.join(exposed) if exposed else 'none'}
Secrets uncovered: {'; '.join(secrets) if secrets else 'none'}
{truths_str}
Final score: {score} pts

Write as an official case file signed by Detective Sterling.
Dramatic and atmospheric. 3-4 short paragraphs max.
"""


# ═══════════════════════════════════════════════════════
#  MYSTERY PARSER  (shared by Gemini + premade loader)
# ═══════════════════════════════════════════════════════

def parse_mystery_data(data: dict):
    """Turn a raw mystery dict into the 6-tuple the game expects."""
    v      = data["victim"]
    victim = {"name": v["name"], "role": v["role"], "found": v["found"]}

    suspects     = [s["name"] for s in data["suspects"]]
    suspect_data = {}
    for s in data["suspects"]:
        raw_art = s.get("ascii_art", "")
        if isinstance(raw_art, list):
            raw_art = "\n".join(raw_art)
        art = sanitize_ascii_art(raw_art)
        suspect_data[s["name"]] = {
            "description":     s["description"],
            "alibi":           s["alibi"],
            "secret":          s["secret"],
            "secret_revealed": False,
            "ascii_art":       art,
            "contradiction": {
                "clue_needed":  s["contradiction_clue"],
                "explanation":  s["contradiction_explanation"],
                "found":        False,
            },
        }

    scene_clues = [
        {
            "name":                  cl["name"],
            "detail":                cl["detail"],
            "unlocks_contradiction": cl.get("contradicts_suspect"),
        }
        for cl in data["crime_scene_clues"]
    ]

    crime_scene = {
        "name": "The Study",
        "description": (
            f"The study is dimly lit, thick with old books and something bitter. "
            f"{victim['name']} — {victim['role']} — is {victim['found']}. "
            f"A cold draught slips through the ajar window. "
            f"A portrait on the wall watches everything in silence."
        ),
        "clues": scene_clues,
    }

    manor_clues  = [{"location": m["location"], "text": m["text"]} for m in data["manor_clues"]]
    hidden_truths = []
    for ht in data.get("hidden_truths", []):
        hidden_truths.append({
            "id":              ht["id"],
            "title":           ht["title"],
            "trigger_keyword": ht["trigger_keyword"].strip().lower(),
            "description":     ht["description"],
            "found":           False,
        })

    return victim, suspects, suspect_data, crime_scene, manor_clues, hidden_truths


def parse_gemini_raw(raw: str):
    """Strip fences and JSON-parse a Gemini response, then call parse_mystery_data."""
    if raw is None:
        return None
    raw = raw.strip()
    for fence in ["```json", "```"]:
        if raw.startswith(fence):
            raw = raw[len(fence):]
    if raw.endswith("```"):
        raw = raw[:-3]
    try:
        data = json.loads(raw.strip())
    except json.JSONDecodeError:
        return None
    return parse_mystery_data(data)


# ═══════════════════════════════════════════════════════
#  PREMADE MYSTERIES  (3 fully hand-crafted)
# ═══════════════════════════════════════════════════════

_PREMADE_MYSTERIES = [
    # ── MYSTERY 1: The Poisoned Claret ──────────────────
    {
        "victim": {
            "name": "Lord Edmund Ashford",
            "role": "a railway magnate whose will was recently forged",
            "found": "slumped in his leather chair, an overturned glass of claret pooling dark across the Persian rug"
        },
        "suspects": [
            {
                "name": "Dr. Helena Voss",
                "description": "A disgraced army surgeon dismissed for stealing morphine from field hospitals.",
                "alibi": "I was in the east wing dispensary all evening, cataloguing medicines for Lord Ashford's ailing wife.",
                "secret": "I forged the will myself — Ashford promised me his estate in exchange for keeping his wife sedated and compliant.",
                "contradiction_clue": "Empty Morphine Phial",
                "contradiction_explanation": "The dispensary log shows no medicines were checked out that evening. The empty morphine phial found near the body matches Dr. Voss's personal medical kit, monogrammed H.V. — she was never in the east wing.",
                "ascii_art": "    .---.\n   ( o o )\n    | - |\n   _|___|_\n  / [bag] \\\n |  -----  |\n |  | H |  |\n  \\_______/\n    |   |\n   /|   |\\\n  / |   | \\\n /___|___\\"
            },
            {
                "name": "Mr. Silas Crane",
                "description": "A scheming solicitor who drafted three versions of Lord Ashford's will in as many months.",
                "alibi": "I retired to the library directly after supper to review the estate documents. The butler saw me there.",
                "secret": "I stand to collect a 40% commission if the forged will is executed — Voss and I arranged the entire scheme.",
                "contradiction_clue": "Muddy Boot Prints",
                "contradiction_explanation": "A trail of fresh mud leads from the garden door to the study — the library is in the opposite wing. The boot prints match Crane's distinctive square-toed shoes, proving he came from outside, not the library.",
                "ascii_art": "   _______\n  |  ___  |\n  | |   | |\n  | |___| |\n   \\  =  /\n   /-----\\\n  | suit  |\n  |=======|\n  |  | |  |\n  |  | |  |\n /|  | |  |\\"
            },
            {
                "name": "Lady Constance Morrow",
                "description": "A mysterious veiled widow and distant relation of Lord Ashford, arrived uninvited three days prior.",
                "alibi": "I was playing the pianoforte in the drawing room the entire evening — three guests can confirm this.",
                "secret": "I am not a widow at all — I am Ashford's first wife, thought dead, returning to reclaim my inheritance before the forged will could disinherit me entirely.",
                "contradiction_clue": "Torn Veil Fabric",
                "contradiction_explanation": "A fragment of black veil caught on the study door's iron latch matches Lady Morrow's veil precisely. The pianoforte bench was cold when checked — she had not played in hours.",
                "ascii_art": "   _____\n  /~~~~~\\\n |  veil |\n  \\~~~~~/ \n   | o o |\n   | --- |\n  /-------\\\n | gown   |\n |=========|\n  \\       /\n   |     |\n   |_____|"
            }
        ],
        "crime_scene_clues": [
            {
                "name": "Empty Morphine Phial",
                "detail": "A small glass phial, still faintly reeking of morphine solution, has rolled beneath the writing desk. The initials H.V. are engraved on its silver cap. It is warm — recently handled.",
                "contradicts_suspect": "Dr. Helena Voss"
            },
            {
                "name": "Muddy Boot Prints",
                "detail": "Two clear boot impressions press into the edge of the study carpet near the garden-facing window. The prints are square-toed, size ten, and still damp with garden soil mixed with greenhouse clay.",
                "contradicts_suspect": "Mr. Silas Crane"
            },
            {
                "name": "Torn Veil Fabric",
                "detail": "A small triangular scrap of fine black silk clings to the iron latch of the study door, caught at roughly shoulder height. The weave is French — expensive, uncommon, and distinctive.",
                "contradicts_suspect": "Lady Constance Morrow"
            },
            {
                "name": "Overturned Claret Glass",
                "detail": "The glass lies on its side, the claret fully absorbed into the rug. A faint crystalline residue coats the inside of the rim — consistent with a dissolved powder, not wine sediment.",
                "contradicts_suspect": None
            },
            {
                "name": "Unsigned Letter",
                "detail": "Half-burnt in the fireplace grate, a letter reads: '…destroy the original document before Thursday or our arrangement expires and I will not be held responsible for what follows.' The handwriting is neat, educated, and deliberately disguised.",
                "contradicts_suspect": None
            }
        ],
        "manor_clues": [
            {"location": "library", "text": "The estate documents on the reading table are a forgery — the ink dates to only six weeks ago, yet the will purports to be five years old."},
            {"location": "kitchen", "text": "Cook reports that a bottle of Lord Ashford's private claret was taken from the kitchen by 'the doctor' shortly before the dinner bell."},
            {"location": "cellar", "text": "Behind a false wine rack, a lockbox contains a second, authentic version of Lord Ashford's will — leaving everything to a charitable hospital in Edinburgh."},
            {"location": "garden", "text": "Near the greenhouse door, a square-toed boot print is pressed deep into the mud, alongside drag marks suggesting a heavy bag was carried toward the manor."},
            {"location": "guest bedroom", "text": "In the guest room assigned to Lady Morrow, a hidden compartment beneath the floorboards contains a marriage certificate — dated 1871, naming her as Edmund Ashford's lawful wife."}
        ],
        "hidden_truths": [
            {
                "id": "truth_1",
                "title": "The Confederacy of Three",
                "trigger_keyword": "laudanum",
                "description": "All three suspects were in league — Voss supplied the poison, Crane forged the paperwork, and Morrow was meant to inherit and split the estate three ways. The murder was never part of the plan; Ashford discovered the forged will and threatened to expose them all that very evening."
            },
            {
                "id": "truth_2",
                "title": "The Edinburgh Heir",
                "trigger_keyword": "codicil",
                "description": "The charitable hospital named in the original will is a front — its sole benefactor and administrator is Ashford's illegitimate son, kept secret for thirty years. The conspirators knew nothing of him, and he knows nothing of the murder."
            }
        ]
    },

    # ── MYSTERY 2: The Masquerade ────────────────────────
    {
        "victim": {
            "name": "Countess Irina Volkov",
            "role": "a foreign countess dealing in stolen antiquities",
            "found": "face-down on the ballroom floor behind a marble pillar, still wearing her swan mask, a single stiletto wound between her shoulder blades"
        },
        "suspects": [
            {
                "name": "Professor Aldous Fenn",
                "description": "An obsessive taxidermist and amateur antiquarian who corresponded with the Countess for years regarding a stolen Byzantine icon.",
                "alibi": "I spent the entire masquerade in the smoking room — half a dozen gentlemen will confirm I never once entered the ballroom.",
                "secret": "The icon she was selling was stolen from my private collection five years ago. I had come to retrieve it by any means necessary.",
                "contradiction_clue": "Swan Feather Clutched in Hand",
                "contradiction_explanation": "A white swan feather — identical to those on the victim's mask — was found clenched in the victim's fist, torn free in a struggle. Fenn's tailcoat carries three pinprick punctures on the left lapel consistent with swan feather quills, proving close physical contact.",
                "ascii_art": "   .----.\n  ( o  . )\n  |  __  |\n  \\_|##|_/\n  /------\\\n | COAT  |\n |[icon] |\n  \\------/\n   || ||\n   || ||\n  /||_||\\  \n /____|___\\"
            },
            {
                "name": "Miss Odette Flair",
                "description": "A theatrical illusionist performing at the masquerade, rumoured to be the Countess's former accomplice in the antiquities trade.",
                "alibi": "I was performing my illusion act on the main stage from ten until midnight — three hundred guests watched me the entire time.",
                "secret": "I owed the Countess a debt of silence — she knew I had helped smuggle a dozen icons into England. When she threatened to expose me unless I paid, I decided the debt must be settled differently.",
                "contradiction_clue": "Powder-Burned Glove",
                "contradiction_explanation": "A white evening glove found behind the pillar carries a faint scorch mark consistent with a hidden-blade mechanism discharge. The glove is size five — Miss Flair's size — and bears traces of her signature violet perfume.",
                "ascii_art": "   *   *   *\n  * illusion*\n   *  ___  *\n    /o   o\\\n   | smile |\n    \\-----/\n   /=======\\\n  | cape   |\n  |~*~*~*~|\n   \\-------/\n    |     |\n    | | | |"
            },
            {
                "name": "Baron Gregor Halst",
                "description": "A war-profiteer in disguise attending the masquerade under a false name, seeking to purchase the icon for a private buyer.",
                "alibi": "I was at the card table in the library annex all night — I barely knew the woman by sight.",
                "secret": "My buyer offered forty thousand pounds for that icon. When the Countess raised the price at the last moment, I panicked. I followed her onto the ballroom floor during the midnight waltz.",
                "contradiction_clue": "Torn Masquerade Ticket",
                "contradiction_explanation": "The Countess's masquerade ticket was found torn in her evening bag — the matching stub belongs to the Baron's assumed alias. Ticket stubs were only exchanged during the midnight waltz, placing him in the ballroom at the exact moment of death.",
                "ascii_art": "  _________\n |  BARON  |\n  \\  o o  /\n   | === |\n   |thick|\n  /-------\\\n | heavy  |\n | coat   |\n |=======|\n  |     |\n  |  |  |\n  |__|__|"
            }
        ],
        "crime_scene_clues": [
            {
                "name": "Swan Feather Clutched in Hand",
                "detail": "Three white swan feathers are crushed in the victim's right hand, clearly torn from an attacker's clothing or mask during a final struggle. The quills are still moist.",
                "contradicts_suspect": "Professor Aldous Fenn"
            },
            {
                "name": "Powder-Burned Glove",
                "detail": "A pristine white evening glove, size five, lies beneath the victim. A circular scorch mark on the palm — roughly one inch in diameter — is consistent with a spring-loaded mechanism. Violet perfume clings to the silk.",
                "contradicts_suspect": "Miss Odette Flair"
            },
            {
                "name": "Torn Masquerade Ticket",
                "detail": "The victim's evening bag contains her admission ticket, torn cleanly in half. The serial number on the stub is registered to a 'Mr. Valentin Grey' — an alias with no prior record — who purchased his ticket three days before the event.",
                "contradicts_suspect": "Baron Gregor Halst"
            },
            {
                "name": "The Byzantine Icon",
                "detail": "Tucked inside the victim's corset is a small painted icon on gilded wood — Byzantine, 11th century, and flagged as stolen in Interpol's 1889 circular. It was not taken by the killer, suggesting the murder was committed in haste.",
                "contradicts_suspect": None
            },
            {
                "name": "Shattered Champagne Flute",
                "detail": "Directly beneath the victim, a champagne flute lies in pieces. The stem has been snapped cleanly — consistent with someone gripping it tightly while falling or struggling — rather than dropping it.",
                "contradicts_suspect": None
            }
        ],
        "manor_clues": [
            {"location": "library", "text": "A rolled letter in the library fireplace, retrieved mostly intact, details a transaction for one Byzantine icon at a price of thirty thousand pounds — with a postscript demanding an additional ten thousand by midnight."},
            {"location": "kitchen", "text": "A kitchen maid overheard two guests arguing in French near the servants' corridor around eleven o'clock — one voice female and imperious, one male and desperate."},
            {"location": "cellar", "text": "In the wine cellar, a false-bottomed crate contains packing straw sized precisely for a small icon — and a shipping label addressed to a private collector in Vienna."},
            {"location": "garden", "text": "A size-twelve boot has crushed the rosebushes beneath the ballroom window; the window latch shows fresh scratch marks as though someone forced it from outside."},
            {"location": "guest bedroom", "text": "The room registered to 'Mr. Valentin Grey' contains military uniform insignia hidden beneath civilian clothes, and a letter of credit drawn on a Berlin bank for forty thousand pounds."}
        ],
        "hidden_truths": [
            {
                "id": "truth_1",
                "title": "The Midnight Commission",
                "trigger_keyword": "chrysobull",
                "description": "The icon was never truly for sale — the Countess was commissioned by the Russian Imperial court to recover it quietly. Her murder will trigger a diplomatic incident that three governments are now racing to suppress."
            },
            {
                "id": "truth_2",
                "title": "The Violet Thread",
                "trigger_keyword": "escapology",
                "description": "Miss Flair's alibi of being on stage is genuine — but her stage double, a trained escapologist in identical costume, was not. The two women have been switching places during performances for two years."
            }
        ]
    },

    # ── MYSTERY 3: The Séance ─────────────────────────────
    {
        "victim": {
            "name": "Madame Zelda Pryce",
            "role": "a fraudulent spiritualist running séances at the manor",
            "found": "collapsed at the head of the séance table, her expression locked in apparent terror, the candles still burning around her"
        },
        "suspects": [
            {
                "name": "Reverend Caspian Mole",
                "description": "A guilt-ridden parish priest attending the séance to expose Madame Pryce as a charlatan and defend his congregation's faith.",
                "alibi": "I was seated directly opposite Madame Pryce and never left my chair from the moment the séance began until the screaming stopped.",
                "secret": "I paid Pryce to fake a message from my deceased sister last year — she then blackmailed me with the recording she had secretly made. I came tonight to destroy that cylinder.",
                "contradiction_clue": "Broken Phonograph Cylinder",
                "contradiction_explanation": "A shattered phonograph cylinder was found trampled beneath the Reverend's chair — the fragments still play a fragment of his voice confessing to embezzlement. He lied about never leaving his seat; he had to have stood to reach the hidden phonograph cabinet behind him.",
                "ascii_art": "    _____\n   /cross\\\n  | +   + |\n  |collar |\n  /-------\\\n | black  |\n | robes  |\n |=======|\n  |     |\n  | | | |\n  | | | |\n /__|_|__\\"
            },
            {
                "name": "Mrs. Agatha Spool",
                "description": "An ambitious lady's companion who has spent three years manoeuvring to inherit her employer's estate through spiritual manipulation.",
                "alibi": "I was holding the hand of Colonel Marsh to my left throughout — he will confirm I never released my grip.",
                "secret": "I am Pryce's business partner. But when Pryce threatened to expose the entire scheme to my employer tonight, I laced the ritual incense with a concentrated belladonna extract.",
                "contradiction_clue": "Belladonna Residue in Incense Burner",
                "contradiction_explanation": "Chemical analysis of the incense burner ash reveals a concentrated belladonna extract — odourless when burned but lethal at close range. Mrs. Spool alone prepared the incense that evening; the other guests confirm they watched her do so before the séance.",
                "ascii_art": "   .-----.\n  / o   o \\\n | pursed  |\n  \\  ___  /\n  /-------\\\n | high   |\n | collar |\n |_______|\n  |     |\n  | | | |\n  |_|_|_|"
            },
            {
                "name": "Mr. Dorian Quelch",
                "description": "A paranoid cryptographer who believed Madame Pryce had decoded a cipher hidden in his late father's estate documents.",
                "alibi": "I sat at the far end of the table and did not move — I was too frightened to participate actively.",
                "secret": "My father's cipher conceals the location of a cache of stolen government bonds. Pryce had nearly decoded it and was preparing to sell the information. I had to stop her tonight.",
                "contradiction_clue": "Cipher Page Torn from Estate Documents",
                "contradiction_explanation": "A torn page matching Quelch's father's estate documents was found inside Madame Pryce's hidden cabinet — but the matching torn edge was found in Quelch's own waistcoat pocket, proving he had handled the document and been inside the cabinet.",
                "ascii_art": "   ______\n  /  ??  \\\n | eyes   |\n | dart   |\n  \\------/\n  /papers\\\n | codes  |\n |=======|\n  |     |\n  | | | |\n  | | | |\n  |_|_|_|"
            }
        ],
        "crime_scene_clues": [
            {
                "name": "Broken Phonograph Cylinder",
                "detail": "A wax phonograph cylinder in several pieces lies beneath one of the chairs. A surviving fragment, when carefully rotated by hand, emits a tinny but recognisable male voice speaking of financial impropriety. The cabinet it came from shows fresh scratch marks on the lock.",
                "contradicts_suspect": "Reverend Caspian Mole"
            },
            {
                "name": "Belladonna Residue in Incense Burner",
                "detail": "The ornate incense burner at the table's centre contains ash laced with a fine crystalline residue. The scent — beneath the frankincense — is faintly sweet in a way that experienced apothecaries associate with belladonna extract at lethal concentration.",
                "contradicts_suspect": "Mrs. Agatha Spool"
            },
            {
                "name": "Cipher Page Torn from Estate Documents",
                "detail": "Inside Madame Pryce's hidden cabinet beneath the table, a torn page of dense cipher text is tucked into a velvet folder. The tear is clean and recent, and microscopic paper fibres along the edge are still loosely attached.",
                "contradicts_suspect": "Mr. Dorian Quelch"
            },
            {
                "name": "Madame Pryce's Notebook",
                "detail": "A leather-bound notebook hidden inside the séance table's false base records names, dates, and payments — a meticulous record of every piece of blackmail material Pryce had accumulated over seven years.",
                "contradicts_suspect": None
            },
            {
                "name": "The Terror Expression",
                "detail": "The attending physician notes that Madame Pryce's expression — pupils massively dilated, jaw rigid — is not consistent with simple cardiac arrest. The dilation pattern and muscle contraction suggest an anticholinergic toxin administered by inhalation.",
                "contradicts_suspect": None
            }
        ],
        "manor_clues": [
            {"location": "library", "text": "A shelf of spiritualist texts has been recently disturbed; behind them, a concealed portfolio contains blackmail photographs of at least a dozen local families."},
            {"location": "kitchen", "text": "The cook found a small glass vial — empty, no label — wedged behind the spice rack; it smells faintly of almonds and something else, sweeter and more unsettling."},
            {"location": "cellar", "text": "A locked trunk in the cellar contains a portable phonograph, a collection of pre-recorded wax cylinders labelled with guests' names, and a receipt for their manufacture."},
            {"location": "garden", "text": "Pressed into the soft earth near the séance room's exterior window, a heel print sits alone — someone stood here for some time, listening through the glass."},
            {"location": "guest bedroom", "text": "In Mrs. Spool's room, a small wooden box contains a vial of commercially prepared belladonna extract, a recipe for incense blending, and a first-class train ticket departing the following morning."}
        ],
        "hidden_truths": [
            {
                "id": "truth_1",
                "title": "The Seventh Victim",
                "trigger_keyword": "ectoplasm",
                "description": "Madame Pryce had staged a victim's death at a séance three years prior — a wealthy widow who had since been declared legally dead, her estate absorbed. The widow is alive, living under a false name, and was present at the manor that very night as a servant."
            },
            {
                "id": "truth_2",
                "title": "The Bond Cache",
                "trigger_keyword": "steganography",
                "description": "Quelch's father's cipher does not conceal stolen bonds — it conceals the identity of a sitting Cabinet minister who arranged for the bonds to be stolen in the first place. The minister has been aware of Quelch's investigation for six months."
            }
        ]
    },
]


def load_premade_mystery(index: int):
    """Load one of the 3 hand-crafted mysteries and return the 6-tuple."""
    data = _PREMADE_MYSTERIES[index % len(_PREMADE_MYSTERIES)]
    return parse_mystery_data(data)


# ═══════════════════════════════════════════════════════
#  CHARACTER ART
# ═══════════════════════════════════════════════════════

_FALLBACK_ART = [
    (
        "    .----. \n"
        "   / o  o \\\n"
        "  |  \\__/  |\n"
        "  |~~~~~~~~|\n"
        "  /        \\\n"
        " /  [    ]  \\\n"
        "|    |  |    |\n"
        "     |  |\n"
        "    /|  |\\\n"
        "   /_|  |_\\"
    ),
    (
        "    _____\n"
        "   / ^ ^ \\\n"
        "  |  ---  |\n"
        "  |=======|\n"
        "  /       \\\n"
        " / [=====] \\\n"
        "|   |   |   |\n"
        "    |   |\n"
        "   _|   |_\n"
        "  |_|   |_|"
    ),
    (
        "   ______\n"
        "  / 0  0 \\\n"
        " |  ~~~~  |\n"
        " | ______ |\n"
        "  \\      /\n"
        "  |      |\n"
        "  | |  | |\n"
        "  | |  | |\n"
        " /| |  | |\\\n"
        "/_|_|__|_|\\"
    ),
]

_UNSAFE_CHARS = set('<>&"')

def sanitize_ascii_art(raw: str) -> str:
    if not raw:
        return ""
    for fence in ["```ascii", "```\n", "```"]:
        raw = raw.replace(fence, "")
    raw = raw.strip()
    if "\\n" in raw:
        raw = raw.replace("\\n", "\n")
    raw = "".join(c for c in raw if c not in _UNSAFE_CHARS)
    lines = raw.split("\n")
    lines = [ln[:24] for ln in lines[:15]]
    result = "\n".join(lines).strip()
    if len(result.replace("\n", "").strip()) < 5:
        return ""
    return result


def get_suspect_art(name: str, index: int) -> str:
    art = ss.suspect_data.get(name, {}).get("ascii_art", "")
    if art:
        return art
    return _FALLBACK_ART[index % len(_FALLBACK_ART)]


# ═══════════════════════════════════════════════════════
#  MANOR MAP
# ═══════════════════════════════════════════════════════

MANOR_MAP_TEMPLATE = """\
  ┌─────────────┬──────────────┬─────────────┐
  │             │              │             │
  │   LIBRARY   │    STUDY     │   KITCHEN   │
  │    {lib}    │   {stu}  ★   │    {kit}    │
  │             │  [CRIME SCN] │             │
  ├─────────────┼──────────────┼─────────────┤
  │             │              │             │
  │   CELLAR    │    GARDEN    │  GUEST BED  │
  │    {cel}    │    {gar}     │    {bed}    │
  │             │              │             │
  └─────────────┴──────────────┴─────────────┘
         ★ = Crime Scene   ✓ = Searched"""

LOCATION_MAP = {
    "library":       "lib",
    "kitchen":       "kit",
    "cellar":        "cel",
    "garden":        "gar",
    "guest":         "bed",
    "bedroom":       "bed",
    "guest bedroom": "bed",
}


def render_manor_map(manor_clues_found):
    slots = {k: "   " for k in ["lib", "kit", "cel", "gar", "bed", "stu"]}
    for loc in manor_clues_found:
        for keyword, slot in LOCATION_MAP.items():
            if keyword in loc.lower():
                slots[slot] = " ✓ "
                break
    return MANOR_MAP_TEMPLATE.format(**slots)


# ═══════════════════════════════════════════════════════
#  BACKGROUND GEMINI PREFETCH
#  Uses a module-level dict as a simple cross-rerun store
#  (Streamlit re-imports the module each run but the
#   module-level dict persists within the same process)
# ═══════════════════════════════════════════════════════

import sys as _sys

# We stash state in the module object so it survives reruns
_mod = _sys.modules[__name__]
if not hasattr(_mod, "_bg_state"):
    _mod._bg_state = {
        "queue":    [],          # list of parsed mystery tuples ready to play
        "fetching": False,       # True while a background thread is running
        "thread":   None,
    }

_bg = _mod._bg_state


def _bg_fetch_worker(api_key: str, n: int):
    """Background thread: generate n mysteries and push them to _bg['queue']."""
    for _ in range(n):
        raw = call_gemini_once(build_mystery_prompt(), api_key)
        result = parse_gemini_raw(raw)
        if result:
            _bg["queue"].append(result)
    _bg["fetching"] = False


def start_bg_fetch(api_key: str, n: int = 2):
    """Kick off background generation of n mysteries if not already running."""
    if _bg["fetching"]:
        return
    if not api_key.strip():
        return
    _bg["fetching"] = True
    t = threading.Thread(target=_bg_fetch_worker, args=(api_key, n), daemon=True)
    _bg["thread"] = t
    t.start()


def pop_bg_mystery():
    """Return and remove the first queued mystery, or None."""
    if _bg["queue"]:
        return _bg["queue"].pop(0)
    return None


def bg_queue_size() -> int:
    return len(_bg["queue"])


# ═══════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═══════════════════════════════════════════════════════

def init_state():
    defaults = {
        "phase":              "welcome",
        "api_key":            "",
        "timer_mode":         False,
        "timer_seconds":      300,
        "timer_start":        None,
        "hidden_truth_mode":  False,
        "victim":             None,
        "suspects":           [],
        "suspect_data":       {},
        "crime_scene":        None,
        "manor_clues":        [],
        "hidden_truths":      [],
        "murderer":           None,
        "scene_clues_found":  [],
        "manor_clues_found":  [],
        "truths_found":       [],
        "score":              0,
        "game_log":           [],
        "won":                None,
        "end_reason":         None,   # "correct" | "wrong" | "timeout"
        "case_report":        None,
        "last_hint":          None,
        "truth_input":        "",
        "is_premade":         False,
        "premade_index":      0,
        "last_interrogated":  None,   # tracks which suspect was last interrogated
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
ss = st.session_state


# ═══════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════

def add_log(msg: str, kind: str = "info"):
    ss.game_log.append({"msg": msg, "kind": kind})


def points(amount: int, reason: str = ""):
    ss.score += amount
    sign = "+" if amount >= 0 else ""
    col  = "green" if amount >= 0 else "red"
    add_log(f":{col}[{sign}{amount} pts — {reason}]", "pts")


def total_clues():
    return len(ss.scene_clues_found) + len(ss.manor_clues_found)


def time_remaining() -> int | None:
    if not ss.timer_mode or ss.timer_start is None:
        return None
    elapsed = int(time.time() - ss.timer_start)
    return max(0, ss.timer_seconds - elapsed)


def timer_expired() -> bool:
    r = time_remaining()
    return r is not None and r == 0


def fmt_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def score_rating(score: int) -> str:
    if score >= 200:
        return "★★★  Grand Master Detective"
    if score >= 150:
        return "★★★  Master Detective"
    if score >= 80:
        return "★★☆  Skilled Investigator"
    return "★☆☆  Needs More Practice"


def _apply_mystery(result, is_premade: bool):
    """Load a parsed mystery tuple into session state and start the game."""
    victim, suspects, suspect_data, crime_scene, manor_clues, hidden_truths = result
    ss.victim        = victim
    ss.suspects      = suspects
    ss.suspect_data  = suspect_data
    ss.crime_scene   = crime_scene
    ss.manor_clues   = manor_clues
    ss.hidden_truths = hidden_truths if ss.hidden_truth_mode else []
    ss.murderer      = random.choice(suspects)
    ss.timer_start   = time.time() if ss.timer_mode else None
    ss.phase         = "playing"
    ss.is_premade    = is_premade
    add_log("🔍 Investigation opened.", "info")


# ═══════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🔍 Detective's Case File")
        st.markdown("---")

        if ss.phase == "playing":
            st.markdown(f"### ⭐ Score: `{ss.score} pts`")

            rem = time_remaining()
            if rem is not None:
                if rem <= 60:
                    css = "timer-red"
                elif rem <= 120:
                    css = "timer-yellow"
                else:
                    css = "timer-green"
                st.markdown(
                    f'<p class="{css}">⏱ {fmt_time(rem)} remaining</p>',
                    unsafe_allow_html=True,
                )
            elif ss.timer_mode:
                st.markdown("⏱ Time's up!")

            st.markdown("---")
            tc = total_clues()
            st.markdown(f"**📋 Clues Gathered:** {tc}")
            st.progress(min(tc / 10, 1.0))

            st.markdown("---")
            st.markdown("### 🗂 Suspect Status")
            for name in ss.suspects:
                d    = ss.suspect_data[name]
                tags = ""
                if d["contradiction"]["found"]:
                    tags += '<span class="badge-contra">LIAR</span>'
                if d["secret_revealed"]:
                    tags += '<span class="badge-secret">SECRET</span>'
                st.markdown(f"**{name}** {tags}", unsafe_allow_html=True)

            if ss.hidden_truth_mode and ss.hidden_truths:
                st.markdown("---")
                st.markdown("### 🌿 Hidden Truths")
                found_count = sum(1 for ht in ss.hidden_truths if ht["found"])
                st.markdown(f"Found: **{found_count} / {len(ss.hidden_truths)}**")
                for ht in ss.hidden_truths:
                    if ht["found"]:
                        st.markdown(
                            f'<span class="badge-truth">✓ {ht["title"]}</span>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown("🔒 *Hidden*")

            # Show background queue status subtly
            if ss.api_key.strip():
                q = bg_queue_size()
                if _bg["fetching"]:
                    st.markdown("---")
                    st.caption("🔄 Preparing next mystery in background…")
                elif q > 0:
                    st.markdown("---")
                    st.caption(f"✅ {q} AI mystery ready for next game")

            st.markdown("---")
            st.markdown("### 📜 Recent Log")
            for entry in ss.game_log[-8:][::-1]:
                st.markdown(entry["msg"])

        elif ss.phase == "welcome":
            st.markdown("**Enter your Gemini API key and configure the game to begin.**")
            st.markdown(
                "Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)",
            )

        elif ss.phase == "ended":
            st.markdown(f"### 🏆 Final Score: `{ss.score} pts`")
            st.markdown(f"**{score_rating(ss.score)}**")
            if st.button("🔄 New Game"):
                api_key = ss.api_key
                timer_mode = ss.timer_mode
                timer_seconds = ss.timer_seconds
                ht_mode = ss.hidden_truth_mode
                premade_index = ss.premade_index
                for k in list(ss.keys()):
                    del ss[k]
                st.session_state["api_key"] = api_key
                st.session_state["timer_mode"] = timer_mode
                st.session_state["timer_seconds"] = timer_seconds
                st.session_state["hidden_truth_mode"] = ht_mode
                st.session_state["premade_index"] = premade_index
                st.rerun()


render_sidebar()


# ═══════════════════════════════════════════════════════
#  WELCOME / SETUP SCREEN
# ═══════════════════════════════════════════════════════

def screen_welcome():
    st.markdown("""
    <div class="title-banner">
      <h1>🔍 The Manor House Mystery</h1>
      <p>AI-Generated Murder Mystery · Powered by Gemini · Detective-Themed</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown("### 🗝 Configuration")

        api_key = st.text_input(
            "Gemini API Key",
            value=ss.api_key,
            type="password",
            placeholder="Paste your Gemini API key here…",
        )
        ss.api_key = api_key

        st.markdown("---")
        st.markdown("### ⏱ Timer Mode")
        timer_on = st.checkbox("Compete against the clock", value=ss.timer_mode)
        ss.timer_mode = timer_on
        if timer_on:
            mins = st.slider("Time limit (minutes)", 2, 15, ss.timer_seconds // 60)
            ss.timer_seconds = mins * 60
            st.info(f"You'll have **{mins} minutes** to solve the case. Unused time = bonus score.")

        st.markdown("---")
        st.markdown("### 🌿 Hidden Truth Mode")
        ht_on = st.checkbox("Enable Hidden Truths (+50 pts each, extremely hard)", value=ss.hidden_truth_mode)
        ss.hidden_truth_mode = ht_on
        if ht_on:
            st.markdown("""
            <div class="truth-box">
            Gemini will hide <b>2 secret truths</b> in the mystery. Each truth has a cryptic keyword.
            If you figure out the keyword and type it in the investigation phase, you unlock the truth
            and earn <b>+50 points</b>. These are designed to be nearly impossible to guess — read
            every clue very carefully.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Begin Investigation", use_container_width=True):
            ss.phase = "generating"
            st.rerun()

    with col2:
        st.markdown("### 📖 How to Play")
        st.markdown("""
        <div class="det-card">
        <b>🚪 Examine the crime scene</b><br>Find clues left behind by the killer.<br><br>
        <b>🗺 Search the manor</b><br>Each room hides a lead. The map updates as you go.<br><br>
        <b>👤 Interrogate suspects</b><br>Everyone has an alibi. Not everyone is telling the truth.<br><br>
        <b>💥 Call out contradictions</b><br>Match scene clues to suspects' lies. +30 pts each.<br><br>
        <b>🤖 Ask Gemini for a hint</b><br>The narrator whispers… for a price of −10 pts.<br><br>
        <b>⚖ Accuse the killer</b><br>One shot. Make it count.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏆 Scoring")
        st.markdown("""
        <div class="det-card">
        Scene clue found &nbsp;&nbsp;&nbsp;→ <b>+10</b><br>
        Manor clue found &nbsp;&nbsp;&nbsp;→ <b>+10</b><br>
        Contradiction exposed → <b>+30</b><br>
        Secret revealed &nbsp;&nbsp;&nbsp;&nbsp;→ <b>+20</b><br>
        Hidden truth &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ <b>+50</b><br>
        Correct accusation &nbsp;&nbsp;→ <b>+50</b><br>
        Wrong accusation &nbsp;&nbsp;&nbsp;&nbsp;→ <b>−30</b><br>
        Gemini hint &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ <b>−10</b>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  GENERATING SCREEN
#  Strategy:
#    1. Try Gemini once (no retries, fast)
#    2. If it works → use that, then start bg fetch of 2 more
#    3. If it fails → load a premade mystery instantly,
#       then start bg polling every 5 s to retry Gemini
# ═══════════════════════════════════════════════════════

def screen_generating():
    st.markdown("""
    <div class="title-banner">
      <h1>🔍 The Manor House Mystery</h1>
    </div>
    """, unsafe_allow_html=True)

    # ── First check: is there a pre-built AI mystery waiting? ──
    queued = pop_bg_mystery()
    if queued:
        _apply_mystery(queued, is_premade=False)
        # kick off 2 more in background to keep queue stocked
        start_bg_fetch(ss.api_key, n=2)
        st.rerun()
        return

    # ── Try Gemini once, quickly ──
    status_box = st.empty()
    status_box.info("🕯 Contacting Gemini to craft a unique Victorian mystery…")

    raw    = call_gemini_once(build_mystery_prompt(), ss.api_key)
    result = parse_gemini_raw(raw)

    if result:
        status_box.empty()
        _apply_mystery(result, is_premade=False)
        # Start background generation of 2 more mysteries
        start_bg_fetch(ss.api_key, n=2)
        st.rerun()
        return

    # ── Gemini failed — load a premade instantly ──
    premade_idx = ss.get("premade_index", 0) % len(_PREMADE_MYSTERIES)
    ss["premade_index"] = (premade_idx + 1) % len(_PREMADE_MYSTERIES)

    status_box.warning(
        "⚠️ Gemini is rate-limited. Loading a hand-crafted mystery while retrying in the background…"
    )
    status_box.empty()

    premade_result = load_premade_mystery(premade_idx)
    _apply_mystery(premade_result, is_premade=True)

    # Start background polling: try to generate an AI mystery every 5 s
    # so it's ready for the NEXT game
    start_bg_fetch(ss.api_key, n=2)

    st.rerun()


# ═══════════════════════════════════════════════════════
#  MAIN GAME SCREEN
# ═══════════════════════════════════════════════════════

def screen_playing():
    if timer_expired() and ss.won is None:
        ss.won        = False
        ss.end_reason = "timeout"
        ss.phase      = "ended"
        add_log("⏰ Time expired — the killer escaped!", "red")
        st.rerun()

    st.markdown("""
    <div class="title-banner" style="padding:0.8rem 0 0.4rem">
      <h1 style="font-size:1.9rem!important">🔍 The Manor House Mystery</h1>
    </div>
    """, unsafe_allow_html=True)

    # Premade badge
    if ss.get("is_premade"):
        st.markdown(
            '<div style="text-align:center;margin-bottom:0.5rem">'
            '<span class="premade-badge">◈ HAND-CRAFTED MYSTERY — AI version preparing in background</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    rem = time_remaining()
    timer_html = ""
    if rem is not None:
        css = "timer-red" if rem <= 60 else ("timer-yellow" if rem <= 120 else "timer-green")
        timer_html = f'<span class="item"><span class="lbl">⏱ TIME</span><span class="val {css}">{fmt_time(rem)}</span></span>'

    st.markdown(f"""
    <div class="score-hud">
      <span class="item"><span class="lbl">⭐ SCORE</span><span class="val">{ss.score} pts</span></span>
      <span class="item"><span class="lbl">📋 CLUES</span><span class="val">{total_clues()}</span></span>
      <span class="item"><span class="lbl">🌿 TRUTHS</span><span class="val">{sum(1 for h in ss.hidden_truths if h['found'])} / {len(ss.hidden_truths)}</span></span>
      {timer_html}
    </div>
    """, unsafe_allow_html=True)

    if ss.victim:
        v = ss.victim
        st.markdown(f"""
        <div class="det-card">
        🌩 <i>The storm has swallowed Blackwood Manor whole.</i><br><br>
        <b>{v['name']}</b>, {v['role']}, has been found dead. Poisoned.<br>
        {v['found']}<br><br>
        Three people were present that night. You are <b>Detective Sterling</b>.
        Solve the case before the killer escapes.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    tabs = st.tabs([
        "🚪 Crime Scene",
        "🗺 Manor",
        "👤 Suspects",
        "💥 Contradictions",
        "📓 Notebook",
        "🤖 Hint",
        "⚖ Accuse",
    ])

    # ── TAB 0: Crime Scene ──
    with tabs[0]:
        st.markdown("### 🚪 Crime Scene: The Study")
        st.markdown(
            f'<div class="det-card"><i>{ss.crime_scene["description"]}</i></div>',
            unsafe_allow_html=True,
        )

        available = [cl for cl in ss.crime_scene["clues"]
                     if cl["name"] not in ss.scene_clues_found]

        if not available:
            st.success("✅ You have examined everything in this room.")
        else:
            st.markdown("**What do you examine?**")
            for cl in available:
                if st.button(f"🔎 {cl['name']}", key=f"scene_{cl['name']}"):
                    ss.scene_clues_found.append(cl["name"])
                    points(10, f"scene clue: {cl['name']}")
                    add_log(f"🔎 Found scene clue: **{cl['name']}**", "clue")
                    st.rerun()

        if ss.scene_clues_found:
            st.markdown("---")
            st.markdown("#### 📋 Clues Found Here")
            for cname in ss.scene_clues_found:
                for cl in ss.crime_scene["clues"]:
                    if cl["name"] == cname:
                        st.markdown(
                            f'<div class="clue-card"><h4>🔎 {cl["name"]}</h4><p>{cl["detail"]}</p></div>',
                            unsafe_allow_html=True,
                        )

    # ── TAB 1: Manor ──
    with tabs[1]:
        st.markdown("### 🗺 Search the Manor")
        st.markdown(
            f'<div class="manor-map">{render_manor_map(ss.manor_clues_found)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        remaining = [cl for cl in ss.manor_clues if cl["location"] not in ss.manor_clues_found]
        if not remaining:
            st.success("✅ You've searched every room. No new clues remain.")
        else:
            if st.button("🚶 Search a room (random)", use_container_width=True):
                found = random.choice(remaining)
                ss.manor_clues_found.append(found["location"])
                points(10, f"manor clue: {found['location']}")
                add_log(f"🏚 Searched **{found['location']}**: {found['text']}", "clue")
                st.rerun()

        if ss.manor_clues_found:
            st.markdown("---")
            st.markdown("#### 📋 Rooms Searched")
            for loc in ss.manor_clues_found:
                for cl in ss.manor_clues:
                    if cl["location"] == loc:
                        st.markdown(
                            f'<div class="clue-card"><h4>📌 {loc.title()}</h4><p>{cl["text"]}</p></div>',
                            unsafe_allow_html=True,
                        )

    # ── TAB 2: Suspects ──
    with tabs[2]:
        st.markdown("### 👤 The Suspects")

        cols = st.columns(len(ss.suspects))
        for i, (name, col) in enumerate(zip(ss.suspects, cols)):
            d    = ss.suspect_data[name]
            art  = get_suspect_art(name, i)
            is_gemini_art = bool(d.get("ascii_art", ""))
            art_label = (
                '<span style="font-size:0.65rem;color:var(--gold-dim);font-family:monospace">✦ AI portrait</span>'
                if is_gemini_art else
                '<span style="font-size:0.65rem;color:var(--text-dim);font-family:monospace">◇ generic</span>'
            )
            tags = ""
            if d["contradiction"]["found"]:
                tags += '<span class="badge-contra">LIAR</span> '
            if d["secret_revealed"]:
                tags += '<span class="badge-secret">SECRET</span>'
            with col:
                st.markdown(f"""
                <div class="suspect-card">
                  <code class="char-art">{art}</code>
                  <div style="margin:2px 0 4px">{art_label}</div>
                  <h4>{name}</h4>
                  <p>{d["description"]}</p>
                  {tags}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🗣 Interrogate a Suspect")
        chosen = st.selectbox("Choose suspect", ss.suspects, key="interrog_sel")

        # Show alibi on button click — store result in session state so it
        # persists across reruns (avoids the nested-button trap)
        if st.button("👤 Interrogate", key="do_interrog"):
            ss["last_interrogated"] = chosen
            add_log(f"👤 Interrogated **{chosen}**", "info")
            st.rerun()

        # Render interrogation result OUTSIDE the button block so it survives reruns
        last = ss.get("last_interrogated")
        if last and last in ss.suspect_data:
            d  = ss.suspect_data[last]
            tc = total_clues()
            st.markdown(f"""
            <div class="det-card">
            <b>{last}</b> says:<br><br>
            <i>"{d['alibi']}"</i>
            </div>
            """, unsafe_allow_html=True)

            if d["secret_revealed"]:
                st.markdown(f"""
                <div class="det-card" style="border-left-color:var(--magenta)">
                <b>Confession:</b> <i>"{d['secret']}"</i>
                </div>
                """, unsafe_allow_html=True)
            elif tc >= 3:
                # Press-harder button now lives OUTSIDE any other button block — works correctly
                if st.button(f"🔥 Press {last} harder", key=f"press_{last}"):
                    ss.suspect_data[last]["secret_revealed"] = True
                    points(20, f"secret: {last}")
                    add_log(f"🗣 Uncovered **{last}'s** secret motive!", "secret")
                    st.rerun()
            else:
                st.warning(f"You need at least 3 clues to press harder. ({tc} so far)")

    # ── TAB 3: Contradictions ──
    with tabs[3]:
        st.markdown("### 💥 Call Out a Contradiction")
        st.markdown("Match a suspect to a scene clue that disproves their alibi. **+30 pts**")

        chosen_c = st.selectbox("Choose suspect", ss.suspects, key="contra_sel")
        if st.button("💥 Challenge their alibi", key="do_contra"):
            d      = ss.suspect_data[chosen_c]
            contra = d["contradiction"]
            if contra["found"]:
                st.warning(f"You've already exposed {chosen_c}'s contradiction.")
            elif contra["clue_needed"] in ss.scene_clues_found:
                contra["found"] = True
                points(30, f"contradiction: {chosen_c}")
                add_log(f"💥 Exposed **{chosen_c}'s** lie!", "red")
                st.markdown(f"""
                <div class="drama-box">
                  <h2>💥 CONTRADICTION EXPOSED!</h2>
                  <p><b>{chosen_c} is LYING!</b></p>
                  <p style="color:var(--text)">{contra['explanation']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()
            else:
                st.error(f"You don't have enough evidence yet. Find **'{contra['clue_needed']}'** at the crime scene first.")

        exposed = [(n, d) for n, d in ss.suspect_data.items() if d["contradiction"]["found"]]
        if exposed:
            st.markdown("---")
            st.markdown("#### Already Exposed")
            for n, d in exposed:
                st.markdown(
                    f'<div class="clue-card"><h4>💥 {n} — alibi DISPROVEN</h4><p>{d["contradiction"]["explanation"]}</p></div>',
                    unsafe_allow_html=True,
                )

    # ── TAB 4: Notebook ──
    with tabs[4]:
        st.markdown("### 📓 Detective's Notebook")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔎 Scene Clues")
            if ss.scene_clues_found:
                for cname in ss.scene_clues_found:
                    st.markdown(f'<div class="nb-entry">🔸 {cname}</div>', unsafe_allow_html=True)
            else:
                st.info("None yet — visit the crime scene.")

            st.markdown("#### 🏚 Manor Clues")
            if ss.manor_clues_found:
                for loc in ss.manor_clues_found:
                    for cl in ss.manor_clues:
                        if cl["location"] == loc:
                            st.markdown(
                                f'<div class="nb-entry">📌 <b>{loc.title()}</b>: {cl["text"]}</div>',
                                unsafe_allow_html=True,
                            )
            else:
                st.info("None yet — search the manor.")

        with c2:
            st.markdown("#### 💥 Contradictions")
            any_c = any(d["contradiction"]["found"] for d in ss.suspect_data.values())
            if any_c:
                for n, d in ss.suspect_data.items():
                    if d["contradiction"]["found"]:
                        st.markdown(f'<div class="nb-entry">💥 <b>{n}</b>: alibi DISPROVEN</div>', unsafe_allow_html=True)
            else:
                st.info("None yet.")

            st.markdown("#### 🗣 Secrets")
            any_s = any(d["secret_revealed"] for d in ss.suspect_data.values())
            if any_s:
                for n, d in ss.suspect_data.items():
                    if d["secret_revealed"]:
                        st.markdown(f'<div class="nb-entry">🗣 <b>{n}</b>: "{d["secret"]}"</div>', unsafe_allow_html=True)
            else:
                st.info("None yet — interrogate suspects.")

        if ss.hidden_truth_mode and ss.hidden_truths:
            st.markdown("---")
            st.markdown("#### 🌿 Hidden Truths")
            st.markdown(
                "*Enter a keyword you've deduced from the evidence. Each correct keyword unlocks a hidden truth and awards +50 pts.*"
            )
            truth_kw = st.text_input("🔑 Enter keyword", key="truth_kw_input", placeholder="Type a Victorian keyword…")
            if st.button("🔍 Test Keyword", key="test_truth_kw"):
                kw = truth_kw.strip().lower()
                matched = False
                for ht in ss.hidden_truths:
                    if not ht["found"] and kw == ht["trigger_keyword"]:
                        ht["found"] = True
                        points(50, f"hidden truth: {ht['title']}")
                        add_log(f"🌿 Hidden truth unlocked: **{ht['title']}**!", "green")
                        matched = True
                        st.balloons()
                        break
                if not matched:
                    st.error("That keyword reveals nothing… keep investigating.")

            for ht in ss.hidden_truths:
                if ht["found"]:
                    st.markdown(f"""
                    <div class="truth-box">
                    <b>{ht['title']}</b><br><br>
                    {ht['description']}
                    <span class="badge-truth">+50 pts</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="clue-card" style="opacity:0.4"><h4>🔒 Hidden Truth — Locked</h4><p><i>Find the trigger keyword to unlock this truth.</i></p></div>',
                        unsafe_allow_html=True,
                    )

    # ── TAB 5: Hint ──
    with tabs[5]:
        st.markdown("### 🤖 Ask Gemini for a Hint")
        st.markdown("*The Victorian narrator will whisper a cryptic clue… for a price of **−10 pts**.*")

        if ss.last_hint:
            st.markdown(
                f'<div class="hint-box">🕯 {ss.last_hint}</div>',
                unsafe_allow_html=True,
            )

        if st.button("🕯 Consult the Narrator (−10 pts)", use_container_width=True):
            if not ss.api_key.strip():
                st.warning("No API key set — hints require Gemini. Add your key on the welcome screen.")
            else:
                points(-10, "hint requested")
                with st.spinner("🕯 The narrator gazes into the shadows…"):
                    p    = hint_prompt(ss.victim, ss.suspects, ss.suspect_data,
                                       ss.scene_clues_found, ss.manor_clues_found, ss.murderer)
                    hint = call_gemini(p, ss.api_key)
                if hint:
                    ss.last_hint = hint.strip()
                    add_log("🤖 Consulted Gemini narrator.", "info")
                else:
                    ss.last_hint = "The narrator remains silent tonight…"
                    points(10, "hint refunded (API error)")
                st.rerun()

    # ── TAB 6: Accuse ──
    with tabs[6]:
        st.markdown("### ⚖ Make Your Accusation")

        tc = total_clues()
        if tc < 3:
            st.warning(f"⚠ Gather at least 3 clues before accusing anyone. ({tc}/3 so far)")
        else:
            st.markdown("**This is your ONE accusation. Choose carefully.**")
            accusee = st.selectbox("I accuse…", ss.suspects, key="accuse_sel")
            if st.button("⚖ Make the Accusation", use_container_width=True, key="do_accuse"):
                won = (accusee == ss.murderer)
                if won:
                    points(50, "correct accusation")
                    add_log(f"⚖ Accused **{accusee}** — CORRECT!", "green")
                else:
                    points(-30, "wrong accusation")
                    add_log(f"⚖ Accused **{accusee}** — WRONG! Real killer: {ss.murderer}", "red")
                ss.won        = won
                ss.end_reason = "correct" if won else "wrong"
                ss.phase      = "ended"
                st.rerun()


# ═══════════════════════════════════════════════════════
#  ENDING SCREEN
# ═══════════════════════════════════════════════════════

def screen_ended():
    st.markdown("""
    <div class="title-banner">
      <h1>⚖ Case Closed</h1>
    </div>
    """, unsafe_allow_html=True)

    if ss.won is True:
        st.markdown(f"""
        <div class="drama-box" style="border-color:var(--green)">
          <h2 style="color:#6fcf97">🎉 CASE SOLVED!</h2>
          <p style="color:var(--text); font-size:1.2rem">
            {ss.murderer} crumbles and confesses.
          </p>
          <p style="color:var(--text-dim)"><i>Motive: "{ss.suspect_data[ss.murderer]['secret']}"</i></p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    elif ss.end_reason == "timeout":
        st.markdown(f"""
        <div class="drama-box">
          <h2>⏰ TIME'S UP!</h2>
          <p style="color:var(--text)">The killer slips into the night…</p>
          <p style="color:var(--text-dim)">The murderer was <b>{ss.murderer}</b>.</p>
          <p style="color:var(--text-dim)"><i>Motive: "{ss.suspect_data[ss.murderer]['secret']}"</i></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="drama-box">
          <h2>❌ WRONG ACCUSATION</h2>
          <p style="color:var(--text)">The real killer escapes into the night…</p>
          <p style="color:var(--text-dim)">The murderer was <b>{ss.murderer}</b>.</p>
          <p style="color:var(--text-dim)"><i>Motive: "{ss.suspect_data[ss.murderer]['secret']}"</i></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-hud" style="justify-content:center">
      <span class="item" style="text-align:center">
        <span class="lbl">FINAL SCORE</span>
        <span class="val" style="font-size:2.2rem">{ss.score} pts</span>
      </span>
      <span class="item" style="text-align:center">
        <span class="lbl">RATING</span>
        <span class="val rating" style="font-size:1.2rem">{score_rating(ss.score)}</span>
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Show queue status on end screen
    q = bg_queue_size()
    if q > 0:
        st.success(f"✅ {q} AI-generated {'mystery is' if q == 1 else 'mysteries are'} ready — your next game will be fully unique!")
    elif _bg["fetching"]:
        st.info("🔄 An AI mystery is being prepared for your next game…")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📜 Generate AI Case Report", use_container_width=True):
            if not ss.api_key.strip():
                st.warning("No API key — case reports require Gemini.")
            else:
                with st.spinner("📜 Detective Sterling is writing the case report…"):
                    truths_found = [ht["title"] for ht in ss.hidden_truths if ht["found"]]
                    p = case_report_prompt(
                        ss.victim, ss.suspects, ss.suspect_data, ss.murderer,
                        ss.scene_clues_found, ss.manor_clues_found, ss.score,
                        ss.won, truths_found,
                    )
                    ss.case_report = call_gemini(p, ss.api_key)
                st.rerun()
    with col2:
        if st.button("🔄 New Mystery", use_container_width=True):
            api_key       = ss.api_key
            timer_mode    = ss.timer_mode
            timer_seconds = ss.timer_seconds
            ht_mode       = ss.hidden_truth_mode
            premade_index = ss.get("premade_index", 0)
            for k in list(ss.keys()):
                del ss[k]
            st.session_state["api_key"]        = api_key
            st.session_state["timer_mode"]     = timer_mode
            st.session_state["timer_seconds"]  = timer_seconds
            st.session_state["hidden_truth_mode"] = ht_mode
            st.session_state["premade_index"]  = premade_index
            st.session_state["phase"]          = "generating"
            st.rerun()

    if ss.case_report:
        st.markdown("---")
        st.markdown("### 📜 Official Case Report")
        st.markdown(
            f'<div class="det-card" style="border-left-color:var(--cyan);white-space:pre-wrap">{ss.case_report}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("📋 Full Game Log"):
        for entry in ss.game_log:
            st.markdown(entry["msg"])


# ═══════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════

if ss.phase == "welcome":
    screen_welcome()
elif ss.phase == "generating":
    screen_generating()
elif ss.phase == "playing":
    screen_playing()
elif ss.phase == "ended":
    screen_ended()
