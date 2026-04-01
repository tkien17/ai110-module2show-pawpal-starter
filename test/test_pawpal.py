import pytest
from pawpal_system import Task, Pet


def test_task_mark_complete():
    task = Task(name="Feed", duration_minutes=10, priority="high", category="feeding", frequency="daily")
    assert not task.completed

    task.mark_complete()
    assert task.completed
    assert not task.is_due()


def test_pet_add_task_increases_count():
    pet = Pet(name="Milo", species="Dog", age=3)
    initial_count = len(pet.tasks)

    pet.add_task(Task(name="Walk", duration_minutes=30, priority="high", category="walking", frequency="daily"))
    assert len(pet.tasks) == initial_count + 1  


def test_sorting_by_time():
    from pawpal_system import Scheduler
    tasks = [
        Task(name="A", duration_minutes=10, priority="low", category="other", frequency="none", time="12:00"),
        Task(name="B", duration_minutes=10, priority="low", category="other", frequency="none", time="08:30"),
        Task(name="C", duration_minutes=10, priority="low", category="other", frequency="none", time="09:15"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)
    assert [t.time for t in sorted_tasks] == ["08:30", "09:15", "12:00"]


def test_daily_recurrence_creates_next_task():
    from datetime import date, timedelta

    pet = Pet(name="Luna", species="Cat", age=2)
    today = date.today()
    pet.add_task(Task(name="Feed", duration_minutes=5, priority="high", category="feeding", frequency="daily", due_date=today))

    initial_len = len(pet.tasks)
    pet.mark_task_complete(0)

    # A new task for the next day should have been appended
    assert len(pet.tasks) == initial_len + 1
    new_task = pet.tasks[-1]
    assert new_task.due_date == today + timedelta(days=1)
    assert not new_task.completed


def test_scheduler_detects_conflicts():
    from pawpal_system import Scheduler, ScheduledTask, Plan

    t1 = Task(name="Walk", duration_minutes=60, priority="high", category="walking", frequency="none", time="08:00")
    t2 = Task(name="Groom", duration_minutes=30, priority="low", category="grooming", frequency="none", time="08:30")

    st1 = ScheduledTask(task=t1, start_time="08:00", end_time="09:00", pet_name="Milo")
    st2 = ScheduledTask(task=t2, start_time="08:30", end_time="09:00", pet_name="Bella")

    plan = Plan(scheduled_tasks=[st1, st2], total_time=90)
    warnings = Scheduler().detect_conflicts(plan)

    assert len(warnings) >= 1
    assert warnings[0].startswith("Conflict:"), "Expected conflict warning message"