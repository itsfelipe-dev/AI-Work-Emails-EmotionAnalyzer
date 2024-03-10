import streamlit as st
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
            icon="github",  # Some icons are available... like Streamlit!
            url="https://extras.streamlitapp.com",
        )
    st.title("About Us")
    st.write("Meet our team members and learn about our university careers!⭐️")


    team_members = [
        {
            "name": "**Andres Orjuela**",
            "img_url": "https://avatars.githubusercontent.com/u/72109168?v=4",
            "university_career": "Software Engineer",
        },
        {
            "name": "**Cindy Rojas**",
            "img_url": "https://via.placeholder.com/150",
            "university_career": "Heathy Care",
        },
        {
            "name": "**Jackeline Wilches**",
            "img_url": "https://via.placeholder.com/150",
            "university_career": "Business Administration",
        },
        {
            "name": "**Maria Paula**",
            "img_url": "https://via.placeholder.com/150",
            "university_career": "Software Engineer",
        },
        {
            "name": "**Daniel Osorio**",
            "img_url": "https://via.placeholder.com/150",
            "university_career": "System Engineer",
        },
    ]

    cols = st.columns(3)
    for i, member in enumerate(team_members):
        cols[i % len(cols)].markdown(
            f'<img src="{member["img_url"]}" style="border-radius: 50%; max-width: 10em;">',
            unsafe_allow_html=True,
        )
        cols[i % len(cols)].write(member["name"])
        # cols[i % len(cols)].write(member["name"])

        cols[i % len(cols)].write(member["university_career"])


about_us()
# def example_1():
#     mention(
#         label="Github",
#         icon="github",  # Some icons are available... like Streamlit!
#         url="https://extras.streamlitapp.com",
#     )
