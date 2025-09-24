import streamlit as st
import time

# List of praises
praises = [
    "Your eyes hold so much depth that anyone who can’t swim could easily drown in them. I’m lucky I know how to swim — that’s why I’m still alive.",
    "Your smile is so contagious that it has the power to make even the sanest person go delightfully insane.",
    "Your lips are like rose petals — roses that could only be found in the Garden of Eden.",
    "The way you carry yourself with so much beauty and elegance… I think I need to inform the Oxford Dictionary team that the word ‘elegance’ should be replaced with ‘Snehance.’",
    "When I say something sarcastically bad to you and you respond with ‘Hawww,’ that ‘Hawww’ has the most wholesome effect.",
    "When you get upset, it feels like the whole world stops. I have to do everything to revive it by making you happy. I like doing that because I am the savior of this world, and all of this is for the life that exists on Earth — especially yours.",
    "Being around you makes everything brighter. Your presence turns ordinary moments into memories I’ll cherish forever, and I can’t imagine a day without your light."
]

# Set page config
st.set_page_config(page_title="Happy 21st Birthday Sneha 🎉", layout="wide")

# CSS for pastel background + matching text color
st.markdown("""
<style>
@keyframes gradientBG {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

.stApp {
  background: linear-gradient(-45deg, #ff9a9e, #ffd1dc, #ffecd2, #ffe0ac);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  color: #ff6f91;  /* Soft pink/red for text */
}

.stButton>button {
  background-color: #ff9a9e;
  color: white;
  font-weight: bold;
  border-radius: 10px;
  padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# Main content
st.title("🎂 Happy 21st Birthday Sneha! 🎉")
st.markdown("""
## 💌 My Dearest Sneha  
On this very special day, I want to celebrate *you*.  
You’re not just turning 21, you’re stepping into a beautiful new chapter of life.  
May your day be filled with love, laughter, and memories that last forever. 🥳💖  
""")

st.markdown("---")
st.header("💖 7 Praises for You 💖")
st.markdown("Click below to reveal each praise, one at a time! 🎁")

if "index" not in st.session_state:
    st.session_state.index = 0

if st.button("✨ Reveal Next Praise ✨"):
    if st.session_state.index < len(praises):
        st.success(f"💖 {praises[st.session_state.index]} 💖")
        st.session_state.index += 1
        st.markdown("❤️✨💖✨❤️")
        time.sleep(0.3)
    else:
        st.balloons()
        st.success("🎉 Happy 21st once again, Sneha! You are truly amazing and loved 💕")
