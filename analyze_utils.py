import re

RISKY_PHRASES = {
    "high": [
        r"\bnot\s+liable\b",
        r"\bnot\s+liable\s+for\s+(any\s+)?(damages|loss|harm)\b",
        r"\bno\s+liability\b",
        r"\bwe\s+are\s+not\s+responsible\b",
        r"\bbinding\s+arbitration\b",
        r"\bterminate(d|s|ing)?\b.*?\bany\s+time\b",
        r"\bwithout\s+prior\s+notice\b",
        r"\bwaive(s|d|r|ing)?\s+.*?\bright(s)?\b",
        r"\bnon[-\s]?refundable\b"
    ],
    "medium": [
        r"\bauto(\s|-|_)?renew(al)?\b",
        r"\bsubject\s+to\s+change\b",
        r"\bthird[-\s]?party\b",
        r"\bfees\s+may\s+apply\b",
        r"\bmay\s+suspend\b",
        r"\badditional\s+charges\b",
        r"\bdiscretionary\b",
        r"\bmay\s+terminate\b",
        r"\bchange(s)?\s+to\s+these\s+terms\b",
        r"\bdata\s+may\s+be\s+shared\b"
    ]
}

# Friendly display names for each regex pattern
RISKY_KEYWORDS = {
    r"\bnot\s+liable\b": "Not liable",
    r"\bnot\s+liable\s+for\s+(any\s+)?(damages|loss|harm)\b": "No liability for damages",
    r"\bno\s+liability\b": "No liability",
    r"\bwe\s+are\s+not\s+responsible\b": "Not responsible",
    r"\bbinding\s+arbitration\b": "Binding arbitration",
    r"\bterminate(d|s|ing)?\b.*?\bany\s+time\b": "Terminate any time",
    r"\bwithout\s+prior\s+notice\b": "Without prior notice",
    r"\bwaive(s|d|r|ing)?\s+.*?\bright(s)?\b": "Waiving rights",
    r"\bnon[-\s]?refundable\b": "Non-refundable",
    r"\bauto(\s|-|_)?renew(al)?\b": "Auto-renewal",
    r"\bsubject\s+to\s+change\b": "Subject to change",
    r"\bthird[-\s]?party\b": "Third-party involvement",
    r"\bfees\s+may\s+apply\b": "Fees may apply",
    r"\bmay\s+suspend\b": "May suspend",
    r"\badditional\s+charges\b": "Additional charges",
    r"\bdiscretionary\b": "Discretionary decision",
    r"\bmay\s+terminate\b": "May terminate",
    r"\bchange(s)?\s+to\s+these\s+terms\b": "Changes to terms",
    r"\bdata\s+may\s+be\s+shared\b": "Data sharing"
}

RISK_WEIGHTS = {
    "high": 5,
    "medium": 4
}

def classify_clause(clause):
    matches = []
    score = 0
    for level, patterns in RISKY_PHRASES.items():
        for pattern in patterns:
            if re.search(pattern, clause, re.IGNORECASE):
                label = RISKY_KEYWORDS.get(pattern, pattern)
                matches.append(label)
                score += RISK_WEIGHTS[level]
    if score >= 8:
        return "high", matches, score
    elif score >= 3:
        return "medium", matches, score
    else:
        return "low", matches, score

def analyze_clauses(text):
    clauses = re.split(r'(?<=[.!?;])\s+', text)
    results = []
    for clause in clauses:
        clean = clause.strip()
        if len(clean) < 30:
            continue
        risk, keywords, score = classify_clause(clean)
        results.append({
            "title": clean[:60] + "...",
            "summary": "This means: " + clean,
            "risk_level": risk,
            "keywords_found": keywords,
            "risk_score": score
        })
    return {
        "summary": "Contract analyzed for hidden or risky clauses.",
        "analysis": results
    }

