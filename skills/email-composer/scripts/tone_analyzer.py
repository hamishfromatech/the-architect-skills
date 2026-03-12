"""
Tone Analyzer - Analyze email tone for appropriateness.

This module provides utilities for analyzing the tone of email
content and suggesting improvements for professional communication.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple


class ToneCategory(Enum):
    """Categories of email tone."""
    FORMAL = "formal"
    SEMIFORMAL = "semiformal"
    CASUAL = "casual"
    AGGRESSIVE = "aggressive"
    PASSIVE = "passive"
    URGENT = "urgent"
    FRIENDLY = "friendly"


@dataclass
class ToneMatch:
    """A tone match found in text."""
    category: ToneCategory
    phrase: str
    position: int
    severity: str  # "low", "medium", "high"
    suggestion: str


@dataclass
class ToneAnalysis:
    """Complete tone analysis result."""
    overall_tone: ToneCategory
    confidence: float
    matches: List[ToneMatch]
    recommendations: List[str]
    formality_score: float  # 0-100
    clarity_score: float
    conciseness_score: float


# Tone indicators
FORMAL_INDICATORS = {
    "phrases": [
        "I would like to request",
        "Please accept my apologies",
        "I am writing to inform you",
        "Kind regards",
        "Sincerely",
        "Dear Sir/Madam",
        "I remain",
        "Yours faithfully",
    ],
    "words": ["hereby", "wherein", "thereof", "pursuant", "notwithstanding"],
}

CASUAL_INDICATORS = {
    "phrases": [
        "no worries",
        "sounds good",
        "catch you later",
        "hey there",
        "what's up",
        "cheers",
        "thanks!",
        "cool",
        "awesome",
    ],
    "words": ["gonna", "wanna", "kinda", "sorta", "yeah", "ok", "cool"],
}

AGGRESSIVE_INDICATORS = {
    "phrases": [
        "you must",
        "you should have",
        "why didn't you",
        "this is unacceptable",
        "I demand",
        "you failed to",
        "you need to",
        "immediately",
        "asap",
    ],
    "words": ["must", "demand", "ridiculous", "unacceptable", "failure"],
}

URGENT_INDICATORS = {
    "phrases": [
        "urgent",
        "as soon as possible",
        "immediately",
        "deadline",
        "time-sensitive",
        "priority",
        "urgent response needed",
    ],
    "words": ["urgent", "asap", "critical", "emergency", "deadline"],
}

# Phrases to avoid in professional emails
UNPROFESSIONAL_PHRASES = [
    (r"\bidiots?\b", "Avoid negative language about people"),
    (r"\bstupid\b", "Use constructive feedback instead"),
    (r"\bhate\b", "Express concerns more professionally"),
    (r"\bbullshit\b", "Use professional language"),
    (r"\bwhatever\b", "Show engagement and interest"),
    (r"\bI guess\b", "Be more confident in your communication"),
    (r"\bmaybe\b", "Be more definitive when possible"),
]

# Passive voice patterns
PASSIVE_PATTERNS = [
    r"(?:was|were|is|are|been|being)\s+\w+ed\b",
    r"\b(?:it is|it was)\s+(?:noted|observed|decided|recommended)",
]


class ToneAnalyzer:
    """Analyze and improve email tone."""

    def __init__(self):
        """Initialize the analyzer."""
        self.compiled_patterns = {
            "unprofessional": [(re.compile(p, re.IGNORECASE), s) for p, s in UNPROFESSIONAL_PHRASES],
            "passive": [re.compile(p, re.IGNORECASE) for p in PASSIVE_PATTERNS],
        }

    def analyze(self, text: str) -> ToneAnalysis:
        """
        Perform comprehensive tone analysis.

        Args:
            text: Email content to analyze

        Returns:
            ToneAnalysis with all findings
        """
        matches = []
        recommendations = []

        # Detect overall tone
        overall_tone, confidence = self._detect_overall_tone(text)

        # Find tone matches
        matches.extend(self._find_formal_matches(text))
        matches.extend(self._find_casual_matches(text))
        matches.extend(self._find_aggressive_matches(text))
        matches.extend(self._find_urgent_matches(text))

        # Check for unprofessional content
        unprofessional = self._check_unprofessional(text)
        matches.extend(unprofessional)

        # Check for passive voice
        passive = self._check_passive_voice(text)
        matches.extend(passive)

        # Generate recommendations
        recommendations = self._generate_recommendations(matches, overall_tone)

        # Calculate scores
        formality_score = self._calculate_formality_score(text, matches)
        clarity_score = self._calculate_clarity_score(text)
        conciseness_score = self._calculate_conciseness_score(text)

        return ToneAnalysis(
            overall_tone=overall_tone,
            confidence=confidence,
            matches=matches,
            recommendations=recommendations,
            formality_score=formality_score,
            clarity_score=clarity_score,
            conciseness_score=conciseness_score,
        )

    def _detect_overall_tone(self, text: str) -> Tuple[ToneCategory, float]:
        """Detect the overall tone of the email."""
        text_lower = text.lower()

        # Count indicators
        formal_count = self._count_indicators(text_lower, FORMAL_INDICATORS)
        casual_count = self._count_indicators(text_lower, CASUAL_INDICATORS)
        aggressive_count = self._count_indicators(text_lower, AGGRESSIVE_INDICATORS)
        urgent_count = self._count_indicators(text_lower, URGENT_INDICATORS)

        # Determine dominant tone
        scores = {
            ToneCategory.FORMAL: formal_count,
            ToneCategory.CASUAL: casual_count,
            ToneCategory.AGGRESSIVE: aggressive_count,
            ToneCategory.URGENT: urgent_count,
        }

        dominant_tone = max(scores, key=scores.get)
        total = sum(scores.values()) or 1
        confidence = scores[dominant_tone] / total

        # Default to semiformal if no strong indicators
        if confidence < 0.3:
            return ToneCategory.SEMIFORMAL, 0.5

        return dominant_tone, min(confidence, 1.0)

    def _count_indicators(self, text: str, indicators: Dict) -> int:
        """Count tone indicators in text."""
        count = 0
        for phrase in indicators.get("phrases", []):
            if phrase.lower() in text:
                count += 1
        for word in indicators.get("words", []):
            count += len(re.findall(rf'\b{word}\b', text, re.IGNORECASE))
        return count

    def _find_formal_matches(self, text: str) -> List[ToneMatch]:
        """Find formal tone indicators."""
        matches = []
        text_lower = text.lower()

        for phrase in FORMAL_INDICATORS["phrases"]:
            if phrase.lower() in text_lower:
                pos = text_lower.find(phrase.lower())
                matches.append(ToneMatch(
                    category=ToneCategory.FORMAL,
                    phrase=phrase,
                    position=pos,
                    severity="low",
                    suggestion="Formal phrasing - appropriate for professional contexts",
                ))

        return matches

    def _find_casual_matches(self, text: str) -> List[ToneMatch]:
        """Find casual tone indicators."""
        matches = []
        text_lower = text.lower()

        for phrase in CASUAL_INDICATORS["phrases"]:
            if phrase.lower() in text_lower:
                pos = text_lower.find(phrase.lower())
                matches.append(ToneMatch(
                    category=ToneCategory.CASUAL,
                    phrase=phrase,
                    position=pos,
                    severity="low",
                    suggestion="Consider more formal alternatives for professional contexts",
                ))

        return matches

    def _find_aggressive_matches(self, text: str) -> List[ToneMatch]:
        """Find aggressive tone indicators."""
        matches = []
        text_lower = text.lower()

        for phrase in AGGRESSIVE_INDICATORS["phrases"]:
            if phrase.lower() in text_lower:
                pos = text_lower.find(phrase.lower())
                matches.append(ToneMatch(
                    category=ToneCategory.AGGRESSIVE,
                    phrase=phrase,
                    position=pos,
                    severity="medium",
                    suggestion="This phrasing may come across as aggressive. Consider softer alternatives.",
                ))

        return matches

    def _find_urgent_matches(self, text: str) -> List[ToneMatch]:
        """Find urgency indicators."""
        matches = []
        text_lower = text.lower()

        for phrase in URGENT_INDICATORS["phrases"]:
            if phrase.lower() in text_lower:
                pos = text_lower.find(phrase.lower())
                matches.append(ToneMatch(
                    category=ToneCategory.URGENT,
                    phrase=phrase,
                    position=pos,
                    severity="low",
                    suggestion="Urgency detected. Ensure this is appropriate for the context.",
                ))

        return matches

    def _check_unprofessional(self, text: str) -> List[ToneMatch]:
        """Check for unprofessional language."""
        matches = []

        for pattern, suggestion in self.compiled_patterns["unprofessional"]:
            for match in pattern.finditer(text):
                matches.append(ToneMatch(
                    category=ToneCategory.AGGRESSIVE,
                    phrase=match.group(),
                    position=match.start(),
                    severity="high",
                    suggestion=suggestion,
                ))

        return matches

    def _check_passive_voice(self, text: str) -> List[ToneMatch]:
        """Check for passive voice usage."""
        matches = []

        for pattern in self.compiled_patterns["passive"]:
            for match in pattern.finditer(text):
                matches.append(ToneMatch(
                    category=ToneCategory.PASSIVE,
                    phrase=match.group(),
                    position=match.start(),
                    severity="low",
                    suggestion="Consider using active voice for more direct communication",
                ))

        return matches

    def _generate_recommendations(
        self,
        matches: List[ToneMatch],
        overall_tone: ToneCategory,
    ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        # Check for aggressive content
        aggressive = [m for m in matches if m.category == ToneCategory.AGGRESSIVE]
        if len(aggressive) > 2:
            recommendations.append(
                "Multiple aggressive phrases detected. Consider softening the tone."
            )

        # Check for passive voice
        passive = [m for m in matches if m.category == ToneCategory.PASSIVE]
        if len(passive) > 3:
            recommendations.append(
                "Heavy use of passive voice. Consider more active phrasing."
            )

        # Check for urgency overuse
        urgent = [m for m in matches if m.category == ToneCategory.URGENT]
        if len(urgent) > 2:
            recommendations.append(
                "Multiple urgency indicators. Reserve urgency for truly time-sensitive matters."
            )

        # Tone-specific recommendations
        if overall_tone == ToneCategory.AGGRESSIVE:
            recommendations.append(
                "Overall tone appears aggressive. Review for professional appropriateness."
            )
        elif overall_tone == ToneCategory.CASUAL:
            recommendations.append(
                "Tone is casual. Ensure this matches your audience expectations."
            )

        return recommendations

    def _calculate_formality_score(
        self,
        text: str,
        matches: List[ToneMatch],
    ) -> float:
        """Calculate formality score (0-100)."""
        formal_matches = [m for m in matches if m.category == ToneCategory.FORMAL]
        casual_matches = [m for m in matches if m.category == ToneCategory.CASUAL]

        # Base score
        score = 50

        # Adjust based on matches
        score += len(formal_matches) * 5
        score -= len(casual_matches) * 5

        # Check for contractions (less formal)
        contractions = len(re.findall(r"\w+'\w+", text))
        score -= contractions * 2

        # Check sentence length (longer = more formal)
        sentences = re.split(r'[.!?]', text)
        avg_length = sum(len(s.split()) for s in sentences if s.strip()) / max(len(sentences) - 1, 1)
        if avg_length > 20:
            score += 10
        elif avg_length < 10:
            score -= 10

        return max(0, min(100, score))

    def _calculate_clarity_score(self, text: str) -> float:
        """Calculate clarity score (0-100)."""
        score = 100

        # Check for unclear phrases
        unclear = re.findall(
            r'\b(?:basically|actually|really|very|quite|rather|somewhat)\b',
            text,
            re.IGNORECASE
        )
        score -= len(unclear) * 5

        # Check for jargon
        jargon = re.findall(
            r'\b(?:synergy|leverage|paradigm|utilize|facilitate)\b',
            text,
            re.IGNORECASE
        )
        score -= len(jargon) * 3

        # Check average word length (too complex words reduce clarity)
        words = text.split()
        if words:
            avg_word_len = sum(len(w) for w in words) / len(words)
            if avg_word_len > 7:
                score -= 10

        return max(0, min(100, score))

    def _calculate_conciseness_score(self, text: str) -> float:
        """Calculate conciseness score (0-100)."""
        score = 100

        # Check for wordiness
        wordy_phrases = [
            (r'\bin order to\b', 'to'),
            (r'\bat this point in time\b', 'now'),
            (r'\bdue to the fact that\b', 'because'),
            (r'\bin the event that\b', 'if'),
            (r'\bfor the purpose of\b', 'for'),
            (r'\bwith regard to\b', 'regarding'),
            (r'\bin spite of the fact that\b', 'although'),
        ]

        for pattern, replacement in wordy_phrases:
            matches = re.findall(pattern, text, re.IGNORECASE)
            score -= len(matches) * 10

        # Check for filler words
        filler = re.findall(
            r'\b(?:just|that|which|there is|there are|it is)\b',
            text,
            re.IGNORECASE
        )
        score -= len(filler) * 2

        return max(0, min(100, score))


def suggest_improvements(text: str) -> List[str]:
    """
    Generate improvement suggestions for email text.

    Args:
        text: Email content to analyze

    Returns:
        List of improvement suggestions
    """
    analyzer = ToneAnalyzer()
    analysis = analyzer.analyze(text)

    suggestions = []

    # Add recommendations
    suggestions.extend(analysis.recommendations)

    # Add specific improvements for each match
    for match in analysis.matches:
        if match.severity in ["medium", "high"]:
            suggestions.append(f"Near '{match.phrase}': {match.suggestion}")

    return list(set(suggestions))  # Remove duplicates


if __name__ == "__main__":
    # Example usage
    sample_email = """
    Dear John,

    I wanted to follow up on our previous conversation. Basically, we really need
    to get this done ASAP. You must submit the report by Friday or else we will
    have serious problems.

    Let me know what you think.

    Thanks!
    """

    analyzer = ToneAnalyzer()
    analysis = analyzer.analyze(sample_email)

    print(f"Overall Tone: {analysis.overall_tone.value}")
    print(f"Confidence: {analysis.confidence:.2f}")
    print(f"Formality Score: {analysis.formality_score:.1f}/100")
    print(f"Clarity Score: {analysis.clarity_score:.1f}/100")
    print(f"Conciseness Score: {analysis.conciseness_score:.1f}/100")
    print("\nRecommendations:")
    for rec in analysis.recommendations:
        print(f"  - {rec}")