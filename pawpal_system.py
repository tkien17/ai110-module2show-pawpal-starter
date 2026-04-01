from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict

@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: str  # high, medium, low
    category: str  # feeding, walking, grooming, etc.
    frequency: str  # daily, weekly, etc.
    time: str = "00:00"  # HH:MM planned time for the task
    due_date: date | None = None
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

    def mark_task_complete(self, index: int) -> None:
        """Mark a task complete by index and, if recurring, create the next occurrence.

        For `frequency` equal to 'daily' or 'weekly', a new Task instance is created
        with the same attributes but with `due_date` advanced by the appropriate
        timedelta and `completed` set to False.
        """
        if not (0 <= index < len(self.tasks)):
            raise IndexError("Task index out of range")

        task = self.tasks[index]
        task.mark_complete()

        if task.frequency.lower() == "daily":
            delta = timedelta(days=1)
        elif task.frequency.lower() == "weekly":
            delta = timedelta(weeks=1)
        else:
            delta = None

        if delta is not None:
            next_due = (task.due_date or date.today()) + delta
            new_task = Task(
                name=task.name,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                category=task.category,
                frequency=task.frequency,
                time=task.time,
                due_date=next_due,
                completed=False,
            )
            self.tasks.append(new_task)

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
    pet_name: str | None = None

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

    def get_pending_tasks_with_pet(self) -> List[tuple[Pet, Task]]:
        """Return pending tasks paired with their pet."""
        items: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                if not task.completed:
                    items.append((pet, task))
        return items

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks across all owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

class Scheduler:
    def generate_plan(self, owner: Owner, start_time: str = "08:00", available_hours: int | None = None) -> Plan:
        """Generate a schedule for the owner's pending tasks within available time."""
        if available_hours is None:
            available_hours = owner.available_hours_per_day

        tasks_with_pet = owner.get_pending_tasks_with_pet()

        # Prioritize tasks (we only use the Task object for priority)
        tasks_with_pet_sorted = sorted(
            tasks_with_pet, key=lambda pt: {"high": 0, "medium": 1, "low": 2}.get(pt[1].priority.lower(), 3)
        )

        total_available_minutes = available_hours * 60
        scheduled = self._schedule_tasks(tasks_with_pet_sorted, total_available_minutes, start_time)
        total_time = sum((st.task.duration_minutes for st in scheduled))
        return Plan(scheduled_tasks=scheduled, total_time=total_time)
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by their `time` attribute (HH:MM strings).

        Uses a lambda as the `key` to convert the "HH:MM" string into a tuple
        of integers (hour, minute) so sorting behaves numerically.
        Example key: `lambda t: tuple(map(int, t.time.split(':')))`
        """
        return sorted(tasks, key=lambda t: tuple(map(int, t.time.split(":"))))

    def filter_tasks(self, owner: Owner, completed: bool | None = None, pet_name: str | None = None) -> List[Task]:
        """Filter tasks by completion status and/or by pet name.

        - If `pet_name` is provided, only tasks for that pet are considered.
        - If `completed` is None, do not filter by completion status.
        """
        if pet_name is not None:
            pets = [p for p in owner.pets if p.name == pet_name]
            tasks: List[Task] = []
            for p in pets:
                tasks.extend(p.tasks)
        else:
            tasks = owner.get_all_tasks()

        if completed is None:
            return tasks

        return [t for t in tasks if t.completed is completed]
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by their `time` attribute (HH:MM strings).

        Uses a lambda as the `key` to convert the "HH:MM" string into a tuple
        of integers (hour, minute) so sorting behaves numerically.
        Example key: `lambda t: tuple(map(int, t.time.split(':')))`
        """
        return sorted(tasks, key=lambda t: tuple(map(int, t.time.split(":"))))

    def filter_tasks(self, owner: Owner, completed: bool | None = None, pet_name: str | None = None) -> List[Task]:
        """Filter tasks by completion status and/or by pet name.

        - If `pet_name` is provided, only tasks for that pet are considered.
        - If `completed` is None, do not filter by completion status.
        """
        if pet_name is not None:
            pets = [p for p in owner.pets if p.name == pet_name]
            tasks: List[Task] = []
            for p in pets:
                tasks.extend(p.tasks)
        else:
            tasks = owner.get_all_tasks()

        if completed is None:
            return tasks

        return [t for t in tasks if t.completed is completed]
    def _prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Order tasks by priority (high, medium, low)."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority.lower(), 3))

    def _schedule_tasks(self, tasks_with_pet: List[tuple[Pet, Task]], available_time: int, start_time: str) -> List[ScheduledTask]:
        """Schedule tasks. If a Task has an explicit `time` (not "00:00"), schedule
        it at that time; otherwise schedule sequentially starting at `start_time`.

        Returns ScheduledTask objects that include the pet name for conflict checks.
        """
        scheduled: List[ScheduledTask] = []
        sequential_cursor = self._parse_time(start_time)
        used_minutes = 0

        for pet, task in tasks_with_pet:
            # If the task provides an explicit time, schedule there.
            if task.time != "00:00":
                start = self._parse_time(task.time)
                end = start + task.duration_minutes
            else:
                # Use sequential scheduling
                if used_minutes + task.duration_minutes > available_time:
                    break
                start = sequential_cursor + used_minutes
                end = start + task.duration_minutes
                used_minutes += task.duration_minutes

            scheduled.append(ScheduledTask(task=task, start_time=self._format_time(start), end_time=self._format_time(end), pet_name=pet.name))

        return scheduled

    def detect_conflicts(self, plan: Plan) -> List[str]:
        """Return lightweight warning messages for any overlapping scheduled tasks.

        This method checks each pair of scheduled tasks for time overlap and
        returns a list of human-readable warnings. It does not raise exceptions.
        """
        warnings: List[str] = []

        def to_minutes(ts: str) -> int:
            h, m = [int(x) for x in ts.split(":")]
            return h * 60 + m

        for i in range(len(plan.scheduled_tasks)):
            a = plan.scheduled_tasks[i]
            a_start = to_minutes(a.start_time)
            a_end = to_minutes(a.end_time)
            for j in range(i + 1, len(plan.scheduled_tasks)):
                b = plan.scheduled_tasks[j]
                b_start = to_minutes(b.start_time)
                b_end = to_minutes(b.end_time)

                # Overlap if start < other_end and other_start < end
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"Conflict: '{a.task.name}' (pet {a.pet_name}) overlaps with '{b.task.name}' (pet {b.pet_name}) at {a.start_time} - {a.end_time} / {b.start_time} - {b.end_time}"
                    )

        return warnings

    @staticmethod
    def _format_time(minutes: int) -> str:
        h = (minutes // 60) % 24
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def _parse_time(ts: str) -> int:
        hours, mins = [int(x) for x in ts.split(":")]
        return hours * 60 + mins

