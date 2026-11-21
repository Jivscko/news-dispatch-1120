"""Facts, palette and geography for the 20 November 2026 front page.

Every string here is drawn from the ten reported items in README.md plus the
date. No names, numbers or sources beyond those ten items are asserted.
"""

PAPER = (246, 242, 232)
INK = (24, 22, 20)
GREY = (94, 88, 80)
MID = (140, 132, 120)
LIGHT = (206, 198, 184)
RULE = (34, 32, 28)
PAPER_DARK = (232, 225, 211)
RIVER = (186, 197, 196)

SECTIONS = {
    "world": (32, 98, 68),
    "politics": (32, 66, 132),
    "energy": (168, 104, 18),
    "justice": (150, 32, 40),
    "market": (88, 54, 136),
}

DATE_LONG = "FRIDAY, 20 NOVEMBER 2026"
DATE_SHORT = "20 NOV 2026"
ALL_DATED = "ALL STORIES DATED 20 NOVEMBER 2026"

LEAD = {
    "num": 1,
    "kick": "LEAD STORY / WORLD",
    "head": "Russia fires retaliatory missile barrage at Kyiv bridges",
    "lines": ("Russia fires retaliatory", "missile barrage at Kyiv bridges"),
    "deck": (
        "A retaliatory missile barrage on the bridges of Kyiv leads the day; "
        "nine other dispatches follow, all dated 20 November 2026."
    ),
    "deck2": (
        "Other datelines: Washington, Texas, New York, Brussels and London, "
        "the Estonian border, global markets and China."
    ),
    "src": "KYIV / 20 NOVEMBER 2026 / STORY 01 OF 10",
    "section": "world",
}

# Secondary stories, in page order after the lead.
STORIES = [
    {
        "num": 2, "section": "politics", "kick": "POLITICS / WASHINGTON",
        "head": "White House removes cyber-security chief after federal tech outages",
        "dek": "The cyber-security chief is out after a run of federal tech outages.",
        "where": "WASHINGTON",
    },
    {
        "num": 3, "section": "energy", "kick": "ENERGY / SENATE",
        "head": "Senate passes bipartisan energy bill over environmental objections",
        "dek": "A bipartisan energy bill clears the Senate despite green objections.",
        "where": "WASHINGTON",
    },
    {
        "num": 7, "section": "world", "kick": "EUROPE / RESET",
        "head": "EU and UK agree to reset relations, ten years after Brexit",
        "dek": "Ten years after Brexit, both sides agree to reset relations.",
        "where": "BRUSSELS / LONDON",
    },
    {
        "num": 4, "section": "justice", "kick": "JUSTICE / TEXAS",
        "head": "Texas death-row execution takes more than an hour",
        "dek": "The execution ran past an hour, the reported item says.",
        "where": "TEXAS",
    },
    {
        "num": 6, "section": "politics", "kick": "NEW YORK / JAIL PLAN",
        "head": "Mamdani sets out plan to close Rikers Island",
        "dek": "The plan would close the Rikers Island jail in New York.",
        "where": "NEW YORK",
    },
    {
        "num": 5, "section": "justice", "kick": "DEFENCE / TEXAS",
        "head": "US Army delays detonation of lead explosives",
        "dek": "Public concern and a lawsuit push the detonation back.",
        "where": "TEXAS",
    },
    {
        "num": 8, "section": "world", "kick": "BALTIC / BORDER",
        "head": "Estonia shuts Russian border; Moscow cries new Iron Curtain",
        "dek": "Estonia closes its border with Russia; Moscow calls it a new Iron Curtain.",
        "where": "ESTONIA / RUSSIA",
    },
    {
        "num": 9, "section": "market", "kick": "MARKETS / IPO",
        "head": "Anthropic stock falls on first day of trading",
        "dek": "Shares fell on the first day of trading after the IPO.",
        "where": "GLOBAL MARKETS",
    },
    {
        "num": 10, "section": "market", "kick": "TECH / CHIPS",
        "head": "China's AI firms short of Nvidia chips",
        "dek": "China's AI firms are short of Nvidia chips, the day's report says.",
        "where": "CHINA",
    },
]

# The four largest cards: 2, 3, 7 and 4 in page order, then the compact briefs.
FEATURE = 2
MEDIUM = [3, 7, 4, 6]
COMPACT = [5, 8, 9, 10]

NUMERALS = [
    ("10", "YEARS SINCE", "BREXIT"),
    ("1 HR+", "TEXAS EXECUTION", "RAN PAST"),
    ("9", "OTHER DISPATCHES", "BESIDE THE LEAD"),
    ("10", "STORIES ON", "THIS PAGE"),
    ("1ST", "DAY OF TRADING", "AFTER THE IPO"),
]

INDEX = [
    (1, "KYIV / MISSILE BARRAGE"),
    (2, "WASHINGTON / CYBER CHIEF"),
    (3, "WASHINGTON / ENERGY BILL"),
    (4, "TEXAS / EXECUTION"),
    (5, "TEXAS / ARMY TEST"),
    (6, "NEW YORK / RIKERS"),
    (7, "BRUSSELS-LONDON / RESET"),
    (8, "ESTONIA / BORDER"),
    (9, "MARKETS / ANTHROPIC"),
    (10, "CHINA / CHIP SHORTAGE"),
]
