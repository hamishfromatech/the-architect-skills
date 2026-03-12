"""
Priority Scorer - Calculate priority scores for tasks.

This module provides utilities for scoring and prioritizing tasks
using various prioritization methodologies.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Callable
import math


class Priority(Enum):
    """Priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKLOG = "backlog"


class EisenhowerQuadrant(Enum):
    """Eisenhower Matrix quadrants."""
    DO = "do_first"           # Important + Urgent
    SCHEDULE = "schedule"      # Important + Not Urgent
    DELEGATE = "delegate"      # Not Important + Urgent
    ELIMINATE = "eliminate"    # Not Important + Not Urgent


class MoSCoWPriority(Enum):
    """MoSCoW prioritization levels."""
    MUST = "must_have"
    SHOULD = "should_have"
    COULD = "could_have"
    WONT = "wont_have"


@dataclass
class Task:
    """A task with priority-related attributes."""
    id: str
    title: str
    description: str = ""
    deadline: Optional[datetime] = None
    estimated_hours: float = 1.0
    impact: int = 5  # 1-10 scale
    urgency: int = 5  # 1-10 scale
    effort: int = 5  # 1-10 scale (higher = more effort needed)
    dependencies: List[str] = None
    tags: List[str] = None
    assignee: Optional[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []


@dataclass
class PrioritizedTask:
    """A task with calculated priority scores."""
    task: Task
    weighted_score: float
    eisenhower_quadrant: EisenhowerQuadrant
    moscow_priority: MoSCoWPriority
    priority_level: Priority
    priority_label: str


class PriorityScorer:
    """Calculate priority scores for tasks."""

    # Default weights for weighted scoring
    DEFAULT_WEIGHTS = {
        "impact": 0.4,
        "urgency": 0.3,
        "effort": 0.2,
        "dependencies": 0.1,
    }

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        custom_scorer: Optional[Callable[[Task], float]] = None,
    ):
        """
        Initialize the priority scorer.

        Args:
            weights: Custom weights for scoring factors
            custom_scorer: Custom scoring function
        """
        self.weights = {**self.DEFAULT_WEIGHTS, **(weights or {})}
        self.custom_scorer = custom_scorer

    def score_task(self, task: Task) -> PrioritizedTask:
        """
        Calculate priority score for a single task.

        Args:
            task: Task to score

        Returns:
            PrioritizedTask with calculated scores
        """
        # Calculate weighted score
        weighted_score = self._calculate_weighted_score(task)

        # Determine Eisenhower quadrant
        eisenhower = self._determine_eisenhower_quadrant(task)

        # Determine MoSCoW priority
        moscow = self._determine_moscow_priority(task)

        # Determine overall priority level
        priority_level = self._determine_priority_level(weighted_score, task)

        # Generate priority label
        priority_label = self._generate_priority_label(priority_level, weighted_score)

        return PrioritizedTask(
            task=task,
            weighted_score=weighted_score,
            eisenhower_quadrant=eisenhower,
            moscow_priority=moscow,
            priority_level=priority_level,
            priority_label=priority_label,
        )

    def score_tasks(self, tasks: List[Task]) -> List[PrioritizedTask]:
        """
        Calculate priority scores for multiple tasks.

        Args:
            tasks: List of tasks to score

        Returns:
            List of PrioritizedTasks sorted by score (descending)
        """
        scored = [self.score_task(task) for task in tasks]
        return sorted(scored, key=lambda x: x.weighted_score, reverse=True)

    def _calculate_weighted_score(self, task: Task) -> float:
        """
        Calculate weighted priority score.

        Formula:
        Score = (Impact * w_impact) + (Urgency * w_urgency) -
                (Effort * w_effort) + (Dependency Bonus * w_dep)

        Higher score = Higher priority
        """
        if self.custom_scorer:
            return self.custom_scorer(task)

        # Normalize values to 0-1 scale
        impact_norm = task.impact / 10
        urgency_norm = task.urgency / 10
        effort_norm = task.effort / 10

        # Invert effort (lower effort = higher priority)
        effort_score = 1 - effort_norm

        # Dependency bonus (tasks that unblock others get higher priority)
        dep_bonus = min(len(task.dependencies) * 0.1, 0.5)  # Cap at 0.5

        # Calculate weighted score
        score = (
            impact_norm * self.weights["impact"] +
            urgency_norm * self.weights["urgency"] +
            effort_score * self.weights["effort"] +
            dep_bonus * self.weights["dependencies"]
        )

        # Apply deadline urgency multiplier
        if task.deadline:
            days_until = (task.deadline - datetime.now()).days
            if days_until <= 1:
                score *= 1.5
            elif days_until <= 3:
                score *= 1.3
            elif days_until <= 7:
                score *= 1.1

        return round(score, 2)

    def _determine_eisenhower_quadrant(self, task: Task) -> EisenhowerQuadrant:
        """
        Determine Eisenhower Matrix quadrant for a task.

        Uses impact for importance and urgency directly.
        """
        is_important = task.impact >= 6
        is_urgent = task.urgency >= 6

        if is_important and is_urgent:
            return EisenhowerQuadrant.DO
        elif is_important and not is_urgent:
            return EisenhowerQuadrant.SCHEDULE
        elif not is_important and is_urgent:
            return EisenhowerQuadrant.DELEGATE
        else:
            return EisenhowerQuadrant.ELIMINATE

    def _determine_moscow_priority(self, task: Task) -> MoSCoWPriority:
        """
        Determine MoSCoW priority for a task.

        Based on impact and urgency combination.
        """
        combined_score = task.impact + task.urgency

        if combined_score >= 15:
            return MoSCoWPriority.MUST
        elif combined_score >= 11:
            return MoSCoWPriority.SHOULD
        elif combined_score >= 7:
            return MoSCoWPriority.COULD
        else:
            return MoSCoWPriority.WONT

    def _determine_priority_level(
        self,
        score: float,
        task: Task,
    ) -> Priority:
        """
        Determine overall priority level based on score and deadline.
        """
        # Immediate deadline check
        if task.deadline:
            days_until = (task.deadline - datetime.now()).days
            if days_until <= 1:
                return Priority.CRITICAL

        # Score-based determination
        if score >= 0.8:
            return Priority.HIGH
        elif score >= 0.5:
            return Priority.MEDIUM
        elif score >= 0.3:
            return Priority.LOW
        else:
            return Priority.BACKLOG

    def _generate_priority_label(self, priority: Priority, score: float) -> str:
        """Generate human-readable priority label."""
        labels = {
            Priority.CRITICAL: "🔴 Critical - Do Immediately",
            Priority.HIGH: "🟠 High - Do Today",
            Priority.MEDIUM: "🟡 Medium - Do This Week",
            Priority.LOW: "🟢 Low - Schedule When Possible",
            Priority.BACKLOG: "⚪ Backlog - Future Consideration",
        }
        return f"{labels[priority]} (Score: {score:.2f})"


class TaskPrioritizer:
    """High-level task prioritization with multiple methods."""

    def __init__(self):
        """Initialize the task prioritizer."""
        self.scorer = PriorityScorer()

    def prioritize_eisenhower(
        self,
        tasks: List[Task],
    ) -> Dict[EisenhowerQuadrant, List[Task]]:
        """
        Categorize tasks using Eisenhower Matrix.

        Args:
            tasks: List of tasks to categorize

        Returns:
            Dictionary mapping quadrants to task lists
        """
        result = {q: [] for q in EisenhowerQuadrant}

        for task in tasks:
            scored = self.scorer.score_task(task)
            result[scored.eisenhower_quadrant].append(task)

        return result

    def prioritize_moscow(
        self,
        tasks: List[Task],
    ) -> Dict[MoSCoWPriority, List[Task]]:
        """
        Categorize tasks using MoSCoW method.

        Args:
            tasks: List of tasks to categorize

        Returns:
            Dictionary mapping priorities to task lists
        """
        result = {p: [] for p in MoSCoWPriority}

        for task in tasks:
            scored = self.scorer.score_task(task)
            result[scored.moscow_priority].append(task)

        return result

    def get_priority_list(
        self,
        tasks: List[Task],
    ) -> List[PrioritizedTask]:
        """
        Get tasks sorted by priority score.

        Args:
            tasks: List of tasks to prioritize

        Returns:
            Sorted list of prioritized tasks
        """
        return self.scorer.score_tasks(tasks)

    def generate_daily_plan(
        self,
        tasks: List[Task],
        work_hours: int = 8,
    ) -> Dict[str, List[Task]]:
        """
        Generate a daily plan based on priorities.

        Args:
            tasks: List of tasks to plan
            work_hours: Available work hours

        Returns:
            Dictionary with time blocks and tasks
        """
        scored_tasks = self.scorer.score_tasks(tasks)
        plan = {
            "morning": [],  # Deep work (high priority)
            "afternoon": [],  # Meetings & communications
            "end_of_day": [],  # Review & planning
        }

        hours_used = 0

        for prioritized in scored_tasks:
            task = prioritized.task

            if hours_used + task.estimated_hours <= work_hours * 0.4:
                # Morning: High priority deep work
                plan["morning"].append(task)
            elif hours_used + task.estimated_hours <= work_hours * 0.7:
                # Afternoon: Medium priority
                plan["afternoon"].append(task)
            else:
                # End of day: Review and planning
                plan["end_of_day"].append(task)

            hours_used += task.estimated_hours

        return plan

    def format_priority_report(
        self,
        tasks: List[Task],
    ) -> str:
        """
        Generate a formatted priority report.

        Args:
            tasks: List of tasks to include

        Returns:
            Formatted report string
        """
        scored_tasks = self.scorer.score_tasks(tasks)

        lines = ["# Priority Task List\n"]

        # Group by priority level
        by_priority = {p: [] for p in Priority}
        for prioritized in scored_tasks:
            by_priority[prioritized.priority_level].append(prioritized)

        for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            tasks_at_level = by_priority[priority]
            if tasks_at_level:
                lines.append(f"\n## {priority.value.upper()} Priority\n")
                for prioritized in tasks_at_level:
                    task = prioritized.task
                    deadline_str = ""
                    if task.deadline:
                        deadline_str = f" - Due: {task.deadline.strftime('%Y-%m-%d')}"
                    lines.append(
                        f"- {task.title}{deadline_str} "
                        f"(Score: {prioritized.weighted_score:.2f})"
                    )

        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    tasks = [
        Task(
            id="1",
            title="Fix critical production bug",
            description="Production system is down",
            deadline=datetime.now() + timedelta(hours=4),
            impact=10,
            urgency=10,
            effort=3,
        ),
        Task(
            id="2",
            title="Write quarterly report",
            description="Q4 report for stakeholders",
            deadline=datetime.now() + timedelta(days=5),
            impact=7,
            urgency=6,
            effort=5,
        ),
        Task(
            id="3",
            title="Review team PRs",
            description="Code review for team",
            impact=5,
            urgency=4,
            effort=3,
        ),
        Task(
            id="4",
            title="Update documentation",
            description="Update API documentation",
            impact=3,
            urgency=2,
            effort=4,
        ),
    ]

    prioritizer = TaskPrioritizer()
    print(prioritizer.format_priority_report(tasks))