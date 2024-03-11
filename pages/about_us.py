import streamlit as st
from random import shuffle
from streamlit_extras.let_it_rain import rain
from streamlit_extras.mention import mention


# validators
def rain_emoji():
    rain(
        emoji="✨",
        font_size=54,
        falling_speed=5,
        animation_length="1s",
    )


rain_emoji()


def about_us():
    with st.sidebar:
        mention(
            label="Github",
            icon="github",
            url="https://github.com/itsfelipe-dev/AI-Work-Emails-EmotionAnalyzer",
        )
    st.title("About Us")
    st.write("Meet our team members and learn about our university careers!⭐️")

    team_members = [
        {
            "name": "Andres Orjuela",
            "img_url": "https://avatars.githubusercontent.com/u/72109168?v=4",
            "university_career": "Software Engineer",
        },
        {
            "name": "Cindy Rojas",
            "img_url": "https://play-lh.googleusercontent.com/7Ak4Ye7wNUtheIvSKnVgGL_OIZWjGPZNV6TP_3XLxHC-sDHLSE45aDg41dFNmL5COA=w240-h480-rw",
            "university_career": "Heathy Care",
        },
        {
            "name": "Jackeline Wilches",
            "img_url": "https://play-lh.googleusercontent.com/7Ak4Ye7wNUtheIvSKnVgGL_OIZWjGPZNV6TP_3XLxHC-sDHLSE45aDg41dFNmL5COA=w240-h480-rw",
            "university_career": "Business Administration",
        },
        {
            "name": "Maria Paula",
            "img_url": "https://play-lh.googleusercontent.com/7Ak4Ye7wNUtheIvSKnVgGL_OIZWjGPZNV6TP_3XLxHC-sDHLSE45aDg41dFNmL5COA=w240-h480-rw",
            "university_career": "Software Engineer",
        },
        {
            "name": "Daniel Osorio",
            "img_url": "https://image.lexica.art/full_jpg/f2b38753-493c-4658-84b4-bd672aef36c7",
            "university_career": "System Engineer",
        },
    ]
    shuffle(team_members)
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        cols[i % len(cols)].markdown(
            f"""<div style="margin-bottom: 3rem; border-radius: 10px;padding:3rem 2rem; text-align: center;width: 100%" >
                    <img src="{member["img_url"]}" style="border-radius: 50%; max-width: 90%; 	border: 3px solid #fbc458; display: block;margin-left: auto;margin-right: auto;margin-bottom: 1rem">
                    <p style="font-weight:bold;margin:0px; ">{member["name"]}</p>
                    <span style="font-size:0.9rem"> {member["university_career"]} </span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        # cols[i % len(cols)].write(member["name"])
        # cols[i % len(cols)].write(member["university_career"])


about_us()
