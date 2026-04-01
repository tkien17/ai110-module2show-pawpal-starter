from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(name="Alex", available_hours_per_day=4)

    pet1 = Pet(name="Milo", species="Dog", age=3)
    pet2 = Pet(name="Luna", species="Cat", age=2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(name="Morning walk", duration_minutes=30, priority="high", category="walking", frequency="daily")
    task2 = Task(name="Feed wet food", duration_minutes=15, priority="medium", category="feeding", frequency="daily")
    task3 = Task(name="Brush coat", duration_minutes=20, priority="low", category="grooming", frequency="daily")

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, start_time="07:30", available_hours=3)

    print(plan.display_plan())


if __name__ == "__main__":
    main()