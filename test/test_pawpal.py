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