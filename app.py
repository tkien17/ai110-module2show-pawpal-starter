import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

st.markdown("### Pets & Tasks")
st.caption("Create pets and assign tasks; data persists in the session.")

# Persist or create Owner in session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_hours_per_day=4)
else:
    # keep owner name in sync with input
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name

owner = st.session_state.owner

# Add pet button
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    new_pet_name = st.text_input("New pet name", value=pet_name, key="new_pet_name")
with col_pet2:
    new_species = st.selectbox("New pet species", ["dog", "cat", "other"], key="new_species")

if st.button("Add pet"):
    pet = Pet(name=new_pet_name, species=new_species, age=age)
    owner.add_pet(pet)
    st.success(f"Added pet {pet.name}")

# Show existing pets
if owner.pets:
    st.write("Owner's pets:")
    for i, p in enumerate(owner.pets):
        st.write(f"{i}: {p.name} ({p.species}) — {len(p.tasks)} tasks")
else:
    st.info("No pets yet. Add a pet above.")

# Task inputs (assign to a selected pet)
if owner.pets:
    st.markdown("---")
    st.write("Add task and assign to a pet")
    pet_options = [p.name for p in owner.pets]
    selected_pet = st.selectbox("Select pet", pet_options)
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")

    if st.button("Add task to pet"):
        task = Task(name=task_title, duration_minutes=int(duration), priority=priority, category="general", frequency="daily")
        # find pet by name and add task
        for p in owner.pets:
            if p.name == selected_pet:
                p.add_task(task)
                st.success(f"Added task '{task.name}' to {p.name}")
                break

    # display tasks for selected pet
    for p in owner.pets:
        if p.name == selected_pet:
            if p.tasks:
                st.write(f"Tasks for {p.name}:")
                for t in p.tasks:
                    status = "done" if t.completed else "pending"
                    st.write(f"- {t.name} ({t.duration_minutes}m) — {t.priority} — {status}")
            else:
                st.info(f"No tasks for {p.name} yet.")

else:
    st.info("Add a pet to assign tasks to.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
