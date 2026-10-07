import streamlit as st

from agent.graph import graph


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Job Research Agent",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------
# Header
# -----------------------------------

st.title("🤖 AI Job Research Agent")

st.write(
    "Find and analyze relevant jobs and internships using AI."
)


# -----------------------------------
# Job Roles
# -----------------------------------

job_roles = [
    "Software Engineer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "React Developer",
    "Python Developer",
    "Java Developer",
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "DevOps Engineer",
    "Cloud Engineer",
    "Cybersecurity Engineer",
    "Mobile App Developer",
    "UI/UX Designer",
    "Product Manager",
    "Business Analyst",
    "QA / Test Engineer",
    "Blockchain Developer",
]


# -----------------------------------
# Job Types
# -----------------------------------

job_types = [
    "Internship",
    "Full-time",
    "Part-time",
    "Contract",
    "Freelance",
]


# -----------------------------------
# Experience Levels
# -----------------------------------

experience_levels = [
    "Fresher / 0 years",
    "Entry Level / 0-1 year",
    "1-2 years",
    "2-3 years",
    "3-5 years",
    "5+ years",
]


# -----------------------------------
# User Inputs
# -----------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    job_role = st.selectbox(
        "Job Role",
        job_roles
    )


with col2:

    job_type = st.selectbox(
        "Job Type",
        job_types
    )


with col3:

    experience_level = st.selectbox(
        "Experience Level",
        experience_levels
    )


# -----------------------------------
# Skills
# -----------------------------------

skills = st.text_input(
    "Your Skills",
    placeholder="Python, Django, SQL, REST API, Git"
)


# -----------------------------------
# Location
# -----------------------------------

location = st.text_input(
    "Preferred Location",
    placeholder="Remote, India"
)


st.write("")


# -----------------------------------
# Search Button
# -----------------------------------

if st.button(
    "🔎 Find Jobs",
    use_container_width=True
):

    # -------------------------------
    # Validate Input
    # -------------------------------

    if not skills.strip():

        st.warning(
            "Please enter your skills."
        )

        st.stop()


    if not location.strip():

        st.warning(
            "Please enter your preferred location."
        )

        st.stop()


    # -------------------------------
    # Create User Query
    # -------------------------------

    user_query = f"""
Find {job_type} opportunities for the role of {job_role}.

Experience level:
{experience_level}

Candidate skills:
{skills}

Preferred location:
{location}
"""


    # -------------------------------
    # Run Agent
    # -------------------------------

    with st.spinner(
        "🤖 AI agent is researching jobs..."
    ):

        try:

            result = graph.invoke({

                "user_query": user_query,

                "query_analysis": "",

                "search_query": "",

                "search_results": [],

                "analyzed_jobs": [],

                "final_answer": ""
            })


        except Exception as e:

            st.error(
                "Something went wrong while running the AI agent."
            )

            st.exception(e)

            st.stop()


    # --------------------------------
    # Query Analysis
    # --------------------------------

    st.subheader(
        "🧠 AI Query Analysis"
    )

    st.write(
        result.get(
            "query_analysis",
            "No analysis available."
        )
    )


    # --------------------------------
    # Search Query
    # --------------------------------

    with st.expander(
        "🔎 View generated search query"
    ):

        st.code(
            result.get(
                "search_query",
                ""
            )
        )


    # --------------------------------
    # Job Recommendations
    # --------------------------------

    st.subheader(
        "🎯 Job Recommendations"
    )


    jobs = result.get(
        "analyzed_jobs",
        []
    )


    if not jobs:

        st.info(
            "No relevant jobs found. Try changing your search criteria."
        )


    else:

        # Sort jobs by match score
        jobs = sorted(
            jobs,
            key=lambda x: x.get(
                "match_score",
                0
            ),
            reverse=True
        )


        for index, job in enumerate(
            jobs,
            start=1
        ):

            with st.container(
                border=True
            ):

                # ------------------------
                # Title
                # ------------------------

                st.markdown(
                    f"### {index}. {job.get('title', 'Not specified')}"
                )


                # ------------------------
                # Company / Location
                # ------------------------

                st.write(
                    f"🏢 **Company:** "
                    f"{job.get('company', 'Not specified')}"
                )

                st.write(
                    f"📍 **Location:** "
                    f"{job.get('location', 'Not specified')}"
                )


                # ------------------------
                # Experience / Salary
                # ------------------------

                col_a, col_b = st.columns(2)


                with col_a:

                    st.write(
                        f"💼 **Experience:** "
                        f"{job.get('experience', 'Not specified')}"
                    )


                with col_b:

                    st.write(
                        f"💰 **Salary/Stipend:** "
                        f"{job.get('salary', 'Not specified')}"
                    )


                # ------------------------
                # Skills
                # ------------------------

                job_skills = job.get(
                    "skills",
                    []
                )


                if isinstance(
                    job_skills,
                    list
                ):

                    skills_text = ", ".join(
                        str(skill)
                        for skill in job_skills
                    )

                else:

                    skills_text = str(
                        job_skills
                    )


                st.write(
                    f"🛠️ **Required Skills:** "
                    f"{skills_text}"
                )


                # ------------------------
                # Match Score
                # ------------------------

                try:

                    score = int(
                        job.get(
                            "match_score",
                            0
                        )
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    score = 0


                score = max(
                    0,
                    min(
                        100,
                        score
                    )
                )


                st.write(
                    f"⭐ **Match Score: {score}%**"
                )


                st.progress(
                    score / 100
                )


                # ------------------------
                # Why It Matches
                # ------------------------

                st.write(
                    "**Why this matches:**"
                )

                st.write(
                    job.get(
                        "reason",
                        "Not specified"
                    )
                )


                # ------------------------
                # Apply Button
                # ------------------------

                url = job.get(
                    "url",
                    ""
                )


                if (
                    url
                    and url != "Not specified"
                ):

                    st.link_button(
                        "🚀 Apply Now",
                        url
                    )