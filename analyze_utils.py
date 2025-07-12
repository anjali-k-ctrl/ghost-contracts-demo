
import re

RISKY_PHRASES = {
    "high": [
        r"terminate.*any time",
        r"without notice",
        r"binding arbitration",
        r"no liability",
        r"waive.*rights"
    ],
    "medium": [
        r"third[- ]party",
        r"auto[- ]renew",
        r"not responsible",
        r"may suspend",
        r"change.*terms"
    ]
}

def classify_clause(clause):
    matches = []
    risk_score = 0
    for level, patterns in RISKY_PHRASES.items():
        for pat in patterns:
            if re.search(pat, clause, re.IGNORECASE):
                matches.append(pat)
                risk_score += {"high": 5, "medium": 3}[level]
    if risk_score >= 8:
        return "high", matches, risk_score
    elif risk_score >= 4:
        return "medium", matches, risk_score
    return "low", matches, risk_score

def analyze_clauses(text):
    clauses = re.split(r'(?<=[.;])\s+', text)
    analysis = []
    for c in clauses:
        if len(c.strip()) < 30:
            continue
        risk, keywords, score = classify_clause(c)
        analysis.append({
            "title": c.strip()[:60] + "...",
            "summary": "This means: " + c.strip(),
            "risk_level": risk,
            "keywords_found": keywords,
            "risk_score": score
        })
    return {
        "summary": "Contract analyzed for potential risks and simplified.",
        "analysis": analysis
    }
