import streamlit as st
import json
import random

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Programming Interview Bot",
    page_icon="💻",
    layout="centered"
)

# ---------------- LOAD QUESTIONS ----------------

with open("questions.json", "r") as file:
    questions = json.load(file)

# ---------------- TITLE ----------------

st.title("💻 Programming Interview Bot")
st.write("Test your programming knowledge with interview questions.")

# ---------------- SETTINGS ----------------

language = st.selectbox(
    "🌐 Select Programming Language",
    list(questions.keys())
)

difficulty = st.selectbox(
    "📊 Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

number_of_questions = st.selectbox(
    "🔢 Number of Questions",
    [2, 3, 5, 10]
)

# ---------------- START INTERVIEW ----------------

if st.button("🚀 Start Interview"):

    available_questions = questions[language][difficulty]

    count = min(number_of_questions, len(available_questions))

    selected_questions = random.sample(
        available_questions,
        count
    )

    st.session_state.selected_questions = selected_questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.results = []
    st.session_state.submitted = False
    st.session_state.started = True
    st.session_state.finished = False

    st.rerun()


# ---------------- INTERVIEW ----------------

if st.session_state.get("started", False) and not st.session_state.get("finished", False):

    selected_questions = st.session_state.selected_questions
    current = st.session_state.current_question

    total = len(selected_questions)

    st.divider()

    st.subheader(f"🎯 Question {current + 1} / {total}")

    st.progress((current + 1) / total)

    question_data = selected_questions[current]

    st.info(question_data["question"])

    user_answer = st.text_area(
        "✍️ Your Answer",
        key=f"answer_{current}",
        height=150
    )

    # ---------------- SUBMIT ----------------

    if not st.session_state.get("submitted", False):

        if st.button("✅ Submit Answer"):

            if user_answer.strip() == "":
                st.warning("Please enter your answer first.")

            else:

                correct_answer = question_data["answer"]

                user_words = set(user_answer.lower().split())
                correct_words = set(correct_answer.lower().split())

                common_words = user_words.intersection(correct_words)

                if len(common_words) >= 3:

                    st.session_state.score += 1

                    st.session_state.results.append(
                        {
                            "question": question_data["question"],
                            "result": "✅ Good Answer"
                        }
                    )

                    st.success("🎉 Good answer!")

                else:

                    st.session_state.results.append(
                        {
                            "question": question_data["question"],
                            "result": "❌ Needs Improvement"
                        }
                    )

                    st.warning("Your answer needs improvement.")

                st.session_state.submitted = True

                st.markdown("### 💡 Expected Answer")

                st.success(correct_answer)

    # ---------------- NEXT QUESTION ----------------

    if st.session_state.get("submitted", False):

        if current + 1 < total:

            if st.button("➡️ Next Question"):

                st.session_state.current_question += 1
                st.session_state.submitted = False

                st.rerun()

        else:

            if st.button("🏁 Finish Interview"):

                st.session_state.finished = True

                st.rerun()


# ---------------- FINAL RESULT ----------------

if st.session_state.get("finished", False):

    st.divider()

    st.title("🎉 Interview Completed!")

    score = st.session_state.score

    total = len(st.session_state.selected_questions)

    percentage = (score / total) * 100

    st.metric(
        "Your Score",
        f"{score} / {total}"
    )

    st.write(f"### 📊 Score: {percentage:.0f}%")

    # ---------------- PERFORMANCE ----------------

    if percentage >= 80:

        st.success(
            "🏆 Excellent! You are well prepared!"
        )

    elif percentage >= 60:

        st.info(
            "👍 Good job! Keep practicing."
        )

    else:

        st.warning(
            "📚 Keep practicing and improve your fundamentals."
        )

    # ---------------- QUESTION RESULTS ----------------

    st.subheader("📋 Question-wise Results")

    for index, result in enumerate(
        st.session_state.results,
        start=1
    ):

        st.write(
            f"**Question {index}:** "
            f"{result['result']}"
        )

        st.caption(
            result["question"]
        )

    # ---------------- NEW INTERVIEW ----------------

    if st.button("🔄 Start New Interview"):

        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.results = []

        st.rerun()