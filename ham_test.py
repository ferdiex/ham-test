import streamlit as st
import json
import random
import time
import collections

# Load questions from the JSON file (handling new structure with metadata)
with open("Elemento-2-2022-2026.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # Load full JSON object (including _meta if present)
    if isinstance(data, list):  # Handle the case where the JSON is a simple array
        questions = data  # Legacy format: entire file contains questions
    else:
        questions = data.get("questions", [])  # New format: extract "questions" keyf)

def reset_state(state_key):
    """Reset a specific Streamlit state."""
    if state_key in st.session_state:
        del st.session_state[state_key]

# App Configuration
st.set_page_config(page_title="FCC Technician Exam", layout="centered")
st.title("📡 FCC Technician Exam Simulator")
st.write("Practice test based on the official 2022–2026 question pool.")

# Extract unique sections for filtering
all_sections = list(set(q["id"][:2] for q in questions))
all_sections.sort()

# Mode selector
new_mode = st.radio("Choose mode:", ["Study", "Practice", "Exam"], key="mode_select")

# Reset state on mode change
if "current_mode" in st.session_state and new_mode != st.session_state.current_mode:
    reset_state("exam_state")
    reset_state("practice_state")
    reset_state("study_state")
st.session_state.current_mode = new_mode

### STUDY MODE ###
if new_mode == "Study":
    st.subheader("Study Mode - Review Questions")

    if "study_state" not in st.session_state:
        st.session_state.study_state = {"filtered_questions": questions}

    # "Select All Sections" toggle
    select_all = st.checkbox("Select All Sections", value=True, key="study_select_all")
    
    # Dynamically enforce select_all logic
    selected_sections = all_sections if select_all else st.multiselect(
        "Select sections to study:",
        options=all_sections,
        default=all_sections  # If not select_all, use dropdown for manual selection
    )

    # Apply filtering logic dynamically
    filtered_questions = [
        q for q in questions if q["id"][:2] in selected_sections
    ]
    st.session_state.study_state["filtered_questions"] = filtered_questions

    # Display filtered questions
    st.caption(f"Showing {len(filtered_questions)} questions.")
    for q in filtered_questions:
        st.write(f"### Question {q['id']} - {q['question']}")
        if q.get("image"):
            st.image(q["image"], caption=f"Figure for {q['id']}", width=600)
        st.write("Options:")
        for opt in q["options"]:
            st.write(opt)
        st.write(f"✅ Correct answer: {q['correct_answer']}")
        st.write("---")

### PRACTICE MODE ###
elif new_mode == "Practice":
    st.subheader("Practice Mode - Flexible Training")

    if "practice_state" not in st.session_state:
        st.session_state.practice_state = {"selected_questions": [], "answers": {}, "graded": False}

    state = st.session_state.practice_state

    # "Select All Sections" behavior
    select_all = st.checkbox("Select All Sections", value=True)
    if select_all:
        st.caption("Note: 'Select All Sections' is active. Manual deselections will not apply.")

    selected_sections = st.multiselect(
        "Select sections for practice:", options=all_sections, default=all_sections if select_all else []
    )

    # Filter questions based on selected sections
    filtered_questions = [q for q in questions if q["id"][:2] in selected_sections]

    # Dynamically adjust slider based on filtered questions
    max_questions = len(filtered_questions)
    if max_questions == 0:
        st.warning("No questions available for the selected sections.")
        num_questions = 0
    else:
        num_questions = st.slider(
            "Number of questions to practice:",
            min_value=1,  # Minimum is 1 question instead of 10
            max_value=max_questions,
            step=1,
            value=min(max_questions, 10)  # Default value is the smaller of 10 or the maximum count
        )

    # Ensure the number of selected questions equals slider value
    if len(state["selected_questions"]) != num_questions:
        state["selected_questions"] = filtered_questions[:num_questions]

    # Render questions & preserve answers
    st.caption(f"Displaying {len(state['selected_questions'])} questions based on your filter and slider selection.")
    for idx, q in enumerate(state["selected_questions"], start=1):
        st.write(f"### Question {idx}: {q['id']} - {q['question']}")
        if q.get("image"):
            st.image(q["image"], caption=f"Figure for {q['id']}", width=600)
        state["answers"][q["id"]] = st.radio(
            "Choose your answer:", q["options"], key=f"practice_{q['id']}"
        )

    # Grade button
    if st.button("Grade Practice"):
        score = 0
        weak_areas = collections.Counter()
        for q in state["selected_questions"]:
            selected_answer = state["answers"].get(q["id"], "")
            if selected_answer.startswith(q["correct_answer"]):
                score += 1
            else:
                weak_areas[q["id"][:2]] += 1

        state["graded"] = True
        st.success(f"**You scored: {score}/{num_questions}**")

        # Display weak areas report
        st.subheader("Weak Areas:")
        for section, count in weak_areas.items():
            st.write(f"Section {section}: {count} incorrect")

### EXAM MODE ###
elif new_mode == "Exam":
    st.subheader("Exam Mode - Official Simulation")

    if "exam_state" not in st.session_state:
        st.session_state.exam_state = {
            "started": False,
            "selected_questions": [],
            "answers": {},
            "graded": False,
            "start_time": None,
            "end_time": None
        }

    state = st.session_state.exam_state

    # Show Restart Exam button only if the exam has started
    if state["started"]:
        if st.button("Restart Exam"):
            reset_state("exam_state")
            st.rerun()

    # Start Exam button
    if not state["started"] and st.button("Start Exam"):
        # Generate a full exam
        exam_pool = collections.defaultdict(list)
        for q in questions:
            exam_pool[q["id"][:2]].append(q)

        selected_questions = []
        question_distribution = {"T1": 6, "T2": 3, "T3": 3, "T4": 3, "T5": 4, "T6": 4, "T7": 4, "T8": 3, "T9": 3, "T0": 2}
        for section, count in question_distribution.items():
            selected_questions.extend(random.sample(exam_pool[section], min(count, len(exam_pool[section]))))

        state["selected_questions"] = selected_questions
        state["started"] = True
        state["start_time"] = time.time()
        state["end_time"] = state["start_time"] + 600  # 10-minute timer
        st.rerun()

    # Render exam questions
    if state["started"]:
        remaining_time = int(state["end_time"] - time.time())
        minutes, seconds = divmod(max(0, remaining_time), 60)
        st.write(f"**Time Remaining: {minutes:02d}:{seconds:02d}**")

        for idx, q in enumerate(state["selected_questions"], start=1):
            st.write(f"### Question {idx}: {q['id']} - {q['question']}")
            if q.get("image"):
                st.image(q["image"], caption=f"Figure for {q['id']}", width=600)
            state["answers"][q["id"]] = st.radio(
                "Choose your answer:", q["options"], key=f"exam_{q['id']}"
            )

        # Grade button
        if st.button("Submit Exam"):
            score = sum(1 for q in state["selected_questions"] if state["answers"].get(q["id"], "").startswith(q["correct_answer"]))
            state["graded"] = True
            st.success(f"**You scored: {score}/35**")

            weak_areas = collections.Counter()
            for q in state["selected_questions"]:
                if not state["answers"].get(q["id"], "").startswith(q["correct_answer"]):
                    weak_areas[q["id"][:2]] += 1

            st.subheader("Weak Areas:")
            for section, count in weak_areas.items():
                st.write(f"Section {section}: {count} incorrect")
