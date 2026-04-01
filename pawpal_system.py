from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str  # high, medium, low
    category: str  # feeding, walking, grooming, etc.
    frequency: str  # daily, weekly, etc.
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_due(self) -> bool:
        """Return True when this task is still due."""
        return not self.completed

@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, index: int) -> None:
        """Remove a task by index from this pet."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
        else:
            raise IndexError("Task index out of range")

    def get_pending_tasks(self) -> List[Task]:
        """Get only the pending (not completed) tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

@dataclass
class ScheduledTask:
    task: Task
    start_time: str  # e.g., "08:00"
    end_time: str

@dataclass
class Plan:
    scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
    total_time: int = 0

    def display_plan(self) -> str:
        lines = [f"Daily plan (total {self.total_time} mins):"]
        for st in self.scheduled_tasks:
            lines.append(f"{st.start_time}-{st.end_time}: {st.task.name} ({st.task.category}, {st.task.priority})")
        return "\n".join(lines)

@dataclass
class Owner:
    name: str
    available_hours_per_day: int
    pets: List[Pet] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, index: int) -> None:
        """Remove a pet from the owner by index."""
        if 0 <= index < len(self.pets):
            self.pets.pop(index)
        else:
            raise IndexError("Pet index out of range")

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks for all pets belonging to this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks across all owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

class Scheduler:
    def generate_plan(self, owner: Owner, start_time: str = "08:00", available_hours: int | None = None) -> Plan:
        """Generate a schedule for the owner's pending tasks within available time."""
        if available_hours is None:
            available_hours = owner.available_hours_per_day

        tasks = owner.get_pending_tasks()
        prioritized = self._prioritize_tasks(tasks)
        total_available_minutes = available_hours * 60
        scheduled = self._schedule_tasks(prioritized, total_available_minutes, start_time)
        total_time = sum((st.task.duration_minutes for st in scheduled))
        return Plan(scheduled_tasks=scheduled, total_time=total_time)
    def _prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Order tasks by priority (high, medium, low)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority.lower(), 3))

    def _schedule_tasks(self, tasks: List[Task], available_time: int, start_time: str) -> List[ScheduledTask]:
        """Schedule tasks sequentially until the available slot is filled."""
        scheduled: List[ScheduledTask] = []
        current_minutes = 0
        start_base = self._parse_time(start_time)

        for task in tasks:
            if current_minutes + task.duration_minutes > available_time:
                break
            start = start_base + current_minutes
            end = start + task.duration_minutes
            scheduled.append(ScheduledTask(task=task, start_time=self._format_time(start), end_time=self._format_time(end)))
            current_minutes += task.duration_minutes

        return scheduled

    @staticmethod
    def _format_time(minutes: int) -> str:
        h = (minutes // 60) % 24
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def _parse_time(ts: str) -> int:
        hours, mins = [int(x) for x in ts.split(":")]
        return hours * 60 + mins

