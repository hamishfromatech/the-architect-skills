"""
Meeting Parser - Parse raw meeting notes into structured format.

This module provides utilities for parsing unstructured meeting notes
and extracting key information like attendees, topics, and action items.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from enum import Enum


class MeetingType(Enum):
    """Types of meetings."""
    STANDUP = "standup"
    STATUS = "status"
    PLANNING = "planning"
    REVIEW = "review"
    BRAINSTORM = "brainstorm"
    DECISION = "decision"
    ONE_ON_ONE = "one_on_one"
    ALL_HANDS = "all_hands"


@dataclass
class Attendee:
    """Meeting attendee information."""
    name: str
    role: Optional[str] = None
    email: Optional[str] = None


@dataclass
class ActionItem:
    """Meeting action item."""
    task: str
    owner: Optional[str] = None
    due_date: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"


@dataclass
class Decision:
    """Meeting decision."""
    description: str
    made_by: Optional[str] = None
    date: Optional[str] = None


@dataclass
class Meeting:
    """Structured meeting data."""
    title: str
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    meeting_type: MeetingType = MeetingType.STATUS
    attendees: List[Attendee] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    discussions: Dict[str, str] = field(default_factory=dict)
    decisions: List[Decision] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    next_meeting: Optional[str] = None
    raw_notes: str = ""


class MeetingParser:
    """Parse raw meeting notes into structured format."""

    # Patterns for extraction
    DATE_PATTERNS = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
    ]

    TIME_PATTERNS = [
        r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b',
        r'\b\d{1,2}\s*(?:AM|PM|am|pm)\b',
    ]

    ATTENDEE_PATTERNS = [
        r'(?:attendees?|participants?|present):\s*([^\n]+)',
        r'(?:@[\w-]+\s*)+',  # @mentions
    ]

    ACTION_PATTERNS = [
        r'(?:action|todo|task)[:\s]+([^\n]+)',
        r'(\w+)\s+(?:will|to)\s+([^\n]+)',
        r'\[\s*(\w+)\s*\]\s*(?:todo|task)?[:\s]*([^\n]+)',
        r'-\s*\[\s*\]\s*([^\n]+)',  # Checkbox items
    ]

    DECISION_PATTERNS = [
        r'(?:decision|decided|agreed)[:\s]+([^\n]+)',
        r'we\s+(?:will|agreed to|decided to)\s+([^\n]+)',
    ]

    BLOCKER_PATTERNS = [
        r'(?:blocker|blocked|blocked by|risk|issue)[:\s]+([^\n]+)',
        r'(?:waiting on|depends on)[:\s]+([^\n]+)',
    ]

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse(self, raw_notes: str) -> Meeting:
        """
        Parse raw meeting notes into structured Meeting object.

        Args:
            raw_notes: Raw meeting notes text

        Returns:
            Structured Meeting object
        """
        meeting = Meeting(
            title=self._extract_title(raw_notes),
            date=self._extract_date(raw_notes),
            time=self._extract_time(raw_notes),
            location=self._extract_location(raw_notes),
            organizer=self._extract_organizer(raw_notes),
            attendees=self._extract_attendees(raw_notes),
            topics=self._extract_topics(raw_notes),
            decisions=self._extract_decisions(raw_notes),
            action_items=self._extract_action_items(raw_notes),
            blockers=self._extract_blockers(raw_notes),
            next_meeting=self._extract_next_meeting(raw_notes),
            raw_notes=raw_notes,
        )

        # Extract discussions per topic
        meeting.discussions = self._extract_discussions(raw_notes, meeting.topics)

        return meeting

    def _extract_title(self, text: str) -> str:
        """Extract meeting title."""
        # Try first line as title
        lines = text.strip().split('\n')
        first_line = lines[0].strip()

        # Remove common prefixes
        title = re.sub(r'^(?:meeting|notes|minutes)[:\s]*', '', first_line, flags=re.IGNORECASE)

        # Remove markdown headings
        title = re.sub(r'^#+\s*', '', title)

        return title if title else "Untitled Meeting"

    def _extract_date(self, text: str) -> Optional[str]:
        """Extract meeting date."""
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)

        # Look for date labels
        date_match = re.search(r'(?:date|when)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if date_match:
            return date_match.group(1).strip()

        return None

    def _extract_time(self, text: str) -> Optional[str]:
        """Extract meeting time."""
        for pattern in self.TIME_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        time_match = re.search(r'(?:time)[:\s]+([^\n]+)', text, re.IGNORECASE)
        if time_match:
            return time_match.group(1).strip()

        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract meeting location."""
        location_match = re.search(
            r'(?:location|venue|room|where)[:\s]+([^\n]+)',
            text,
            re.IGNORECASE
        )
        if location_match:
            return location_match.group(1).strip()

        # Check for virtual meeting indicators
        if re.search(r'(?:zoom|teams|meet\.google|slack huddle)', text, re.IGNORECASE):
            return "Virtual"

        return None

    def _extract_organizer(self, text: str) -> Optional[str]:
        """Extract meeting organizer."""
        organizer_match = re.search(
            r'(?:organizer|facilitator|host|chair)[:\s]+([^\n]+)',
            text,
            re.IGNORECASE
        )
        if organizer_match:
            return organizer_match.group(1).strip()
        return None

    def _extract_attendees(self, text: str) -> List[Attendee]:
        """Extract list of attendees."""
        attendees = []

        for pattern in self.ATTENDEE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Parse attendee string
                attendee_str = match.group(1) if match.lastindex else match.group(0)

                # Split by common delimiters
                names = re.split(r'[,;]', attendee_str)

                for name in names:
                    name = name.strip()
                    if name and len(name) > 1:
                        # Check for role in parentheses
                        role_match = re.search(r'(\w+)\s*\(([^)]+)\)', name)
                        if role_match:
                            attendees.append(Attendee(
                                name=role_match.group(1).strip(),
                                role=role_match.group(2).strip()
                            ))
                        else:
                            attendees.append(Attendee(name=name))

        return attendees

    def _extract_topics(self, text: str) -> List[str]:
        """Extract meeting topics/agenda items."""
        topics = []

        # Look for agenda section
        agenda_match = re.search(
            r'(?:agenda|topics|discussion items)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if agenda_match:
            agenda_text = agenda_match.group(1)
            # Extract numbered or bulleted items
            items = re.findall(r'(?:\d+\.|[-*])\s*([^\n]+)', agenda_text)
            topics.extend([item.strip() for item in items if item.strip()])

        # Also look for heading-style topics
        heading_topics = re.findall(r'^#+\s*([^\n]+)', text, re.MULTILINE)
        for topic in heading_topics:
            topic = topic.strip()
            # Skip common non-topic headings
            if topic.lower() not in ['attendees', 'date', 'time', 'location', 'action items', 'next steps']:
                if topic not in topics:
                    topics.append(topic)

        return topics

    def _extract_discussions(self, text: str, topics: List[str]) -> Dict[str, str]:
        """Extract discussion content for each topic."""
        discussions = {}

        # If we have topics, try to find content between them
        if topics:
            for i, topic in enumerate(topics):
                # Find section for this topic
                pattern = rf'{re.escape(topic)}.*?(?=' + '|'.join([re.escape(t) for t in topics[i+1:]] + [r'\n\n\n', r'$']) + ')'
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(0)
                    # Remove the topic itself
                    content = re.sub(rf'^{re.escape(topic)}\s*', '', content, flags=re.IGNORECASE)
                    discussions[topic] = content.strip()

        return discussions

    def _extract_decisions(self, text: str) -> List[Decision]:
        """Extract decisions made in the meeting."""
        decisions = []

        for pattern in self.DECISION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decision_text = match.group(1).strip()
                decisions.append(Decision(description=decision_text))

        return decisions

    def _extract_action_items(self, text: str) -> List[ActionItem]:
        """Extract action items from meeting notes."""
        action_items = []

        for pattern in self.ACTION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()

                if len(groups) == 2:
                    # Pattern with owner and task
                    owner, task = groups
                    action_items.append(ActionItem(
                        task=task.strip(),
                        owner=owner.strip() if owner else None,
                    ))
                elif len(groups) == 1:
                    # Pattern with just task
                    task = groups[0].strip()

                    # Try to find owner in surrounding context
                    owner = self._find_owner_in_context(text, match.start())

                    action_items.append(ActionItem(
                        task=task,
                        owner=owner,
                    ))

        return action_items

    def _find_owner_in_context(self, text: str, position: int) -> Optional[str]:
        """Try to find owner name near an action item."""
        # Look backwards for names
        context = text[max(0, position - 100):position]
        name_match = re.search(r'(\w+)\s+(?:will|to)\s+$', context)
        if name_match:
            return name_match.group(1)
        return None

    def _extract_blockers(self, text: str) -> List[str]:
        """Extract blockers and risks."""
        blockers = []

        for pattern in self.BLOCKER_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                blocker = match.group(1).strip()
                if blocker:
                    blockers.append(blocker)

        return blockers

    def _extract_next_meeting(self, text: str) -> Optional[str]:
        """Extract next meeting info."""
        next_match = re.search(
            r'(?:next meeting|follow.?up)[:\s]+([^\n]+)',
            text,
            re.IGNORECASE
        )
        if next_match:
            return next_match.group(1).strip()
        return None


if __name__ == "__main__":
    # Example usage
    sample_notes = """
    Project Status Meeting - January 15, 2024

    Date: January 15, 2024
    Time: 2:00 PM - 3:00 PM
    Location: Conference Room A

    Attendees: John Smith (PM), Sarah Johnson (Dev), Mike Brown (QA), Lisa Chen (Designer)

    Agenda:
    1. Sprint Progress Review
    2. Blockers Discussion
    3. Next Sprint Planning

    Sprint Progress Review
    - Completed 8 of 10 planned stories
    - Velocity slightly below target
    - Sarah will finish the remaining API endpoints by Friday

    Blockers Discussion
    - Blocked by: API documentation is incomplete
    - Risk: Third-party integration may be delayed
    - Decision: We will postpone the third-party feature to next sprint

    Action Items
    - [Sarah] Complete API documentation by Jan 17
    - [Mike] Set up testing environment by Jan 18
    - John to send status report to stakeholders

    Next Meeting: January 22, 2024 at 2:00 PM
    """

    parser = MeetingParser()
    meeting = parser.parse(sample_notes)

    print(f"Title: {meeting.title}")
    print(f"Date: {meeting.date}")
    print(f"Attendees: {[a.name for a in meeting.attendees]}")
    print(f"Topics: {meeting.topics}")
    print(f"Action Items: {[f'{a.task} (Owner: {a.owner})' for a in meeting.action_items]}")
    print(f"Decisions: {[d.description for d in meeting.decisions]}")
    print(f"Blockers: {meeting.blockers}")