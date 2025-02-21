import streamlit as st
import pandas as pd


st.set_page_config(page_title="Epic Study Planner", layout="wide")


st.markdown("""
    <style>
        
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        body {
            font-family: 'Orbitron', sans-serif !important;
            background-color: #0a0a0a;
            color: #ffffff;
            margin: 0;
            padding: 0;
            text-align: center;
        }


        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ff88;
            margin-bottom: 10px;
        }

        h2 {
            font-size: 1.5rem;
            color: #ffffff;
            margin-bottom: 20px;
        }

      
        .bold-label {
            font-weight: bold;
            font-size: 1.2rem;
            color: #ffffff;
        }

.stButton>button {
    background: rgba(255, 255, 255, 0.1); /* شفاف جزئي */
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    padding: 12px 40px;
    border-radius: 12px;
    color: #ffffff;
    font-weight: 700;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    width: auto;
    margin: 10px auto;
    display: block;
    text-align: center;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.2); /* ظل خفيف */
}

.stButton>button:hover {
    background: rgba(255, 255, 255, 0.3); /* يزيد الوضوح عند التمرير */
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(255, 255, 255, 0.3);
}


    </style>
""", unsafe_allow_html=True)

def home_page():
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.markdown("<h1>Epic Study Planner</h1>", unsafe_allow_html=True)
    st.markdown("Study strategically, manage your time wisely, and unlock your full learning potential", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Planning"):
            st.session_state.page = "input"
            st.rerun()
    with col2:
        if st.button("Contact Us"):
            st.session_state.page = "contact"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def input_page():
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.markdown("<h1> Enter Your Study Details</h1>", unsafe_allow_html=True)

    st.markdown("<div class='bold-label'><br><h3>Number of Subjects</h3></div>", unsafe_allow_html=True)
    num_subjects = st.number_input("", min_value=1, value=1, step=1, key="num_subjects")

    subjects = []
    
    for i in range(num_subjects):
        st.markdown(f"<h3>Subject {i+1}</h3>", unsafe_allow_html=True)
        name = st.text_input(f"Subject {i+1} Name", key=f"name_{i}")
        difficulty = st.slider(f"Difficulty (1 = very easy, 5 = very hard)", 1, 5, 3, key=f"difficulty_{i}")
        aversion = st.slider(f"Aversion (1 = like, 5 = hate)", 1, 5, 3, key=f"aversion_{i}")
        importance = st.slider(f"Importance (1 = not important, 5 = crucial)", 1, 5, 3, key=f"importance_{i}")
        subjects.append({"name": name, "difficulty": difficulty, "aversion": aversion, "importance": importance})

    st.markdown("<div class='bold-label'><h3>Total Study Hours Available</h3></div>", unsafe_allow_html=True)
    total_hours = st.number_input("", min_value=1, value=10, step=1, key="total_hours")

    st.session_state.study_data = {"subjects": subjects, "study_hours": total_hours}

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Calculate Allocation"):
            df = pd.DataFrame(subjects)
            df["priority"] = (df["difficulty"] + df["importance"]) + df["aversion"]
            df["priority"] = df["priority"].apply(lambda x: max(x, 1))
            total_priority = df["priority"].sum()
            df["allocated_hours"] = (df["priority"] / total_priority) * total_hours
            st.session_state.allocation = df
            st.session_state.page = "results"
            st.rerun()
    with col2:
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def results_page():
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.markdown("<h1>Study Allocation Results</h1>", unsafe_allow_html=True)

    if st.session_state.allocation is None:
        st.warning("No allocation data available. Please enter your study details first.")
        if st.button("Go to Input"):
            st.session_state.page = "input"
            st.rerun()
    else:
        df = st.session_state.allocation
        st.write("Your personalized study plan:")
        st.dataframe(df[["name", "difficulty", "aversion", "importance", "allocated_hours"]])

        for idx, row in df.iterrows():
            st.write(f"**{row['name']}**: {round(row['allocated_hours'], 2)} hours/day")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Input"):
            st.session_state.page = "input"
            st.rerun()
    with col2:
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def contact_page():
    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.markdown("<h1>Contact Us</h1>", unsafe_allow_html=True)
    st.write("Have questions or suggestions? We'd love to hear from you!")
    st.write("📧 **Email:** h_belaib@estin.dz")
    st.write("📸 **Instagram:** [Developer](https://www.instagram.com/bl._.haitem/)")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "input":
    input_page()
elif st.session_state.page == "results":
    results_page()
elif st.session_state.page == "contact":
    contact_page()
