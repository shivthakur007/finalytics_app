
import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Happy 21st Birthday Sneha 🎉", layout="centered")

# ========== DYNAMIC BACKGROUND (HTML) ==========
background_html = """
<style>
body {
  margin: 0;
  height: 100vh;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(270deg, #ff758c, #ff7eb3, #6a82fb, #fc5c7d);
  background-size: 800% 800%;
  animation: gradientAnimation 20s ease infinite;
}
@keyframes gradientAnimation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.sparkle, .heart {
  position: absolute;
  opacity: 0.8;
}
.sparkle {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: floatSparkles 10s linear infinite;
}
.heart {
  width: 20px;
  height: 20px;
  background: red;
  transform: rotate(45deg);
  animation: floatHearts 12s linear infinite;
}
.heart:before,
.heart:after {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  background: red;
  border-radius: 50%;
}
.heart:before {
  top: -10px;
  left: 0;
}
.heart:after {
  left: -10px;
  top: 0;
}
@keyframes floatSparkles {
  from { transform: translateY(100vh) scale(0.5); opacity: 1; }
  to { transform: translateY(-10vh) scale(1.2); opacity: 0; }
}
@keyframes floatHearts {
  from { transform: translateY(100vh) scale(0.6); opacity: 1; }
  to { transform: translateY(-10vh) scale(1); opacity: 0; }
}
</style>
<script>
function createSparkle() {
  const sparkle = document.createElement("div");
  sparkle.classList.add("sparkle");
  sparkle.style.left = Math.random() * window.innerWidth + "px";
  sparkle.style.animationDuration = 5 + Math.random() * 5 + "s";
  document.body.appendChild(sparkle);
  setTimeout(() => sparkle.remove(), 10000);
}
function createHeart() {
  const heart = document.createElement("div");
  heart.classList.add("heart");
  heart.style.left = Math.random() * window.innerWidth + "px";
  heart.style.animationDuration = 6 + Math.random() * 6 + "s";
  document.body.appendChild(heart);
  setTimeout(() => heart.remove(), 12000);
}
setInterval(createSparkle, 400);
setInterval(createHeart, 1200);
</script>
"""
st.markdown(background_html, unsafe_allow_html=True)

# ========== MAIN CONTENT ==========
st.title("🎂 Happy 21st Birthday Sneha! 🎉")

st.markdown(
    """
    ## 💌 My Dearest Sneha,  
    On this very special day, I want to celebrate *you*.  
    You’re not just turning 21, you’re stepping into a beautiful new chapter of life.  
    May your day be filled with love, laughter, and memories that last forever. 🥳💖  
    """
)

st.markdown("---")

st.header("💖 7 Praises for You 💖")
st.markdown("Click below to reveal each praise, one at a time! 🎁")

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

# Session state to keep track
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

