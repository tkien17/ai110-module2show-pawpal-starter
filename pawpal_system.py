from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str] = field(default_factory=list)

@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str  # high, medium, low
    category: str  # feeding, walking, grooming, etc.
    frequency: str  # daily, weekly, etc.

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
    preferences: Dict[str, str] = field(default_factory=dict)
    pet: Pet | None = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def edit_task(self, index: int, task: Task) -> None:
        if 0 <= index < len(self.tasks):
            self.tasks[index] = task
        else:
            raise IndexError("Task index out of range")

class Scheduler:
    def generate_plan(self, owner: Owner) -> Plan:
        prioritized = self._prioritize_tasks(owner.tasks)
        max_minutes = owner.available_hours_per_day * 60
        scheduled = self._schedule_tasks(prioritized, max_minutes)
        planned = Plan(scheduled_tasks=scheduled, total_time=sum((st.task.duration_minutes for st in scheduled)))
        return planned

    def _prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority.lower(), 3))

    def _schedule_tasks(self, tasks: List[Task], available_time: int) -> List[ScheduledTask]:
        scheduled = []
        current_minutes = 0
        start_base = 8 * 60

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
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"
