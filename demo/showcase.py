"""Streamlit demo showcase for Chopstickz AI video editing platform."""

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title="Chopstickz Demo", layout="centered")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[
            "Home",
            "Auto Clip",
            "Normalized Output Vector",
            "Facial Recognition Model",
        ],
        icons=["house", "fire", "gear", "activity"],
        default_index=0,
    )

if selected == "Home":
    st.title("Chopstickz")
    st.write("A proprietary AI Video Editing Platform")
    st.image("assets/image.png", caption="Sunrise by the mountains")
    st.write(
        "We live in a digital world fueled and filled with more content than ever. "
        "After conducting extensive market research with numerous Twitch and YouTube "
        "creators, we stumbled upon a rather niche issue. Content creators face "
        "tremendous difficulty when having to edit lengthy videos; Their tools are "
        "often designed to be used by experts. To account for this, many have to waste "
        "a lot of time learning tools or resort to outsourcing their work. In addition "
        "to this, the user experience with certain editing software often feels archaic "
        "with a disproportionate amount of tools provided to the user."
    )

elif selected == "Auto Clip":
    st.title("Auto Clip")
    video_file = open("assets/clip_3.mp4", "rb")
    video_bytes = video_file.read()
    st.write("Entertaining clip captured by our algorithm")
    st.video(video_bytes)
    st.write(
        "Our proudest moment was when our first output was generated. We had selected "
        "a random Pewdiepie Minecraft stream and when we saw the quality of the short "
        "format videos generated, we knew that all the work we had put in was not in "
        "vain and our project indeed had a future."
    )

elif selected == "Normalized Output Vector":
    st.title("Normalized Output Vector")
    st.image("assets/graph.png")
    st.write(
        "Retrieves voice transcription using Whisper, chat logs using OCR/Web Scraping, "
        "and creator expressions using OpenCV. Uses Roberta's fine-tuned model to analyze "
        "the viewership engagement (chats) with the creator, and its sentiment. Uses a "
        "fine-tuned T5 model to transcribe the stream and run a text-text analysis to "
        "gauge the streamer's key moments. Uses a DeepFace model to read the streamer's "
        "reaction and weigh this metric with the models used above to produce valuable "
        "insights into key moments of a stream. We normalize these metrics and generate "
        "spikes that occur at certain time intervals, representing high levels of "
        "engagement between the streamer and the viewer."
    )

elif selected == "Facial Recognition Model":
    image_comparison(
        img1="assets/image_1.png",
        img2="assets/image_2.png",
    )

elif selected == "Contact":
    st.title("Contact")

