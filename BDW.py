import streamlit as st

# List of praises
praises = [
    "Your eyes have so much depth that anyone who doesn’t know how to swim could drown, but I’m lucky—I know how to swim, so I’m still alive.",
    "Your smile is so contagious that it has the power to make even the sanest person go delightfully insane.",
    "Your lips are like petals of roses, roses that could only be found in the Garden of Eden.",
    "The way you carry yourself with so much beauty and elegance makes me think I should inform the Oxford Dictionary team to replace the word 'elegance' with 'snehance.'",
    "When I say something sarcastically bad to you and you reply 'Haww,' that 'Haww' has a wholesome effect on me.",
    "When you get upset, the whole world stops, and I have to do everything to revive it by making you happy. I like to do that, as if I were the savior of the world, bringing life back to Earth.",
]

# Set page config
st.set_page_config(page_title="Happy Birthday Sneha 🎉", layout="wide")

# Add background with CSS animation (fixed layering)
page_bg = """
<style>
@keyframes gradient {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}
.stApp {
  background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1, #fbc2eb);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  position: relative;
  z-index: 0;
}
.stApp > * {
  position: relative;
  z-index: 1;
  color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Main content
st.title("🎂 Happy 21st Birthday Sneha 🎂")
st.subheader("✨ A special collection of praises just for you ✨")

if "praise_index" not in st.session_state:
    st.session_state.praise_index = 0

if st.button("💖 Show Praise 💖"):
    if st.session_state.praise_index < len(praises):
        st.write(f"**{praises[st.session_state.praise_index]}**")
        st.session_state.praise_index += 1
    else:
        st.balloons()
        st.success("🎉 You've read all the praises! You're truly special! 💕")
