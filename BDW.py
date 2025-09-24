import streamlit as st
import time

st.set_page_config(page_title="Happy 21st 🎉", page_icon="🎂", layout="centered")

st.title("💖 7 Praises for You 💖")
st.markdown("Click below to reveal each praise, one at a time! 🎁")

# List of 7 polished praises
praises = [
    "Your eyes hold so much depth that anyone who can’t swim could easily drown in them. I’m lucky I know how to swim — that’s why I’m still alive.",
    "Your smile is so contagious that it has the power to make even the sanest person go delightfully insane.",
    "Your lips are like rose petals — roses that could only be found in the Garden of Eden.",
    "The way you carry yourself with so much beauty and elegance… I think I need to inform the Oxford Dictionary team that the word ‘elegance’ should be replaced with ‘Snehance.’",
    "When I say something sarcastically bad to you and you respond with ‘Hawww,’ that ‘Hawww’ has the most wholesome effect.",
    "When you get upset, it feels like the whole world stops. I have to do everything to revive it by making you happy. I like doing that because I am the savior of this world, and all of this is for the life that exists on Earth — especially yours.",
    "Being around you makes everything brighter. Your presence turns ordinary moments into memories I’ll cherish forever, and I can’t imagine a day without your light."
]

# Keep track of progress using session state
if "index" not in st.session_state:
    st.session_state.index = 0

# Button to reveal the next praise
if st.button("✨ Reveal Next Praise ✨"):
    if st.session_state.index < len(praises):
        # Display praise with heart emoji animation
        st.success(f"💖 {praises[st.session_state.index]} 💖")
        st.session_state.index += 1
        # Small heart animation using st.markdown
        st.markdown("❤️✨💖✨❤️")
        time.sleep(0.3)  # brief pause for effect
    else:
        st.balloons()
        st.warning("🎉 All 7 praises revealed! You are truly amazing! 💕")
