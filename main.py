from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def main() -> None:
    owner = Owner(name="Alex", available_hours_per_day=4)

    pet1 = Pet(name="Milo", species="Dog", age=3)
    pet2 = Pet(name="Luna", species="Cat", age=2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Intentionally add tasks out of chronological order to demonstrate sorting
    today = date.today()

    task1 = Task(name="Morning walk", duration_minutes=30, priority="high", category="walking", frequency="daily", time="09:30", due_date=today)
    task2 = Task(name="Feed wet food", duration_minutes=15, priority="medium", category="feeding", frequency="daily", time="08:15", due_date=today)
    task3 = Task(name="Brush coat", duration_minutes=20, priority="low", category="grooming", frequency="daily", time="07:45", due_date=today)
    task4 = Task(name="Evening play", duration_minutes=20, priority="medium", category="play", frequency="daily", time="19:00", due_date=today)
    # Add a conflicting task (same time as task1) for another pet to trigger warnings
    task5 = Task(name="Vet check", duration_minutes=30, priority="high", category="health", frequency="weekly", time="09:30", due_date=today)

    # Mark one task completed to demonstrate filtering
    task2.mark_complete()

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet1.add_task(task4)
    pet2.add_task(task5)

    scheduler = Scheduler()
    # Show pending tasks in insertion (unsorted) order
    pending = owner.get_pending_tasks()
    print("Pending tasks (unsorted):")
    for t in pending:
        print(f"- {t.name} at {t.time} (pet task)")

    # Sort pending tasks by time using the new method
    sorted_tasks = scheduler.sort_by_time(pending)
    print("\nPending tasks (sorted by time):")
    for t in sorted_tasks:
        print(f"- {t.name} at {t.time}")

    # Filter tasks by pet name
    milo_tasks = scheduler.filter_tasks(owner, pet_name="Milo")
    print("\nTasks for Milo:")
    for t in milo_tasks:
        status = "done" if t.completed else "pending"
        print(f"- {t.name} at {t.time} [{status}]")

    # Filter completed tasks
    completed_tasks = scheduler.filter_tasks(owner, completed=True)
    print("\nCompleted tasks:")
    for t in completed_tasks:
        print(f"- {t.name} at {t.time}")

    # Also show the generated plan to keep original behavior
    plan = scheduler.generate_plan(owner, start_time="07:30", available_hours=3)
    print("\nGenerated plan summary:")
    print(plan.display_plan())

    # Detect conflicts and print warnings (lightweight)
    warnings = scheduler.detect_conflicts(plan)
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print("- ", w)


if __name__ == "__main__":
    main()