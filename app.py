import os
import time
import json
import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv
from random import choice
from google.generativeai import configure, GenerativeModel
from streamlit_extras.colored_header import colored_header
from streamlit_extras.tags import tagger_component
from st_pages import Page, hide_pages, show_pages
from streamlit_extras.mention import mention

load_dotenv(".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.6,
    # "top_p": 1,
    # "top_k": 1,
    # "max_output_tokens": 10,
}


model = GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)


def gemini_prompt(subject_email, body_email, testing=False):
    """
    Generate a prompt for analyzing email emotions.

    Args:
        subject_email (str): Subject of the email.
        body_email (str): Body of the email.
        testing (bool, optional): Whether the function is used for testing purposes. Defaults to False.

    Returns:
        str: Generated response containing emotions.
    """
    if testing:
        return """
        Emotions shared in the email:

        Concern: The sender expresses concerns about the current work environment.
        Disappointment: The sender is disappointed with the lack of teamwork, unprofessional behavior, and disparity in workload.
        Frustration: The sender is frustrated with the breakdown of communication, lack of recognition, and unfair workload distribution.
        Resentment: The sender feels resentment toward colleagues who are not carrying their fair share of the workload.
        Demotivation: The sender feels demotivated due to the lack of recognition and appreciation.
        Unease: The sender is uneasy about the unprofessional behavior and disrespect among colleagues.
        Disengagement: The sender is disengaged from their work and team due to the negative work environment.
        Urgency: The sender conveys a sense of urgency in resolving the issues.
        emotions_list = [ {'emotion': 'Concern', 'percentage_of_appear': '20%'}, {'emotion': 'Disappointment', 'percentage_of_appear': '15%'}, {'emotion': 'Frustration', 'percentage_of_appear': '25%'}, {'emotion': 'Resentment', 'percentage_of_appear': '10%'}, {'emotion': 'Demotivation', 'percentage_of_appear': '10%'}, {'emotion': 'Unease', 'percentage_of_appear': '5%'}, {'emotion': 'Disengagement', 'percentage_of_appear': '5%'}, {'emotion': 'Urgency', 'percentage_of_appear': '10%'}, ]   
        """

    format_list = "emotions_list = [{''emotion':'emotion_name','percentage_of_appear':'percentage%'}]"

    prompt = f"""Your task is to analyze this email. The subject is: {subject_email}. The body is: {body_email}. Retrieve the emotions present in the email and return a list of emotions, explaining each one in short description, new line for separation. After that, provide recommendations for the person. Finally, write a list of emotions in array format like {format_list}, always ensuring the array is on a new line."""

    response = model.generate_content(prompt)

    return response.text


def custom_header(label, description):
    colored_header(
        label=label,
        description=description,
        color_name="violet-70",
    )


def intro():
    show_pages(
        [Page("app.py", "Home", "🛖"), Page("pages/about_us.py", "About us", "📲")]
    )

    st.set_page_config(
        page_title="AI EmotionAnalyzer 🚀",
        page_icon="✉️",
        initial_sidebar_state="collapsed",
    )
    with st.sidebar:
        mention(
            label="Github",
            icon="github",
            url="https://extras.streamlitapp.com",
        )
    st.title("AI EmotionAnalyzer 🚀")

    st.markdown(
        """
        # EmotionAnalyzer: Understand the Sentiment of Your Work Emails 👀✉️

        ## Introduction:

        Welcome to EmotionAnalyzer! We help you decode the emotions in your work emails 🚀. In today's fast-paced world, effective communication is key, and understanding the underlying sentiments can make a world of difference.

        Our cutting-edge tool utilizes advanced algorithms to analyze your emails, detecting tones like appreciation, frustration, urgency, and more 📊. With EmotionAnalyzer, you can:

        - **Gain Deeper Insights**: Uncover the true emotions behind the words 👁️.
        - **Enhance Communication**: Respond empathetically based on emotional context 🤝.
        - **Improve Efficiency**: Quickly identify critical emails and streamline your workflow 🚀.
        - **Foster Positive Work Culture**: Cultivate a supportive environment by addressing emotions head-on 🌟.
    """
    )

    # custom_header("Please input the subject and body of your email below","")


def parse_response(response_text):
    """
    Parse the response text to extract emotions list.

    Args:
        response_text (str): Response text from the model.

    Returns:
        tuple: Tuple containing parsed body and emotions list.
    """
    response_text = response_text.replace("```", "")
    body = response_text.split("emotions_list", 1)[0].replace(
        "Emotions in array format:", ""
    )
    emotions_list = (
        (response_text.split("emotions_list", 1)[1])
        .replace("\n", "")
        .replace("'", '"')
        .replace(" ", "")
        .replace("=", "")
        .replace("},]", "}]")
    )

    print((emotions_list))

    emotions_list = json.loads(emotions_list)

    return (body, emotions_list)


def bar_chart_emotions(emotions_list):
    """
    Display emotions list as a bar chart.

    Args:
        emotions_list (list): List of emotions with percentages.
    """
    df = pd.DataFrame(emotions_list)
    df.rename(
        columns={"percentage_of_appear": "Percentage", "emotion": "Emotions"},
        inplace=True,
    )
    df["Percentage"] = df["Percentage"].str.rstrip("%").astype("float") / 100
    df["Percentage_str"] = (df["Percentage"] * 100).astype(str) + "%"

    # Create chart
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("Emotions"),
            alt.Y("Percentage:Q", axis=alt.Axis(format="%")),
            alt.Color("Emotions"),
            alt.Tooltip(["Emotions", "Percentage_str"]),
            text=alt.Text("Percentage_str"),
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)


def emotions_list_display(emotions_list):
    """
    Display emotions list using Streamlit tagger component.

    Args:
        emotions_list (list): List of emotions.
    """
    emotions_list = [i["emotion"] for i in emotions_list]
    color_list_base = [
        "lightblue",
        "orange",
        "bluegreen",
        "blue",
        "violet",
        "red",
        "yellow",
    ]
    color_list_choice = []
    for i in range(len(emotions_list)):
        color_list_choice.append(choice(color_list_base))

    tagger_component(
        "",
        emotions_list,
        color_name=color_list_choice,
    )


def stream_data(response):
    """
    Stream data to Streamlit for displaying generated text.

    Args:
        response (str): Generated text to stream.
    """
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.08)


def ask_prompt():
    st.divider()
    st.markdown("#")
    st.write("### Please input the subject and body of your email below ✉️:")

    st.markdown("**Email Subject:**")
    email_subject = st.text_input(
        "Subject", value="", max_chars=100, key="email_subject"
    )
    st.markdown("**Email Body:**")
    email_body = st.text_area("Body", value="", height=200, key="email_body")
    if st.button("Analyze Emotions"):
        if len(email_subject) > 10 and len(email_body) > 10:
            try:
                response = gemini_prompt(email_subject, email_body, False)
                st.success("Successful analyzed!.", icon="✅")
                parser_response_text, emotions_list = parse_response(response)
                st.markdown("### **Here is a emotions identified:**")
                bar_chart_emotions(emotions_list)
                emotions_list_display(emotions_list)
                st.markdown("### **Result** ⌨️ :")
                st.write_stream(stream_data(parser_response_text))
            except Exception as e:
                st.error("An error ocurred, retry.", icon="🤖")
        else:
            st.error("Body and Subject must be greater than 10 characters.", icon="🤖")


intro()
ask_prompt()
